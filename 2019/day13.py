"""Solutions for Day 13 of Advent of Code 2019

https://adventofcode.com/2019/day/13
"""
from intcode import IntCodeProcessor, ExecutionError, ExecutionCode
from utils import split_by_size

BLOCK = 2
PADDLE = 3
BALL = 4

def part1(inputs = None):
    """Output the answer to part 1 - """
    cpu = IntCodeProcessor(path='day13input.txt')
    output = cpu.execute_program()
    block_count = sum([1 for instruction in output[2::3] if instruction == BLOCK])
    print(f'Part 1 answer: {block_count}')

def part2():
    """Output the answer to part 2 - What's the final score"""

    program = IntCodeProcessor.load_program('day13input.txt')
    program[0] = 2
    cpu = IntCodeProcessor(program)
    result = None
    next_input = None
    ball_pos = None
    paddle_pos = None
    score = None
    while result is None:
        try:
            result = cpu.execute_program(next_input, reset=False)
        except ExecutionError as err:
            assert err.reason == ExecutionCode.NEED_INPUT

        ball_pos, paddle_pos, score = process_output(cpu.outputs, ball_pos, paddle_pos, score)
        cpu.outputs = []
        next_input = next_input_for(ball_pos, paddle_pos)
    print(f'Part 2 answer: {score}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day13input.txt') as file:
        return file.read()

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return """"""

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """"""

def next_input_for(ball_pos, paddle_pos):
    if ball_pos[0] == paddle_pos[0]:
        return 0
    elif ball_pos[0] > paddle_pos[0]:
        return 1
    else:
        return -1

def process_output(output, ball_pos, paddle_pos, score):
    for instr in split_by_size(output, 3):
        if instr[0] == -1 and instr[1] == 0:
            score = instr[2]
        elif instr[2] == BALL:
            ball_pos = (instr[0], instr[1])
        elif instr[2] == PADDLE:
            paddle_pos = (instr[0], instr[1])
    return ball_pos, paddle_pos, score

if __name__ == '__main__':
    part1()
    part2()
