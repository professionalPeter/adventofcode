"""Solutions for Day 8 of Advent of Code 2019

https://adventofcode.com/2019/day/8
"""
from collections import Counter
from itertools import dropwhile
from utils import split_by_size

def part1(pixels, pixel_width, pixel_height):
    """Output the answer to part 1 - """
    layers = split_by_size(pixels, pixel_width * pixel_height)
    layer_counts = [Counter(layer) for layer in layers]
    layer_zero_counts = [counts['0'] for counts in layer_counts]
    min_layer_index = layer_zero_counts.index(min(layer_zero_counts))
    min_layer_counter = layer_counts[min_layer_index]
    print(f"Part 1 answer: {min_layer_counter['1'] * min_layer_counter['2'] }")

def part2(pixels, pixel_width, pixel_height):
    """Output the answer to part 2 - """

    # Split the pixels into layers
    layers = split_by_size(pixels, pixel_width * pixel_height)

    # Group the pixels into groups of pixels that are on top of each other when the layers are stacked
    pixel_stacks = list(zip(*layers))

    # 2's are transparent pixels, so find the first pixel in each stack that isn't transparent
    visible_pixels = [list(dropwhile(lambda p: p == '2', stack))[0] for stack in pixel_stacks]

    # Transform the pixels into characters that will print nicely
    block_pixels = [u'\u25a0' if pixel == '1' else u'\u25a1' for pixel in visible_pixels]

    # Group the pixels into rows
    pixel_rows = split_by_size(block_pixels, pixel_width)

    # Join all the characters in each row into a single string
    joined_pixel_rows = [''.join(row) for row in pixel_rows]
    print('Part 2 answer:', *joined_pixel_rows, sep = '\n')
    return layers, pixel_stacks, visible_pixels

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day08input.txt') as file:
        return file.read().rstrip()

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return '123456789012'

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return '0222112222120000'

if __name__ == '__main__':
    part1(puzzle_input(), 25, 6)
    part2(puzzle_input(), 25, 6)

