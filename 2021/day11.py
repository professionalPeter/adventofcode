"""Solutions for Day 11 of Advent of Code 2021

https://adventofcode.com/2021/day/11
"""

from aoc import Input

def get_adjacent(x,y, grid):
    #use combinations?
    width = len(grid[0])
    height = len(grid)
    return [coord for coord in
        [(x-1, y-1), (x, y-1), (x+1, y-1),
         (x-1, y),             (x+1, y),
         (x-1, y+1), (x, y+1), (x+1, y+1)]
        if coord[0] >= 0 and coord[0] < width and coord[1] >= 0 and coord[1] < height]

def print_grid(grid, label):
    print(label)
    for line in grid:
        print(''.join([str(i) for i in line]))
    print('\n')

def energize(x, y, grid):
    grid[y][x] += 1
    return grid[y][x] == 10

def step(grid):
    new_flashed = set()
    for y, line in enumerate(grid):
        for x, level in enumerate(line):
            if energize(x, y, grid):
                new_flashed.add((x, y))

    all_flashed = set()
    while current := new_flashed.pop() if new_flashed else False:
        adjacent = get_adjacent(current[0], current[1], grid)
        for adjacent_x, adjacent_y in adjacent:
            if ((adjacent_x, adjacent_y) not in all_flashed) and energize(adjacent_x, adjacent_y, grid):
                new_flashed.add((adjacent_x,adjacent_y))
        grid[current[1]][current[0]] = 0
        all_flashed.add(current)
    return len(all_flashed)

def part1(inputs = None):
    """Output the answer to part 1 - """
    grid = [[int(x) for x in line] for line in inputs]

    flash_count = 0
    for i in range(0,100):
        flash_count += step(grid)

    print(f'Part 1 answer: {flash_count}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    grid = [[int(x) for x in line] for line in inputs]
    grid_size = len(grid) * len(grid[0])

    flash_count = 0
    step_count = 0
    while flash_count != grid_size:
        flash_count = step(grid)
        step_count += 1
        #print_grid(grid, f'===={step_count}====')

    print(f'Part 2 answer: {step_count}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day11input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())

