"""Solutions for Day 17 of Advent of Code 2019

https://adventofcode.com/2019/day/17
"""
from intcode import IntCodeProcessor, ExecutionError, ExecutionCode

def part1():
    """Output the answer to part 1 - Determine the alignment parameter from the number of intersections in the map"""
    camera_output = IntCodeProcessor(path='day17input.txt').execute_program()
    camera_output = ints_to_string(camera_output)
    grid = camera_output.splitlines()

    scaffolds = set()
    for row_index, row in enumerate(grid):
        for col_index, element in enumerate(row): 
            if element == '#':
                scaffolds.add((row_index,col_index))

    intersections = [loc for loc in scaffolds if set(locations_adjacent_to(loc)) <= scaffolds]
    parameters = [loc[0] * loc[1] for loc in intersections]

    print(f'Part 1 answer: {sum(parameters)}')

def part2():
    """Output the answer to part 2 - Provide the commands to the robot to follow the path without falling off, then find the resulting output value from the robot

    If the robot falls off, then a map showing the location where it fell off is printed.
    """
    commands = ['A,A,B,C,B,A,C,B,C,A',
                'L,6,R,12,L,6,L,8,L,8',
                'L,6,R,12,R,8,L,8',
                'L,4,L,4,L,6',
                'n']

    cpu = IntCodeProcessor(path='day17input.txt', overrides = [2])
    result = cpu.execute_program(input_channel = compile_commands(commands))

    if result[-2:] == [10,10]:
        print_map(result)
    else:
        print(f'Part 2 answer: {result[-1]}')

def ints_to_string(iterable):
    """Transform a list of ints into the ASCII string they represent"""
    return ''.join([chr(i) for i in iterable])

def locations_adjacent_to(loc):
    """Return the locations adjacent to the given location

    Adjacent is defined as north, south, west, and east (i.e. no diagonals)
    """
    return [(loc[0] + direction[0], loc[1] + direction[1]) for direction in [(0,-1),(0,1),(-1,0),(1,0)]]

def compile_commands(commands):
    """Transform a list command strings into ASCII input to the vacuum robot

    A single command is a string of comma-separated characters. No newline is expected to end each line.
    """
    return [ord(char) for char in ''.join([c + '\n' for c in commands])]

def print_map(ascii_map):
    """Print the vacuum robot's output as an ASCII map"""
    print(ints_to_string(ascii_map))

if __name__ == '__main__':
    part1()
    part2()


