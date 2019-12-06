from itertools import product
from intcode import IntCodeProcessor

def part1():
    """Output the answer for part 1"""
    print(f'Part 1 answer: {cpu.execute_program_with_inputs(12, 2)}')

def find_inputs_in_range_for_output(range_end, output):
    """ Returns the first aggregated noun and verb (100 * noun + verb) required to produce
        the given output for nouns and verbs in the range 0 to range_end (not including
        range_end)"""
    for noun, verb in product(range(range_end), range(range_end)):
        result = cpu.execute_program_with_inputs(noun, verb)
        if result == output:
            return noun * 100 + verb
    return None

def part2():
    """Output the answer for part 1"""
    print(f'Part 2 answer: {find_inputs_in_range_for_output(100, 19690720)}')

cpu = IntCodeProcessor(path = 'day02input.txt')
part1() # Expected answer: 662703
part2() # Expected answer: 4019
