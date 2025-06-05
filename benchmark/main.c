#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <time.h>
#include <malloc.h>

#include "bmp.h"
#include "inpaint.h"

int main(int argc, char* argv[])
{
	if (argc != 4)
	{
		if (argc >= 1)
		{
			fprintf(stderr, "Usage: %s input_image.bmp mask_image.bmp output_image.bmp\n", argv[0]);
		}
		else
		{
			fprintf(stderr, "Usage: inpaint input_image.bmp mask_image.bmp output_image.bmp\n");
		}
		return -1;
	}

	char* input_image = argv[1];
	char* mask_image = argv[2];
	char* output_image = argv[3];

	// Read image
	size_t w = 0;
	size_t h = 0;
	uint8_t* r = NULL;
	uint8_t* g = NULL;
	uint8_t* b = NULL;

	printf("Loading image: '%s'.\n", input_image);
	if (!bmp_read_image(input_image, &r, &g, &b, &w, &h))
	{
		return -1;
	}

	// Read mask
	size_t w_mask = 0;
	size_t h_mask = 0;
	bool* m = NULL;

	printf("Loading mask: '%s'.\n", mask_image);
	m = bmp_read_mask(mask_image, &w_mask, &h_mask);
	if (m == NULL)
	{
		free(r);
		free(g);
		free(b);
		return -1;
	}

	// Make sure image and maks have same size
	if (w_mask != w || h_mask != h)
	{
		fprintf(stderr, "Mask size (%zu x %zu pixels) is not equal to image size (%zu x %zu pixels).\n", w_mask, h_mask, w, h);
		free(m);
		free(r);
		free(g);
		free(b);
		return -1;
	}

	// Run inpaint algorithm
	printf("Running inpaint algorithm...\n");
	
	clock_t tic = clock();
	if (!inpaint(r, g, b, m, w, h))
	{
		fprintf(stderr, "Inpaint algorithm failed.\n");
		free(m);
		free(r);
		free(g);
		free(b);
		return -1;
	}
	clock_t toc = clock();

	double runtime = 1000 * (toc - tic) / CLOCKS_PER_SEC; // in ms
	printf("Finished. Runtime: %.0lf ms.\n", runtime);

	// Write output image
	printf("Saving image: '%s'.\n", output_image);
	if (!bmp_write_image(output_image, r, g, b, w, h))
	{
		free(m);
		free(r);
		free(g);
		free(b);
		return -1;
	}

	// Clean-up
	free(m);
	free(r);
	free(g);
	free(b);
	return 0;
}