from itertools import product
from enum import IntEnum

# NOTE: This code has hardcoded the instruction length (4) in several places.
# This makes me think that the functions aren't quite split out properly yet.
# For instance, if one piece of code extracts the instruction, then it should
# probably also be responsible for incrementing the counter too since it knows
# how long the instruction was.

class OpCode(IntEnum):
    ADD = 1
    MULT = 2

def load_program():
    """Load the puzzle input and split it into a list of ints"""
    with open('day2input.txt') as fp:
        return [int(x) for x in fp.read().rstrip().split(',')]

def extract_instruction(memory, instruction_pointer):
    """Extract the instruction at the instruction pointer"""
    return memory[instruction_pointer:instruction_pointer+4]

def execute_instruction(memory, instruction):
    """Execute the given instruction"""
    opcode = instruction[0]
    parameters = instruction[1:]
    if opcode == OpCode.ADD:
        memory[parameters[2]] = memory[parameters[0]] + memory[parameters[1]]
    elif opcode == OpCode.MULT: 
        memory[parameters[2]] = memory[parameters[0]] * memory[parameters[1]]
    else:
        raise ValueError(f'{opcode} is not a supported opcode')

def execute_program(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb
    instruction_pointer = 0
    while memory[instruction_pointer] != 99:
        instruction = extract_instruction(memory, instruction_pointer)
        execute_instruction(memory, instruction)
        instruction_pointer += 4
    return memory[0]

def part1():
    """Output the answer for part 1"""
    memory = load_program()
    print(f'Part 1 answer: {execute_program(memory, 12, 2)}')

def find_inputs_in_range_for_output(range_end, output):
    """ Returns the first aggregated noun and verb (100 * noun + verb) required to produce
        the given output for nouns and verbs in the range 0 to range_end (not including 
        range_end)"""
    initial_memory = load_program()
    for noun, verb in product(range(range_end), range(range_end)):
        memory = initial_memory.copy()
        result = execute_program(memory, noun, verb)
        if result == output:
            return noun * 100 + verb

def part2():
    print(f'Part 2 answer: {find_inputs_in_range_for_output(100, 19690720)}')

part1()
part2()
