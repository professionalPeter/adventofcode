"""Solutions for Day 03 of Advent of Code 2021

https://adventofcode.com/2021/day/03
"""
from aoc import Input
import operator

def compute_most_common_bits(binary_strings):
    bit_counts = [0] * len(binary_strings[0])
    for line in binary_strings:
        for idx, character in enumerate(line):
            bit_counts[idx] += 1 if character == '1' else -1
    return [1 if bit >= 0 else 0 for bit in bit_counts]

def part1(inputs = None):
    """Output the answer to part 1 - """
    most_common_bits = compute_most_common_bits(inputs)
    binaryString = '0b' + ''.join([str(bit) for bit in most_common_bits])
    gamma = int(binaryString, 2)
    epsilon = 2 ** len(inputs[0]) - 1 - gamma
    print(f'Part 1 answer: {gamma * epsilon}')

def compute_life_support_rating(inputs, op):
    remaining_values = inputs
    for index in range(len(inputs[0])):
        if len(remaining_values) > 1:
            most_common_bits = compute_most_common_bits(remaining_values)
            remaining_values = [val for val in remaining_values if op(int(val[index]), most_common_bits[index])]
    return int('0b' + ''.join(remaining_values), 2)

def part2(inputs = None):
    """Output the answer to part 2 - """
    oxygen = compute_life_support_rating(inputs, operator.eq)
    co2 = compute_life_support_rating(inputs, operator.ne)
    print(f'Part 2 answer: {oxygen * co2}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day03input.txt')

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""")

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    from collections import Counter
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())

