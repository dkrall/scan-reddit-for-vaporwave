#!/usr/bin/env python3
import os
import sys
from config import config_horizontal_search
import numpy as np
from PIL import Image

RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2

#arr_averages_by_four_corners_ten_pixels = []
#arr_averages_by_four_corners_forty_pixels = []
#arr_averages_by_fiftieth_horizonal_row = []
#arr_averages_by_ten_pixels = []
#arr_averages_by_hundred_pixels = []

def main():
    argv = sys.argv
    general_instructions = 'Command was formatted incorrectly! Please use the following format: "./compile_stats_for_ideal_vaporwave_images.py corners 10", "./compile_stats_for_ideal_vaporwave_images.py skip 10", or "./compile_stats_for_ideal_vaporwave_images.py horizontal 50"'
    int_param = -1
    function_keyword = argv[1]

    if len(argv) > 2:
        int_param = parse_int_if_allowed(argv[2])

    if int_param < 0:
        print(general_instructions)
        print('Second parameter must be a valid integer greater than 0. Invalid integer was provided.')
        return

    match function_keyword:
        case 'corners':
            arr_averages_by_four_corners(int_param)
        case 'skip':
            arr_averages_by_skip(int_param)
        case 'horizontal':
            arr_averages_by_horizontal(int_param)
        case default:
            print(general_instructions)
            return


def parse_int_if_allowed(param_string):
    try:
        return(int(param_string))
    except:
        return(-1)


def arr_averages_by_horizontal(int_param):
    dir_name = './ideal_vaporwave_images'
    all_stats = []
    for filename in os.listdir(dir_name):
        initial_img = Image.open(dir_name + '/' + filename)

        # The following two lines ensure that three color values are present, regardless of the
        # image format
        img = Image.new('RGBA', initial_img.size)
        img.paste(initial_img)

        image_array = np.array(img)

        height = image_array.shape[0]
        width = image_array.shape[1]

        # so for instance if the param is 50, we fetch the 50th row
        sample_pixels = image_array[int_param]

        stats = get_array_stats(sample_pixels)
        #print_stats(filename, stats)
        print_verdict(filename, stats)
        all_stats.append(stats)

    stats = aggregate_stats_for_multiple_files(all_stats)
    #print_stats('aggregate of all files', stats)


def arr_averages_by_four_corners(int_param):
    print('This function is not yet implemented!')


def arr_averages_by_skip(int_param):
    print('This function is not yet implemented!')


def print_stats(filename, stats):
    print('For ' + filename + ', the following stats were observed:')
    color_names = ['Red', 'Green', 'Blue']
    stat_keys = ['max', 'mins', 'avgs']
    for color in [0, 1, 2]:
        for key in stat_keys:
            print(str(color_names[color]) + ' ' + key + ': ' + str(stats[key][color]))
    print('')


def print_verdict(filename, stats):
    MIN_INDEX = 0
    MAX_INDEX = 1

    ranges = config_horizontal_search()
    verdict = True
    verdict_string = "Fails"

    for color in [RED_INDEX, GREEN_INDEX, BLUE_INDEX]:
        min = ranges[color][MIN_INDEX]
        max = ranges[color][MAX_INDEX]
        verdict = verdict and min < stats['avgs'][color] and max > stats['avgs'][color]

    if verdict:
        verdict_string = "Passes"

    print(filename + ': ' + verdict_string)


def aggregate_stats_for_multiple_files(stats):
    sums = [0, 0, 0]
    max = [0, 0, 0]
    mins = [999, 999, 999]
    avgs = [0, 0, 0]

    for file_stats in stats:
        for color in [0, 1, 2]:
            sums[color] += file_stats['avgs'][color]

            if file_stats['max'][color] > max[color]:
                max[color] = file_stats['max'][color]

            if file_stats['mins'][color] < mins[color]:
                mins[color] = file_stats['mins'][color]

    for color in [0, 1, 2]:
        avgs[color] = sums[color] / len(stats)

    stats = {
        'max': max,
        'mins': mins,
        'avgs': avgs
    }

    return(stats)


# Takes a one-dimensional array of tuples (first key is pixel number, second is color) as a parameter and iterates through it, returning
# a dicts with the max, min, and average values for R, G, and B color dimensions.
def get_array_stats(sample_pixels):

    sums = [0, 0, 0]
    max = [0, 0, 0]
    mins = [999, 999, 999]
    avgs = [0, 0, 0]

    #print(sample_pixels)
    for pixel in sample_pixels:
        for color in [0, 1, 2]:
            sums[color] = sums[color] + pixel[color]

            if pixel[color] > max[color]:
                max[color] = pixel[color]

            if pixel[color] < mins[color]:
                mins[color] = pixel[color]

    for color in [0, 1, 2]:
        avgs[color] = sums[color] / len(sample_pixels)

    stats = {
        'max': max,
        'mins': mins,
        'avgs': avgs
    }

    return(stats)


if __name__ == "__main__":
    main()
