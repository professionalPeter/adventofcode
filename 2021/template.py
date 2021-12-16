"""Solutions for Day DAY of Advent of Code 2021

https://adventofcode.com/2021/day/DAY
"""

from aoc import Input

def part1(inputs = None):
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {None}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('dayDAYinput.txt')

def test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(test_input().parse_lines())
    part2(test_input().parse_lines())

