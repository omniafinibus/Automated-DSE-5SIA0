#define _CRT_SECURE_NO_WARNINGS // Or fopen() will break on Windows...
#include <stdio.h>
#include <malloc.h>

#include "bmp.h"

// BMP file header (see https://en.wikipedia.org/wiki/BMP_file_format)
#pragma pack(push, 1)
typedef struct {
	uint16_t  type;             // Magic identifier: 0x4d42
	uint32_t  size;             // File size in bytes
	uint16_t  reserved1;        // Not used
	uint16_t  reserved2;        // Not used
	uint32_t  offset;           // Offset to image data in bytes from beginning of file (54 bytes)
	uint32_t  dib_header_size;  // DIB Header size in bytes (40 bytes)
	int32_t   width_px;         // Width of the image
	int32_t   height_px;        // Height of image
	uint16_t  num_planes;       // Number of color planes
	uint16_t  bits_per_pixel;   // Bits per pixel
	uint32_t  compression;      // Compression type
	uint32_t  image_size_bytes; // Image size in bytes
	int32_t   x_resolution_ppm; // Pixels per meter
	int32_t   y_resolution_ppm; // Pixels per meter
	uint32_t  num_colors;       // Number of colors  
	uint32_t  important_colors; // Important colors 
} bmp_header_t;
#pragma pack(pop)

// Read raw image data from BMP file, returning the width, height, bits per pixel, and row size in bytes using pointers. Make sure to free the returned memory.
uint8_t* bmp_read(char* filename, size_t* width, size_t* height, size_t* bits_per_pixel, size_t* row_size);

// Write raw image data to BMP file.
bool bmp_write(char* filename, uint8_t* image_data, size_t width, size_t height, size_t bits_per_pixel, size_t row_size);

bool* bmp_read_mask(char* filename, size_t* width, size_t* height)
{
	size_t w = 0;
	size_t h = 0;
	size_t bpp = 0;
	size_t row_size = 0;

	// Read mask image
	uint8_t* raw_image_data = bmp_read(filename, &w, &h, &bpp, &row_size);
	if (raw_image_data == NULL)
	{
		return NULL;
	}

	// Ensure mask image is monochrome
	if (bpp != 1)
	{
		fprintf(stderr, "Error: mask must be a monochrome image (1 bit per pixel), while file '%s' has %zu bits per pixel.\n", filename, bpp);
		free(raw_image_data);
		return NULL;
	}

	// Allocate memory for mask data
	bool* mask_data = (bool*)malloc(w * h * sizeof(bool));
	if (mask_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for mask data.\n");
		free(raw_image_data);
		return NULL;
	}

	// Unpack the booleans from the raw image data (little-endian); flip y direction, since BMP stores rows bottom-to-top
	uint8_t* row_ptr = raw_image_data + (h - 1) * row_size;
	bool* mask_ptr = mask_data;
	for (size_t y = 0; y < h; y += 1)
	{
		for (size_t x = 0; x < w; x += 1)
		{
			*mask_ptr = !(row_ptr[x / 8] & (0x80 >> x % 8));
			mask_ptr += 1;
		}
		row_ptr -= row_size;
	}

	free(raw_image_data);

	*width = w;
	*height = h;
	return mask_data;
}

bool bmp_write_mask(char* filename, bool* mask_data, size_t width, size_t height)
{
	// Check arguments
	if (width == 0 || height == 0)
	{
		fprintf(stderr, "Error: writing zero-size images is not supported.\n");
		return false;
	}

	// Determine padded row size
	size_t row_size = width / 32; // in 32-bit words
	if (width % 32 != 0)
	{
		row_size += 1; // in 32-bit words
	}
	row_size *= 4; // in bytes

	// Allocate memory for image data
	uint8_t* raw_image_data = (uint8_t*)calloc(row_size * height, sizeof(uint8_t));
	if (raw_image_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for image data.\n");
		return false;
	}

	// Pack the booleans into the image data (little-endian); flip y direction, since BMP stores rows bottom-to-top
	uint8_t* row_ptr = raw_image_data + (height - 1) * row_size;
	bool* mask_ptr = mask_data;
	for (size_t y = 0; y < height; y += 1)
	{
		for (size_t x = 0; x < width; x += 1)
		{
			if (!*mask_ptr)
			{
				row_ptr[x / 8] |= (0x80 >> x % 8);
			}
			mask_ptr += 1;
		}
		row_ptr -= row_size;
	}

	// Write the image
	if (!bmp_write(filename, raw_image_data, width, height, 1, row_size))
	{
		free(raw_image_data);
		return false;
	}

	// Return
	free(raw_image_data);
	return true;
}

