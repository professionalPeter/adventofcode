"""Solutions for Day 10 of Advent of Code 2021

https://adventofcode.com/2021/day/10
"""

from aoc import Input
from functools import reduce
from statistics import median

ENDINGS = {'{':'}', '[':']', '(':')', '<':'>' }

def find_illegal_char(line):
    stack = []
    for char in line:
        if ENDINGS.get(char):
            stack.append(ENDINGS[char])
        elif char in ENDINGS.values():
            match = stack.pop()
            if match != char:
                return char
    return None

def find_incomplete_chars(line):
    stack = []
    for char in line:
        if ENDINGS.get(char):
            stack.append(ENDINGS[char])
        elif char in ENDINGS.values():
            match = stack.pop()
            assert(match == char)
    return stack

def part1(inputs = None):
    """Output the answer to part 1 - """
    POINTS = { ')':3, ']':57, '}':1197, '>':25137 }
    answer = 0
    for line in inputs:
        if fail_char := find_illegal_char(line):
            answer += POINTS[fail_char]
    print(f'Part 1 answer: {answer}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    POINTS = { ')':1, ']':2, '}':3, '>':4 }
    incomplete_lines = [line for line in inputs if find_illegal_char(line) is None]
    scores = []
    for line in incomplete_lines:
        scores.append(reduce(lambda acc, element: acc * 5 + POINTS[element], reversed(find_incomplete_chars(line)), 0))
    print(f'Part 2 answer: {median(scores)}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day10input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())

