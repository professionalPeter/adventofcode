"""Solutions for Day 01 of Advent of Code 2021

https://adventofcode.com/2021/day/01
"""
import aoc

def count_increases(int_list, window_size):
    incs = 0
    for previous, current in zip(int_list, int_list[window_size:]):
            incs += 1 if current > previous else 0
    return incs

def part1(inputs = None):
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {count_increases(inputs, 1)}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {count_increases(inputs, 3)}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return aoc.Input.from_file('day01input.txt')

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return aoc.Input.from_data("""199
200
208
210
200
207
240
269
260
263""")

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """"""

if __name__ == '__main__':
    part1(puzzle_input().parse_ints())
    part2(puzzle_input().parse_ints())

