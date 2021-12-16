"""Solutions for Day 15 of Advent of Code 2021

https://adventofcode.com/2021/day/15
"""

from aoc import Input
from itertools import product

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

def get_location_cost(grid, target):
    #todo memo these too
    x = target[0] % 10
    y = target[1] % 10
    cost = grid[y][x]
    assert(target[0] // 10 < 5 and target[1] // 10 < 5) # line below only handles a 5x5 grid
    cost += (target[0] // 10) + (target[1] // 10)
    if cost > 9:
        cost -= 9 
    return cost

def min_cost_with_start(grid, start, target, memo):
    if start == target:
        return get_location_cost(grid, start)
    if cost := memo.get(target):
        #print(f'used memo {target}')
        return cost
    #print(f'{target}')
    min_x = (start[0] // 10) * 10
    min_y = (start[1] // 10) * 10
    neighbors = [(target[0]-1, target[1]), (target[0], target[1]-1)]
    neighbor_costs = {neighbor:min_cost_with_start(grid, start, neighbor, memo) for neighbor in neighbors if neighbor[0] >= min_x and neighbor[1] >= min_y}
    min_neighbor_cost = min(neighbor_costs.values()) if len(neighbor_costs) > 0 else 0
    cost = get_location_cost(grid, target) + min_neighbor_cost
    memo[(start,target)] = cost
    return cost

def min_costs_through_tile(grid, tile_x, tile_y, memo):
    # min cost of top edge
    tile_start_x = tile_x * 10
    tile_start_y = tile_y * 10
    tile_end_x = tile_start_x + len(grid[0]) - 1
    tile_end_y = tile_start_y + len(grid) - 1
        
    entries = [(tile_start_x, tile_start_y + y) for y in range(len(grid))] + [(tile_start_x + x, tile_start_y) for x in range(len(grid[0]))]
    exits = [(tile_end_x, tile_start_y + y) for y in range(len(grid))] + [(tile_start_x + x, tile_end_y) for x in range(len(grid[0]))]
    print(entries)
    print(exits)
    paths = list(product(entries, exits))
    print(len(paths))
    for start, end in paths:
        min_cost_with_start(grid, start, end, memo)

def min_cost_adv(grid, target, memo):
    if target[0] == 0 and target[1] == 0:
        return 0
    if cost := memo.get(target):
        #print(f'used memo {target}')
        return cost
    #print(f'{target}')
    neighbors = [(target[0]-1, target[1]), (target[0], target[1]-1)]
    neighbor_costs = {neighbor:min_cost_adv(grid, neighbor, memo) for neighbor in neighbors if neighbor[0] >= 0 and neighbor[1] >= 0}
    x = target[0] % 10
    y = target[1] % 10
    cost_delta = (target[0] // 10) + (target[1] // 10)
    cost = grid[y][x] + cost_delta
    if cost > 9:
        cost -= 9 
    cost += min(neighbor_costs.values())
    memo[target] = cost
    return cost

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
    least_cost_path = min_cost_adv(grid, target, {})
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
    grid = [list(map(int, line)) for line in test_input().parse_lines()]
    part1(puzzle_input().parse_lines())
    part2(grid)
    min_costs_through_tile(grid, 0, 0, {})

