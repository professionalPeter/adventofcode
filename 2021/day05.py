"""Solutions for Day 05 of Advent of Code 2021

https://adventofcode.com/2021/day/05
"""

from aoc import Input
from collections import defaultdict

def is_vertical(segment):
    return segment[0][0] == segment[1][0] 

def is_horizontal(segment):
    return segment[0][1] == segment[1][1]

def parse_line_segments(line):
    point_strs = line.split(' -> ')
    return [[int(component) for component in components.split(',')] for components in point_strs]
def part1(inputs = None):
    """Output the answer to part 1 - """
    segments = [parse_line_segments(line) for line in inputs]
    vent_map = defaultdict(int)
    for segment in segments:
        if is_horizontal(segment):
            start = segment[0][0]
            end = segment[1][0]
            if start > end:
                start, end = end, start
            for x in range(start, end+1):
                vent_map[x, segment[0][1]] += 1
        elif is_vertical(segment):
            start = segment[0][1]
            end = segment[1][1]
            if start > end:
                start, end = end, start
            for y in range(start, end+1):
                vent_map[segment[0][0], y] += 1
    overlaps = sum(1 for k,v in vent_map.items() if v > 1)
    print(f'Part 1 answer: {overlaps}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    segments = [parse_line_segments(line) for line in inputs]
    vent_map = defaultdict(int)
    for segment in segments:
        if is_horizontal(segment):
            start = segment[0][0]
            end = segment[1][0]
            if start > end:
                start, end = end, start
            for x in range(start, end+1):
                vent_map[x, segment[0][1]] += 1
        elif is_vertical(segment):
            start = segment[0][1]
            end = segment[1][1]
            if start > end:
                start, end = end, start
            for y in range(start, end+1):
                vent_map[segment[0][0], y] += 1
        else:
            x_start = segment[0][0]
            x_end = segment[1][0]
            x_step = 1 if x_start < x_end else -1
            x_end += x_step
            y_start = segment[0][1]
            y_end = segment[1][1]
            y_step = 1 if y_start < y_end else -1
            y_end += y_step
            points = zip(range(x_start, x_end, x_step), range(y_start, y_end, y_step))
            for point in points:
                vent_map[point[0], point[1]] += 1
    overlaps = sum(1 for k,v in vent_map.items() if v > 1)
    print(f'Part 2 answer: {overlaps}')

# I think I can reduce both solutions into a single solution
def part3(inputs = None):
    """Output the answer to part 2 - """
    segments = [parse_line_segments(line) for line in inputs]
    vent_map = defaultdict(int)
    for segment in segments:
        x_start = segment[0][0]
        x_end = segment[1][0]
        x_step = 1 if x_start < x_end else -1
        x_end += x_step
        y_start = segment[0][1]
        y_end = segment[1][1]
        y_step = 1 if y_start < y_end else -1
        y_end += y_step
        print(segment, 'x:', x_start, x_end, x_step, 'y:', y_start, y_end, y_step)
        points = zip(range(x_start, x_end, x_step), range(y_start, y_end, y_step))

        for point in points:
            vent_map[point[0], point[1]] += 1
    print(len(vent_map))
    overlaps = sum(1 for k,v in vent_map.items() if v > 1)
    print(f'Part 3 answer: {overlaps}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day05input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part3(test_input1().parse_lines())
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())
