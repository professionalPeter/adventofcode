"""Solutions for Day 15 of Advent of Code 2021

https://adventofcode.com/2021/day/15
"""

from aoc import Input
from collections import namedtuple
import heapq

def min_cost(grid, target, memo):
    if target[0] == 0 and target[1] == 0:
        return 0
    if cost := memo.get(target):
        #print(f'used memo {target}')
        return cost
    #print(f'{target}')
    neighbors = [(target[0]-1, target[1]), (target[0], target[1]-1)]
    neighbor_costs = {neighbor:min_cost(grid, neighbor, memo) for neighbor in neighbors if neighbor[0] >= 0 and neighbor[1] >= 0}
    cost = grid[target[1]][target[0]] + min(neighbor_costs.values())
    memo[target] = cost
    return cost

def get_cost(grid, target):
    width = len(grid[0])
    height = len(grid)
    x = target[0] % width
    y = target[1] % height
    cost = grid[y][x]
    assert(target[0] // width < 5 and target[1] // height < 5) # line below only handles a 5x5 grid
    cost += (target[0] // width) + (target[1] // width)
    if cost > 9:
        cost -= 9 
    return cost

PathCost = namedtuple("PathCost", "cost x y")

def get_adjacent(x,y, x_range, y_range):
    #use combinations?
    return [coord for coord in
        [          (x, y-1),
         (x-1, y),             (x+1, y),
                   (x, y+1)]
        if coord[0] in x_range and coord[1] in y_range]

def min_cost_adv(grid, target, tiles):
    travelled = set()
    sorted_next_steps = [PathCost(0, 0, 0)]
    
    x_range = range(len(grid[0]) * tiles)
    y_range = range(len(grid) * tiles)

    while True:
        step = heapq.heappop(sorted_next_steps)
        if step.x == target[0] and step.y == target[1]:
            return step.cost
        neighbors = get_adjacent(step.x, step.y, x_range, y_range)
        for neighbor in neighbors:
            if neighbor not in travelled:
                travelled.add(neighbor)
                heapq.heappush(sorted_next_steps, PathCost(step.cost + get_cost(grid, neighbor), neighbor[0], neighbor[1]))

def part1(inputs = None):
    """Output the answer to part 1 - """
    grid = [list(map(int, line)) for line in inputs]
    target = (len(grid[0])-1, len(grid)-1)
    least_cost_path = min_cost(grid, target, {})
    print(f'Part 1 answer: {least_cost_path}')

def part2(grid):
    """Output the answer to part 2 - """
    """Output the answer to part 1 - """
    tiles = 5
    target = (len(grid[0])*tiles - 1, len(grid)*tiles - 1)
    least_cost_path = min_cost_adv(grid, target, tiles)
    print(f'Part 2 answer: {least_cost_path}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day15input.txt')

def test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    grid = [list(map(int, line)) for line in puzzle_input().parse_lines()]
    part2(grid)

