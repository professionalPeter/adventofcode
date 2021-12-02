"""Solutions for Day 02 of Advent of Code 2021

https://adventofcode.com/2021/day/02
"""
from aoc import Input

COMMAND_MAP = {
    "forward" : 1+0j,
    "down"    : 0+1j,
    "up"      : 0-1j
}

def parse_command(cmd):
    name, magnitude = cmd.split()
    return int(magnitude) * COMMAND_MAP[name]

def format_answer(horizontal, depth):
    return int(horizontal * depth)

def part1(inputs = None):
    """Output the answer to part 1 - """
    answer = sum([parse_command(cmd) for cmd in inputs])
    print(f'Part 1 answer: {format_answer(answer.real, answer.imag)}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    commands = [parse_command(cmd) for cmd in inputs]
    depth = 0
    horiz_pos_and_aim = 0+0j
    for cmd in commands:
        horiz_pos_and_aim += cmd
        depth += cmd.real * horiz_pos_and_aim.imag
    print(f'Part 2 answer: {format_answer(horiz_pos_and_aim.real, depth)}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day02input.txt')

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""forward 5
down 5
forward 8
up 3
down 8
forward 2""")

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """"""

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())

