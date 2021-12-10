"""Solutions for Day 09 of Advent of Code 2021

https://adventofcode.com/2021/day/09
"""

from aoc import Input
from collections import namedtuple, defaultdict

CavePos = namedtuple("CavePos", "x y height")


def safe_get(list_, index, default):
    return list_[index] if index >= 0 and index < len(list_) else default

def part1(inputs = None):
    """Output the answer to part 1 - """
    lows = []
    grid = []
    for y, line in enumerate(inputs):
        int_line = [int(x) for x in line]
        grid.append(int_line)
        lows += [CavePos(x,y, height) for x, height in enumerate(int_line) if height < safe_get(int_line, x-1, 99) and height < safe_get(int_line, x+1, 99)]
    risk_levels = [cave_pos.height+1 for cave_pos in lows if (cave_pos.y-1 < 0 or cave_pos.height < grid[cave_pos.y-1][cave_pos.x]) and (cave_pos.y+1 >= len(grid) or cave_pos.height < grid[cave_pos.y+1][cave_pos.x])]
    print(f'Part 1 answer: {sum(risk_levels)}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    last_basin = -1
    prev_line = ['9'] * len(inputs[0])
    print(prev_line)
    basin_sizes = defaultdict(int)
    curr_line_basins = []
    for y, line in enumerate(inputs):
        for x, height in enumerate(line):
            if height == '9':
                curr_line_basins.append(None)
                continue
            if x == 0 or line[x-1] == '9':
                last_basin += 1
                print("New Basin: ", last_basin, "at ", x, ",", y)
            if prev_line[x] != None:
                print(f'prev[{x}] = {prev_line[x]}')
                print(f"Merging: {prev_line[x]}:{basin_sizes[prev_line[x]]} into {last_basin}:{basin_sizes[last_basin]} at {x},{y}")
                basin_sizes[last_basin] += basin_sizes[prev_line[x]]
                basin_sizes[prev_line[x]] = 0
            basin_sizes[last_basin] += 1
            #print(f'basin {last_basin} = {basin_sizes[last_basin]}')
            curr_line_basins.append(last_basin)
        prev_line = curr_line_basins
    basin_sizes ={k:v for k,v in basin_sizes.items() if v >0}
    print(f'Part 2 answer: {basin_sizes}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day09input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""2199943210
3987894921
9856789892
8767896789
9899965678""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(test_input1().parse_lines())