bool bmp_read_image(char* filename, uint8_t** red, uint8_t** green, uint8_t** blue, size_t* width, size_t* height)
{
	size_t w = 0;
	size_t h = 0;
	size_t bpp = 0;
	size_t row_size = 0;

	// Read mask image
	uint8_t* raw_image_data = bmp_read(filename, &w, &h, &bpp, &row_size);
	if (raw_image_data == NULL)
	{
		return false;
	}

	// Ensure mask image is monochrome
	if (bpp != 24)
	{
		fprintf(stderr, "Error: mask must be a 24 bit per pixel image, while file '%s' has %zu bits per pixel.\n", filename, bpp);
		free(raw_image_data);
		return false;
	}

	// Allocate memory for red, green, blue data
	uint8_t* red_data = (uint8_t*)malloc(w * h * sizeof(uint8_t));
	if (red_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for image data (red channel).\n");
		free(raw_image_data);
		return false;
	}

	uint8_t* green_data = (uint8_t*)malloc(w * h * sizeof(uint8_t));
	if (green_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for image data (green channel).\n");
		free(red_data);
		free(raw_image_data);
		return false;
	}

	uint8_t* blue_data = (uint8_t*)malloc(w * h * sizeof(uint8_t));
	if (blue_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for image data (blue channel).\n");
		free(green_data);
		free(red_data);
		free(raw_image_data);
		return false;
	}

	// Unpack the raw image data (interleaved, little-endian); flip y direction, since BMP stores rows bottom-to-top
	uint8_t* row_ptr = raw_image_data + (h - 1) * row_size;
	uint8_t* red_ptr = red_data;
	uint8_t* green_ptr = green_data;
	uint8_t* blue_ptr = blue_data;
	for (size_t y = 0; y < h; y += 1)
	{
		for (size_t x = 0; x < w; x += 1)
		{
			*red_ptr = row_ptr[3 * x + 2];
			*green_ptr = row_ptr[3 * x + 1];
			*blue_ptr = row_ptr[3 * x + 0];
			
			red_ptr += 1;
			green_ptr += 1;
			blue_ptr += 1;
		}
		row_ptr -= row_size;
	}

	free(raw_image_data);

	*red = red_data;
	*green = green_data;
	*blue = blue_data;
	*width = w;
	*height = h;
	return true;
}

bool bmp_write_image(char* filename, uint8_t* red, uint8_t* green, uint8_t* blue, size_t width, size_t height)
{
	// Check arguments
	if (width == 0 || height == 0)
	{
		fprintf(stderr, "Error: writing zero-size images is not supported.\n");
		return false;
	}

	// Determine padded row size
	size_t row_size = width * 24 / 32; // in 32-bit words
	if (width * 24 % 32 != 0)
	{
		row_size += 1; // in 32-bit words
	}
	row_size *= 4; // in bytes

	// Allocate memory for image data
	uint8_t* raw_image_data = (uint8_t*)calloc(row_size * height, sizeof(uint8_t));
	if (raw_image_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for image data.\n");
		return false;
	}

	// Pack the channels into the image data (interleaved, little-endian); flip y direction, since BMP stores rows bottom-to-top
	uint8_t* row_ptr = raw_image_data + (height - 1) * row_size;
	uint8_t* red_ptr = red;
	uint8_t* green_ptr = green;
	uint8_t* blue_ptr = blue;
	for (size_t y = 0; y < height; y += 1)
	{
		for (size_t x = 0; x < width; x += 1)
		{
			row_ptr[3 * x + 2] = *red_ptr;
			row_ptr[3 * x + 1] = *green_ptr;
			row_ptr[3 * x] = *blue_ptr;
			red_ptr += 1;
			green_ptr += 1;
			blue_ptr += 1;
		}
		row_ptr -= row_size;
	}

	// Write the image
	if (!bmp_write(filename, raw_image_data, width, height, 24, row_size))
	{
		free(raw_image_data);
		return false;
	}

	// Return
	free(raw_image_data);
	return true;
}

