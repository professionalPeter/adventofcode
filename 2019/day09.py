"""Solutions for Day 9 of Advent of Code 2019

https://adventofcode.com/2019/day/9
"""
from intcode import IntCodeProcessor

def part1():
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {IntCodeProcessor(path = "day09input.txt").execute_program(1)}')

def part2():
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {IntCodeProcessor(path = "day09input.txt").execute_program(2)}')

if __name__ == '__main__':
    part1()
    part2()
