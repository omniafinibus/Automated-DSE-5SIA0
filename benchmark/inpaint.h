#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Inpaint algorithm. Image data (red, green, blue) is passed as the r, g, b arrays. Array m contains the inpaint
// area mask (true means the corresponding pixel must be inpainted). Image size (width, height) is passed in the
// w, h arguments. All arrays have width x height elements. The first element corresponds to the top-left pixel in
// the image, and the next elements run from left-to-right, and then top-to-bottom.
//
// The algorithm should modify the r, g, b arrays to return its result.
// 
// If the algorithm ran succesfully, true must be returned; if it failed, false must be returned.
bool inpaint(uint8_t* r, uint8_t* g, uint8_t* b, bool* m, size_t w, size_t h);
