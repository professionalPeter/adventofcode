from itertools import product

# NOTE: This code has hardcoded the instruction length (4) in several places.
# This makes me think that the functions aren't quite split out properly yet.
# For instance, if one piece of code extracts the instruction, then it should
# probably also be responsible for incrementing the counter too since it knows
# how long the instruction was.
from intcode import IntCodeProcessor

def load_program():
    """Load the puzzle input and split it into a list of ints"""
    with open('day2input.txt') as file:
        return [int(x) for x in file.read().rstrip().split(',')]

def part1():
    """Output the answer for part 1"""
    print(f'Part 1 answer: {cpu.execute_program(12, 2)}')

def find_inputs_in_range_for_output(range_end, output):
    """ Returns the first aggregated noun and verb (100 * noun + verb) required to produce
        the given output for nouns and verbs in the range 0 to range_end (not including
        range_end)"""
    for noun, verb in product(range(range_end), range(range_end)):
        result = cpu.execute_program(noun, verb)
        if result == output:
            return noun * 100 + verb
    return None

def part2():
    """Output the answer for part 1"""
    print(f'Part 2 answer: {find_inputs_in_range_for_output(100, 19690720)}')

cpu = IntCodeProcessor(load_program())
part1() # Expected answer: 662703
part2() # Expected answer: 4019
