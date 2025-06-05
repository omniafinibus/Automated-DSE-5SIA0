#pragma once
// Functions for reading from/writing to BMP files.

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

// Read mask data from monochrome BMP file, returning the width and height using pointers. Make sure to free the returned memory.
// The return value points to an array of width x height elements. The first element corresponds to the top-left pixel in the image,
// and the next elements run from left-to-right, and then top-to-bottom. If the file could not be read, NULL is returned.
bool* bmp_read_mask(char* filename, size_t* width, size_t* height);

// Write mask data to monochrome BMP file. The mask_data argument must point to an array of width x height elements. The first
// element corresponds to the top-left pixel in the image, and the next elements run from left-to-right, and then top-to-bottom.
// If the file was written succesfully, true is returned; if it failed, false is returned.
bool bmp_write_mask(char* filename, bool* mask_data, size_t width, size_t height);

// Read image data from 24 bit per pixel BMP file, returning the image data (red, green, blue), width and height using pointers.
// Make sure to free the returned memory (red, green, blue). The returned image data pointers point to arrays of width x height elements.
// The first element corresponds to the top-left pixel in the image, and the next elements run from left-to-right, and then top-to-bottom.
// If the file was read succesfully, true is returned; if it failed, false is returned.
bool bmp_read_image(char* filename, uint8_t** red, uint8_t** green, uint8_t** blue, size_t* width, size_t* height);

// Write image data to 24 bit per pixel BMP file. The image data (red, green, blue) arguments must point to arrays of width x height
// elements. The first element corresponds to the top-left pixel in the image, and the next elements run from left-to-right, and
// then top-to-bottom. If the file was written succesfully, true is returned; if it failed, false is returned.
bool bmp_write_image(char* filename, uint8_t* red, uint8_t* green, uint8_t* blue, size_t width, size_t height);
