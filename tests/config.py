#!/usr/bin/env python3

HORIZONTAL_OFFSET = 200
MIN_SAMPLE_AREA = 100

# Red shouild have a wide range, while blue has a more restrictive range. Green should be the narrowest range of all.
def config_horizontal_search():
    ranges = [
        [57, 255],#Red
        [32, 152],#Green
        [135, 255]#Blue
    ]

    return ranges

def max_horizontal_pixel(row_array):
    max_horizontal = len(row_array)

    if is_trim_edge_pixels(len(row_array)):
        max_horizontal = len(row_array) - HORIZONTAL_OFFSET

    return max_horizontal

def min_horizontal_pixel(row_array):
    min_horizontal = 0

    if is_trim_edge_pixels(len(row_array)):
        min_horizontal = HORIZONTAL_OFFSET

    return min_horizontal


def is_trim_edge_pixels(length):
    return len(row_array) > (2 * HORIZONTAL_OFFSET + MIN_SAMPLE_AREA)
