"""Solutions for Day 01 of Advent of Code 2019

https://adventofcode.com/2019/day/01
"""

def part1(inputs = None):
    """Output the answer to part 1 - """
    nums = [int(x) for x in inputs.splitlines()]
    incs = 0
    for previous, current in zip(nums, nums[1:]):
            incs += 1 if current > previous else 0
    print(f'Part 1 answer: {incs}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    nums = [int(x) for x in inputs.splitlines()]
    windows = []
    for a, b, c in zip(nums, nums[1:], nums[2:]):
        windows.append(a + b + c)
    incs = 0
    for previous, current in zip(windows, windows[1:]):
            incs += 1 if current > previous else 0
    print(f'Part 2 answer: {incs}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day01input.txt') as file:
        return file.read()

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return """199
200
208
210
200
207
240
269
260
263"""

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """"""

if __name__ == '__main__':
    part1(puzzle_input())
    part2(puzzle_input())
