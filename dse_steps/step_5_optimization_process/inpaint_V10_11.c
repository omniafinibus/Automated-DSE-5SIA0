#include <stdio.h>
#include <malloc.h>

#include "inpaint.h"

// Type for flag array
typedef enum
{
	KNOWN, // Pixel value is known
	INSIDE, // Pixel value is unknown; pixel is inside of inpaint area
	BAND // Pixel value is unknown; pixel is on border of inpaint area
} flag_t;

// Find all INSIDE pixels, and mark them as BAND when they have at least one KNOWN neighbour.
// The number of pixels marked as BAND is returned.
size_t mark_band(flag_t* f, size_t w, size_t h)
{
	size_t found_pixels = 0;

	for (size_t y = 0; y < h; y++)
	{
		for (size_t x = 0; x < w; x++)
		{
			uint32_t wShift = w - 1;
			uint32_t hShift = h - 1;
			uint16_t yNeg = y - 1;
			uint16_t yPos = y + 1;
			uint16_t xNeg = x - 1;
			uint16_t xPos = x + 1;
			uint32_t i = y * w;
			i +=  x;
			if (f[i] != INSIDE)
			{
				// The pixel must be inside the inpaint area for it to be a candidate for marking as BAND.
				continue;
			}

			// If any of the 8 neighbouring pixels is KNOWN, the current pixel is marked as BAND.
			// Bound checks are necessary in case the current pixel is on the border of the image (since then the neighbour is outside of the image).

			// Top-left
			if (x > 0 && y > 0) // Bound check
			{
				uint32_t element =  yNeg * w;
				element +=  xNeg;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Top-center
			if (y > 0) // Bound check
			{
				uint32_t element =  yNeg * w;
				element += x;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Top-right
			if (x < wShift && y > 0) // Bound check
			{
				uint32_t element =  yNeg * w;
				element += xPos;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Mid-left
			if (x > 0) // Bound check
			{
				uint32_t element = y * w;
				element += xNeg;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Mid-right
			if (x < wShift) // Bound check
			{
				uint32_t element = y * w;
				element += xPos;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Bottom-left
			if (x > 0 && y < hShift) // Bound check
			{
				uint32_t element = yPos * w;
				element += xNeg;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Bottom-center
			if (y < hShift) // Bound check
			{
				uint32_t element =  yPos * w;
				element += x;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}

			// Bottom-right
			if (x < wShift && y < hShift) // Bound check
			{
				uint32_t element =  yPos * w;
				element += xPos;
				if (f[element] == KNOWN)
				{
					f[i] = BAND;
					found_pixels++;
					continue;
				}
			}
		}
	}

	return found_pixels;
}

// Set the pixel at (x, y) to the weighted mean value of the KNOWN neighbouring pixels around it.
// The diagonal neighbours (top-left, top-right, bottom-left, bottom-right) are weighted by 1/sqrt(2),
// and the cardinal neighbours (top-center, mid-left, mid-right, bottom-center) are weighted by 1.
// The argument v is one of the colour channels (r, g, b) of the image data.
void inpaint_pixel(size_t x, size_t y, uint8_t* v, flag_t* f, size_t w, size_t h)
{
	float total_weight = 0; // Sum of weights of KNOWN neighbours.
	float value = 0; // Sum of weighted values of KNOWN neighbours.

	// Top-left
	if (x > 0 && y > 0) // Bound check
	{
		uint32_t element = (y - 1);
		element = element * w;
		element = element + (x - 1);
		if (f[element] == KNOWN)
		{
			value += 0.707 * v[element];
			total_weight += 0.707;
		}
	}

	// Top-center
	if (y > 0) // Bound check
	{
		uint32_t element = (y - 1);
		element = element * w;
		element = element + x;
		if (f[element] == KNOWN)
		{
			value += v[element];
			total_weight += 1;
		}
	}

	// Top-right
	if (x < w - 1 && y > 0) // Bound check
	{
		uint32_t element = (y - 1);
		element = element * w;
		element = element + (x + 1);
		if (f[element] == KNOWN)
		{
			value += 0.707 * v[element];
			total_weight += 0.707;
		}
	}

	// Mid-left
	if (x > 0) // Bound check
	{
		uint32_t element = y * w;
		element = element + (x - 1);
		if (f[element] == KNOWN)
		{
			value += v[element];
			total_weight += 1;
		}
	}

	// Mid-right
	if (x < w - 1) // Bound check
	{
		uint32_t element = y * w;
		element = element + (x + 1);
		if (f[element] == KNOWN)
		{
			value += v[element];
			total_weight += 1;
		}
	}

	// Bottom-left
	if (x > 0 && y < h - 1) // Bound check
	{
		uint32_t element = (y + 1);
		element = element * w;
		element = element + (x - 1);
		if (f[element] == KNOWN)
		{
			value += 0.707 * v[element];
			total_weight += 0.707;
		}
	}

	// Bottom-center
	if (y < h - 1) // Bound check
	{
		uint32_t element = (y + 1);
		element = element * w;
		element = element + x;
		if (f[element] == KNOWN)
		{
			value += v[element];
			total_weight += 1;
		}
	}

	// Bottom-right
	if (x < w - 1 && y < h - 1) // Bound check
	{
		uint32_t element = (y + 1);
		element = element * w;
		element = element + (x + 1);
		if (f[element] == KNOWN)
		{
			value += 0.707 * v[element];
			total_weight += 0.707;
		}
	}

	// Make sure there was at least one KNOWN neighbour, or we cause division-by-zero.
	if (total_weight == 0)
	{
		fprintf(stderr, "Warning: pixel (%zu, %zu) to be inpainted has no known neighbours. This should not happen and indicates a bug in the algorithm.\n", x, y);
		v[y * w + x] = 0;
		return;
	}

	// Set the value of the pixel to be inpainted to the mean of the KNOWN neighbours.
	v[y * w + x] = (uint8_t)(value / total_weight);
}

bool inpaint(uint8_t* r, uint8_t* g, uint8_t* b, bool* m, size_t w, size_t h)
{
	// Allocate memory for flag array
	flag_t* f = (flag_t*)malloc(w * h * sizeof(flag_t));
	if (f == NULL)
	{
		fprintf(stderr, "Error: could not allocate memory for flag array.\n");
		return false;
	}

	// Initialize flag array using mask (true <-> INSIDE; false <-> KNOWN)
	for (size_t index = 0; index < w * h; index += 1)
	{
		f[index] = m[index] ? INSIDE : KNOWN;
	}

	// Main algorithm loop
	while (true)
	{
		size_t pixels_in_band = mark_band(f, w, h);
		if (pixels_in_band == 0)
		{
			// All pixels have been inpainted
			break;
		}

		// Inpaint all pixels in the band
		for (size_t y = 0; y < h; y += 1)
		{
			for (size_t x = 0; x < w; x += 1)
			{
				if (f[y * w + x] == BAND)
				{
				}
			}
		}

		// Mark all pixels in the band as known
		for (size_t y = 0; y < h; y += 1)
		{
			for (size_t x = 0; x < w; x += 1)
			{
				if (f[y * w + x] == BAND)
				{
					inpaint_pixel(x, y, r, f, w, h);
					inpaint_pixel(x, y, g, f, w, h);
					inpaint_pixel(x, y, b, f, w, h);
					f[y * w + x] = KNOWN;
				}
			}
		}
	}

	// Free memory of flag array
	free(f);

	return true;
}
