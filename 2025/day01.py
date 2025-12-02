"""Solutions for Day 01 of Advent of Code 2025

https://adventofcode.com/2025/day/1
"""

from aoc import Input

def transform_input_to_rotations( inputs ):
    return [int(x[1:]) * (1 if x[0] == 'R' else -1) for x in inputs]

def did_hit_zero( start, end ):
    if end == 0:
        return True
    elif start < 0:
        return end > 0
    elif start > 0:
        return end < 0
    else: # start == 0
        return False


def part1(inputs = None):
    """Output the answer to part 1 - """
    rotations = transform_input_to_rotations(inputs)
    dial = 50
    zeros = 0
    for rot in rotations:
        dial = (dial + rot) % 100
        print(dial)
        if dial == 0:
           zeros += 1 
    print(f'Part 1 answer: {zeros}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    rotations = transform_input_to_rotations(inputs)
    unclamped_dial = 50
    dial = 50
    zeros = 0
    for rot in rotations:
        mag = abs(rot)
        zeros += mag // 100

        rot_remainder = mag % 100
        unclamped_dial = dial + (rot_remainder if rot >= 0 else -rot_remainder)
        if dial != 0 and (unclamped_dial >= 100 or unclamped_dial <= 0):
            zeros += 1

        if unclamped_dial < 0:
            dial = unclamped_dial + 100
        else:
            dial = unclamped_dial % 100

        print(dial, rot, rot_remainder, unclamped_dial, zeros )
    print(f'Part 2 answer: {zeros}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day01input.txt')

def test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())
