"""Solutions for Day 13 of Advent of Code 2021

https://adventofcode.com/2021/day/13
"""

from aoc import Input
from collections import namedtuple

Point = namedtuple("Point", "x y")
Fold = namedtuple("Fold", "axis distance")

def make_point(definition):
    x, y = definition.split(',')
    return Point(int(x), int(y))

def make_fold(definition):
    axis, distance = definition.split('=')
    return Fold(axis[-1], int(distance))

def fold_point(point, fold):
    if fold.axis == 'y':
        return point if point.y < fold.distance else Point(point.x, 2*fold.distance - point.y)
    else:
        return point if point.x < fold.distance else Point(2*fold.distance - point.x, point.y)

def part1(inputs = None):
    """Output the answer to part 1 - """
    dot_coords = set([make_point(line) for line in inputs[0]])
    folds = [make_fold(line) for line in inputs[1]]
    
    dot_coords = set([fold_point(point, folds[0]) for point in dot_coords])
    
    print(f'Part 1 answer: {len(dot_coords)}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    dot_coords = set([make_point(line) for line in inputs[0]])
    folds = [make_fold(line) for line in inputs[1]]
    
    for fold in folds:
        dot_coords = set([fold_point(point, fold) for point in dot_coords])
    
    size_x = max(dot_coords, key = lambda p: p.x).x + 1
    size_y = max(dot_coords, key = lambda p: p.y).y + 1
    grid = [[' '] * size_x for _ in range(size_y)]
    for point in dot_coords:
        grid[point.y][point.x] = '#'
    output = '\n'.join([''.join(line) for line in grid])
    
    print(f'Part 2 answer: \n{output}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day13input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_records())
    part2(puzzle_input().parse_records())

