#include <stdio.h>
#include <malloc.h>

#include "inpaint.h"

// Type for flag array
#define KNOWN 0  // Pixel value is known
#define INSIDE 1  // Pixel value is unknown; pixel is inside of inpaint area
#define BAND 2 // Pixel value is unknown; pixel is on border of inpaint area

// Using integers instead of binary due to GCC warnings
#define TL 128// 0b10000000 // Assigned bit for the Top Left pixel
#define TC 64 // 0b01000000 // Assigned bit for the Top Centre pixel
#define TR 32 // 0b00100000 // Assigned bit for the Top Right pixel
#define ML 16 // 0b00010000 // Assigned bit for the Middle Left pixel
#define MR 8  // 0b00001000 // Assigned bit for the Middle Right pixel
#define BL 4  // 0b00000100 // Assigned bit for the Bottom Left pixel
#define BC 2  // 0b00000010 // Assigned bit for the Bottom Centre pixel
#define BR 1  // 0b00000001 // Assigned bit for the Bottom Right pixel

#define T  224 //(TL + TC + TR)	// (TL | TC | TR)	// Assigned bits for the top row			
#define C  24  //(ML + MR)		// (ML | MR)		// Assigned bits for the centre row
#define B  7   //(BL + BC + BR)	// (BL | BC | BR)	// Assigned bits for the bottom row
#define L  148 //(TL + ML + BL)	// (TL | ML | BL)	// Assigned bits for the left column
#define M  66  //(TC + BC)		// (TC | BC)		// Assigned bits for the middle column
#define R  41  //(TR + MR + BR)	// (TR | MR | BR)	// Assigned bits for the right column

#define TOP_LEFT_CORNER 	11  // (BC + BR + MR)			 // (BC | BR | MR) // Bits which need to be checked for the pixel in the top left corner 
#define TOP_RIGHT_CORNER 	22  // (ML + BL + BC)			 // (ML | BL | BC) // Bits which need to be checked for the pixel in the top right corner
#define BOTTOM_LEFT_CORNER 	104 // (TC + TR + MR)			 // (TC | TR | MR) // Bits which need to be checked for the pixel in the bottom left corner
#define BOTTOM_RIGHT_CORNER 208 // (TL + TC + ML)			 // (TL | TC | ML) // Bits which need to be checked for the pixel in the bottom right corner
#define TOP_ROW 			31  // (ML + MR + BL + BC + BR)  // (B | C) 	   // Bits which need to be checked for the pixels in the top row
#define LEFT_COLUMN			107 // (TC + TR + MR + BC + BR)  // (M | R) 	   // Bits which need to be checked for the pixels in the left column
#define RIGHT_COLUMN 		214 // (TL + TC + ML + BL + BC)  // (L | M) 	   // Bits which need to be checked for the pixels in the right column
#define BOTTOM_ROW			248 // (TL + TC + TR + ML + MR)  // (T | C) 	   // Bits which need to be checked for the pixels in the bottom row


