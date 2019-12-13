"""Solutions for Day 11 of Advent of Code 2019

https://adventofcode.com/2019/day/11
"""
from enum import IntEnum
from intcode import IntCodeProcessor, ExecutionError, ExecutionCode
import logging

logging.basicConfig(level=logging.INFO)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'({self.x},{self.y})'
    def __str__(self):
        return f'Point({self.x},{self.y})'
    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y
    def __key(self):
        return (self.x, self.y)
    def __hash__(self):
        return hash(self.__key())


def part1():
    """Output the answer to part 1 - """
    cpu = IntCodeProcessor(path='day11input.txt')

    heading = (0,1)
    path = [(0,0)]
    paint = {}
    result = None
    next_input = None

    while result is None:
        try:
            result = cpu.execute_program(next_input, reset = False)
        except ExecutionError as err:
            assert err.reason == ExecutionCode.NEED_INPUT
            pass

        output_count = len(cpu.outputs)
        assert output_count == 2 or output_count == 0
        if output_count == 2:
            new_color = cpu.outputs.pop(0)
            turn = cpu.outputs.pop(0)
            heading = step_robot(new_color, turn, path, heading, paint)
        next_input = paint.get(path[-1], 0)
    print(f'Part 1 answer: {len(paint)}')

def part2():
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

def rotate(point, right):
    '''Rotate point by 90 degrees

    Rotate left if the second argument is falsy, and right if the second argument is truthy
    '''
    return (point[1], -point[0]) if right else (-point[1], point[0])

def step_robot(paint_command, move_command, path, heading, paint):
    location = path[-1]
    paint[location] = paint_command
    new_heading = rotate(heading, move_command)
    path.append((location[0] + new_heading[0], location[1] + new_heading[1]))
    return new_heading

if __name__ == '__main__':
    #part1()
    part2()

    cpu = IntCodeProcessor(path='day11input.txt')
    heading = (0,1)
    path = [(0,0)]
    paint = {}
    result = None
    next_input = 1

    while result is None:
        try:
            result = cpu.execute_program(next_input, reset = False)
        except ExecutionError as err:
            assert err.reason == ExecutionCode.NEED_INPUT
            pass

        output_count = len(cpu.outputs)
        assert output_count == 2 or output_count == 0
        if output_count == 2:
            new_color = cpu.outputs.pop(0)
            turn = cpu.outputs.pop(0)
            heading = step_robot(new_color, turn, path, heading, paint)
        next_input = paint.get(path[-1], 0)

    s = {}
    for loc, color in paint.items():
        s.setdefault(loc[1], []).append((loc[0], color))
    s = {k:sorted(v) for k,v in s.items()}
    g = {k:[' ' if p[1] == 0 else '#' for p in v] for k,v in s.items()}
    g[-5].insert(0,' ')
    g[-2].insert(0,' ')
    g[-1].insert(0,' ')
    for k in sorted(g.keys(),reverse=True):
        row = (' ' if g[k][0] == 1 else '').join(g[k])
        print(row)
