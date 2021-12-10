"""Solutions for Day 10 of Advent of Code 2021

https://adventofcode.com/2021/day/10
"""

from aoc import Input

def part1(inputs = None):
    """Output the answer to part 1 - """
    ENDINGS = {'{':'}', '[':']', '(':')', '<':'>' }
    stack = []
    line = inputs[2]
    for char in line:
        if ENDINGS.get(char):
            stack.append(ENDINGS[char])
        elif char in ENDINGS.values():
            match = stack.pop()
            if match != char:
                fail_char = char
                break
    print(f'Part 1 answer: {fail_char}')




def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

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
    part1(test_input1().parse_lines())
    part2(test_input2().parse_lines())

