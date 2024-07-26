#!/usr/bin/env python3
import os
import sys
from config import config_horizontal_search, min_horizontal_pixel, max_horizontal_pixel
import numpy as np
from PIL import Image

RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2

VERTICAL_OFFSET = 200

#arr_averages_by_four_corners_ten_pixels = []
#arr_averages_by_four_corners_forty_pixels = []
#arr_averages_by_fiftieth_horizonal_row = []
#arr_averages_by_ten_pixels = []
#arr_averages_by_hundred_pixels = []


def is_file_vaporwave(filename):
    all_stats = []

    initial_img = Image.open(filename)

    # The following two lines ensure that three color values are present, regardless of the
    # image format
    img = Image.new('RGBA', initial_img.size)
    img.paste(initial_img)

    image_array = np.array(img)

    height = image_array.shape[0]
    width = image_array.shape[1]

    # so for instance if the VERTICAL_OFFSET is 200, we fetch the 200th row
    sample_pixels = image_array[VERTICAL_OFFSET]

    avgs = get_array_color_avgs(sample_pixels)
    return determine_verdict(filename, avgs)


def determine_verdict(filename, avgs):
    MIN_INDEX = 0
    MAX_INDEX = 1

    ranges = config_horizontal_search()
    verdict = True
    verdict_string = "Fails"

    for color in [RED_INDEX, GREEN_INDEX, BLUE_INDEX]:
        min = ranges[color][MIN_INDEX]
        max = ranges[color][MAX_INDEX]
        verdict = verdict and min < avgs[color] and max > avgs[color]

    if verdict:
        verdict_string = "Passes"

    print(filename + ': ' + verdict_string)


# Takes a one-dimensional array of tuples (first key is pixel number, second is color) as a parameter and iterates through it, returning
# a dicts with the max, min, and average values for R, G, and B color dimensions.
def get_array_color_avgs(sample_pixels):
    avgs = [0, 0, 0]
    sums = [0, 0, 0]
    min = min_horizontal_pixel(sample_pixels)
    max = max_horizontal_pixel(sample_pixels)

    for pixel_index in range(min, max):
        pixel = sample_pixels[pixel_index]
        for color in [0, 1, 2]:
            sums[color] = sums[color] + pixel[color]

    for color in [0, 1, 2]:
        avgs[color] = sums[color] / len(sample_pixels)

    return(avgs)
