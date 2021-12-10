"""Solutions for Day 07 of Advent of Code 2021

https://adventofcode.com/2021/day/07
"""

from aoc import Input

def compute_target_position(crab_positions, fuel_cost_function):
    low = min(crab_positions)
    hi = max(crab_positions)
    fuel_costs = [sum([fuel_cost_function(crab, target) for crab in crab_positions]) for target in range(low, hi+1)]
    return min(fuel_costs)


def part1(inputs = None):
    """Output the answer to part 1 - """
    fuel_cost = compute_target_position(inputs, lambda a, b: abs(a-b))
    print(f'Part 1 answer: {fuel_cost}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    fuel_function = lambda a, b: int((abs(a-b) * (abs(a-b)+1))/2)
    fuel_cost = compute_target_position(inputs, fuel_function)
    print(f'Part 2 answer: {fuel_cost}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day07input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""16,1,2,0,4,2,7,1,2,14""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_ints(','))
    part2(puzzle_input().parse_ints(','))

