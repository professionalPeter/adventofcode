"""Solutions for Day 7 of Advent of Code 2019

https://adventofcode.com/2019/day/7
"""
from intcode import IntCodeProcessor, ExecutionError
from itertools import permutations
import logging

def part1(program = None):
    """Output the answer to part 1 - """
    phase_setting_groups = permutations(range(5))
    thruster_signal = []
    for phase_settings in phase_setting_groups:
        output = generate_thruster_signal(program, phase_settings)
        thruster_signal.append(output)
    output = max(thruster_signal)

    print(f'Part 1 answer: {output}')

def part2(program = None):
    """Output the answer to part 2 - """
    program = puzzle_input()
    phase_setting_groups = permutations(range(5,10))
    thruster_signal = []
    for phase_settings in phase_setting_groups:
        result = generate_thruster_signal_part2(program, phase_settings)
        thruster_signal.append(result)

    print(f'Part 2 answer: {max(thruster_signal)}')

def generate_thruster_signal(program, phase_settings):
    cpu = IntCodeProcessor(program)
    signal = 0
    for phase in phase_settings:
        signal = cpu.execute_program([phase, signal])[0]
    return signal 

def generate_thruster_signal_part2(program, phase_settings):
    cpus = [IntCodeProcessor(program) for _ in range(5)]
    for index, phase in enumerate(phase_settings):
        try:
            logging.debug(f'CPU {index} - initialize')
            cpus[index].execute_program([phase])
        except ExecutionError:
            pass
    cpu_index = 0
    next_input = [0]
    while True:
        try:
            logging.debug(f'CPU {cpu_index} - start')
            result = cpus[cpu_index].execute_program(next_input, False)
            if result is not None:
                if cpu_index == 4:
                    break
                else:
                    next_input = cpus[cpu_index].outputs
                    cpus[cpu_index].outputs = []
        except ExecutionError:
            next_input = cpus[cpu_index].outputs
            cpus[cpu_index].outputs = []
        cpu_index = (cpu_index+1) % 5
    return result
    
def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day07input.txt') as file:
        return file.read().rstrip().split(',')

def part1_test_input():
    """Returns the test data set from the description of part 1"""

    return [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

if __name__ == '__main__':
    part1(puzzle_input())
    part2(puzzle_input())