uint8_t* bmp_read(char* filename, size_t* width, size_t* height, size_t* bits_per_pixel, size_t* row_size)
{
	// Open file
	FILE* fp = fopen(filename, "rb");
	if (!fp)
	{
		fprintf(stderr, "Error: could not open file '%s' for reading.\n", filename);
		return NULL;
	}

	// Read header
	bmp_header_t hdr;
	size_t bytes_read = fread(&hdr, 1, sizeof(bmp_header_t), fp);

	if (bytes_read != sizeof(bmp_header_t))
	{
		fprintf(stderr, "Error: could not read BMP header (%zu bytes) from file '%s'.\n", sizeof(bmp_header_t), filename);
		fclose(fp);
		return NULL;
	}

	// Parse header
	if (hdr.type != 0x4d42)
	{
		fprintf(stderr, "Error: file '%s' is not a BMP file.\n", filename);
		fclose(fp);
		return NULL;
	}

	if (hdr.dib_header_size != 40 || hdr.num_planes != 1 || hdr.compression != 0 
		|| hdr.num_colors != 0 || hdr.width_px <= 0 || hdr.height_px <= 0 || hdr.bits_per_pixel == 0)
	{
		fprintf(stderr, "Error: file '%s' is a BMP file with unsupported features.\n", filename);
		fclose(fp);
		return NULL;
	}

	// Compute size of one row of image data
	size_t padded_row_size = hdr.width_px * hdr.bits_per_pixel; // in bits
	if (padded_row_size % 32 != 0)
	{
		// In the BMP file format, rows are padded so they are always a multiple of 4 bytes
		padded_row_size += 32; // in bits
	}
	padded_row_size /= 32; // in 32-bit words
	padded_row_size *= 4; // in bytes

	// Check size of image data
	//size_t image_data_size = hdr.size - hdr.offset;
	size_t image_data_size = hdr.image_size_bytes;
	if (image_data_size < hdr.height_px * padded_row_size)
	{
		fprintf(stderr, "Error: image data in BMP file '%s' is %zu bytes, which does not match with image size (%u x %u pixels).\n", filename, image_data_size, hdr.width_px, hdr.height_px);
		fclose(fp);
		return NULL;
	}

	// Allocate memory for image data
	uint8_t * image_data = (uint8_t*)malloc(image_data_size * sizeof(uint8_t));
	if (image_data == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for image data.\n");
		fclose(fp);
		return NULL;
	}

	// Read image data
	if (fseek(fp, hdr.offset, SEEK_SET) != 0)
	{
		fprintf(stderr, "Error: could not seek to beginning of image data (offset: %u bytes) in file '%s'.\n", hdr.offset, filename);
		free(image_data);
		fclose(fp);
		return NULL;
	}

	bytes_read = fread(image_data, sizeof(uint8_t), image_data_size, fp);
	if (bytes_read != image_data_size)
	{
		fprintf(stderr, "Error: could not read %zu bytes of image data from file '%s'.\n", image_data_size, filename);
		free(image_data);
		fclose(fp);
		return NULL;
	}

	// Close the file
	fclose(fp);

	// Return
	*width = hdr.width_px;
	*height = hdr.height_px;
	*bits_per_pixel = hdr.bits_per_pixel;
	*row_size = padded_row_size;
	return image_data;
}

bool bmp_write(char* filename, uint8_t* image_data, size_t width, size_t height, size_t bits_per_pixel, size_t row_size)
{
	// Create header
	bmp_header_t hdr;
	hdr.type = 0x4d42;
	hdr.size = (uint32_t)(sizeof(bmp_header_t) + row_size * height);
	hdr.reserved1 = 0;
	hdr.reserved2 = 0;
	hdr.offset = sizeof(bmp_header_t);
	hdr.dib_header_size = 40;
	hdr.width_px = (int32_t)width;
	hdr.height_px = (int32_t)height;
	hdr.num_planes = 1;
	hdr.bits_per_pixel = (uint16_t)bits_per_pixel;
	hdr.compression = 0;
	hdr.image_size_bytes = (uint32_t)(row_size * height);
	hdr.x_resolution_ppm = 0;
	hdr.y_resolution_ppm = 0;
	hdr.num_colors = 0;
	hdr.important_colors = 0;

	if (bits_per_pixel == 1)
	{
		// Accomodate color map for monochrome images
		hdr.size += 8;
		hdr.offset += 8;
	}

	// Open file
	FILE* fp = fopen(filename, "wb");
	if (!fp)
	{
		fprintf(stderr, "Error: could not open file '%s' for writing.\n", filename);
		return false;
	}

	// Write header
	size_t bytes_written = fwrite(&hdr, 1, sizeof(bmp_header_t), fp);
	if (bytes_written != sizeof(bmp_header_t))
	{
		fprintf(stderr, "Error: could not write header (%zu bytes) to file '%s'.\n", sizeof(bmp_header_t), filename);
		fclose(fp);
		return false;
	}

	// Write colour map (for monochrome images)
	if (bits_per_pixel == 1)
	{
		// This colour map is required for MS Paint compatibility
		uint8_t colour_map[8] = { 0, 0, 0, 0, 0xff, 0xff, 0xff, 0 };
		bytes_written = fwrite(&colour_map, sizeof(uint8_t), 8, fp);
		if (bytes_written != 8)
		{
			fprintf(stderr, "Error: could not write colour map to file '%s'.\n", filename);
			fclose(fp);
			return false;
		}
	}

	// Write image data
	bytes_written = fwrite(image_data, sizeof(uint8_t), hdr.image_size_bytes, fp);
	if (bytes_written != hdr.image_size_bytes)
	{
		fprintf(stderr, "Error: could not write image data (%u bytes) to file '%s'.\n", hdr.image_size_bytes, filename);
		fclose(fp);
		return false;
	}

	fclose(fp);
	return true;
}