// This function allows the location of pixels which need to be check be defined
size_t sub_mark_band(uint8_t* f, size_t x, size_t y, size_t w, uint8_t mask){
	uint32_t i = y * w;
	i += x;

	if (f[i] != INSIDE) {
		// The pixel must be inside the inpaint area for it to be a candidate for marking as BAND.
		return 0;
	}

	uint16_t yNeg = y - 1;
	uint16_t xNeg = x - 1;
	uint16_t xPos = x + 1;
	uint16_t yPos = y + 1;
	
	// Top-left
	if (mask & TL) // Bound check
	{
		uint32_t element = yNeg * w;
		element += xNeg;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Top-center
	if (mask & TC) // Bound check
	{
		uint32_t element = yNeg * w;
		element += x;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Top-right
	if (mask & TR) // Bound check
	{
		uint32_t element = yNeg * w;
		element += xPos;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Mid-left
	if (mask & ML) // Bound check
	{
		uint32_t element = y * w;
		element += xNeg;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Mid-right
	if (mask & MR) // Bound check
	{
		uint32_t element = y * w;
		element += xPos;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Bottom-left
	if (mask & BL) // Bound check
	{
		uint32_t element = yPos * w;
		element += xNeg;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Bottom-center
	if (mask & BC) // Bound check
	{
		uint32_t element =  yPos * w;
		element += x;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}

	// Bottom-right
	if (mask & BR) // Bound check
	{
		uint32_t element =  yPos * w;
		element += xPos;
		if (f[element] == KNOWN)
		{
			f[i] = BAND;
			return 1;
		}
	}
	return 0;
}

// THis function is meant for the pixels away from the border
size_t full_sub_mark_band(uint8_t* f, size_t x, size_t y, size_t w) {
	uint32_t i = y * w;
	i +=  x;
	if (f[i] != INSIDE) {
		// The pixel must be inside the inpaint area for it to be a candidate for marking as BAND.
		return 0;
	}

	// If any of the 8 neighbouring pixels is KNOWN, the current pixel is marked as BAND.
	// Bound checks are necessary in case the current pixel is on the border of the image (since then the neighbour is outside of the image).

	// Top-left
	uint32_t element = y - 1;
	element *= w;
	element += x - 1;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Top-center
	element++;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Top-right
	element++;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Mid-right
	element += w;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Mid-left 
	element -= 2;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Bottom-left
	element += w;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Bottom-center
	element++;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	// Bottom-right
	element++;
	if (f[element] == KNOWN) {
		f[i] = BAND;
		return 1;
	}

	return 0;
}

// Find all INSIDE pixels, and mark them as BAND when they have at least one KNOWN neighbour.
// The number of pixels marked as BAND is returned.
size_t mark_band(uint8_t* f, size_t w, size_t h)
{
	size_t found_pixels = 0;
	for (size_t y = 1; y < h-1; y++) {
		for (size_t x = 1; x < w-1; x++) {
			found_pixels += full_sub_mark_band(f, x, y, w); 		 // Centre plane
		}
		found_pixels += sub_mark_band(f, 0, y, w, LEFT_COLUMN);      // left column
		found_pixels += sub_mark_band(f, w-1, y, w, RIGHT_COLUMN);   // right column
	}

	for (size_t x = 1; x < w-1; x++) {
		found_pixels += sub_mark_band(f, x, h-1, w, BOTTOM_ROW);     // bottom row
		found_pixels += sub_mark_band(f, x, 0, w, TOP_ROW);          // Top row
	}

	found_pixels += sub_mark_band(f, 0, 0, w, TOP_LEFT_CORNER);      // Top left
	found_pixels += sub_mark_band(f, 0, h-1, w, BOTTOM_LEFT_CORNER); // Bottom left
	found_pixels += sub_mark_band(f, w-1, 0, w, TOP_RIGHT_CORNER);   // Top right
	found_pixels += sub_mark_band(f, w-1, h-1, w, BOTTOM_RIGHT_CORNER); // Bottom right

	return found_pixels;
}

// Set the pixel at (x, y) to the weighted mean value of the KNOWN neighbouring pixels around it.
// The diagonal neighbours (top-left, top-right, bottom-left, bottom-right) are weighted by 1/sqrt(2),
// and the cardinal neighbours (top-center, mid-left, mid-right, bottom-center) are weighted by 1.
// The argument v is one of the colour channels (r, g, b) of the image data.
void inpaint_pixel(size_t x, size_t y, uint8_t* v, uint8_t* f, size_t w, size_t h)
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
			total_weight++;
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
			total_weight++;
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
			total_weight++;
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
			total_weight++;
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
	if (total_weight == 0) {
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
	uint8_t* f = (uint8_t*)malloc(w * h * sizeof(uint8_t));
	if (f == NULL) {
		fprintf(stderr, "Error: could not allocate memory for flag array.\n");
		return false;
	}

	// Initialize flag array using mask (true <-> INSIDE; false <-> KNOWN)
	for (size_t index = 0; index < w * h; index++) {
		f[index] = m[index] ? INSIDE : KNOWN;
	}

	// Main algorithm loop
	while (true) {

		size_t pixels_in_band = mark_band(f, w, h);
		if (pixels_in_band == 0) {
			// All pixels have been inpainted
			break;
		}
		
		// Inpaint all pixels in the band
		for (size_t y = 0; y < h; y++) {
			for (size_t x = 0; x < w; x++) {
				if (f[y * w + x] == BAND) {
					inpaint_pixel(x, y, r, f, w, h);
					inpaint_pixel(x, y, g, f, w, h);
					inpaint_pixel(x, y, b, f, w, h);
				}
			}
		}

		// Mark all pixels in the band as known
		for (size_t y = 0; y < h; y++)
		{
			for (size_t x = 0; x < w; x++)
			{
				if (f[y * w + x] == BAND)
				{
					f[y * w + x] = KNOWN;
				}
			}
		}
	}

	// Free memory of flag array
	free(f);

	return true;
}
