"""Solutions for Day 17 of Advent of Code 2021

https://adventofcode.com/2021/day/17
"""

from aoc import Input
from math import sqrt, ceil, floor
import re

def solve_quadratic(v, d):
    b = 2*v+1
    radicand = b**2 - 8*d
    if radicand < 0:
        return None
    return (b - sqrt(radicand))/2, (b + sqrt(radicand))/2

def part1(inputs = None):
    """Output the answer to part 1 - """
    match = re.search('.*x=(.*)\.\.(.*), y=(.*)\.\.(.*)', inputs)
    target_min_x = int(match.group(1))
    target_max_x = int(match.group(2))
    target_min_y = int(match.group(3))
    target_max_y = int(match.group(4))

    # max height is achieved by using the max velocity
    # Since upward launch will return to 0 height with the same velocity as it
    # was launched, then the max velocity is the one where the step after the
    # return to 0 will hit the last row of the target
    max_vy = -target_min_y - 1
    max_height = (max_vy * (max_vy + 1))/2

    print(f'Part 1 answer: {max_height}')

def part2(inputs = None):
    match = re.search('.*x=(.*)\.\.(.*), y=(.*)\.\.(.*)', inputs)
    target_min_x = int(match.group(1))
    target_max_x = int(match.group(2))
    target_min_y = int(match.group(3))
    target_max_y = int(match.group(4))
    
    min_vy = target_min_y
    max_vy = -target_min_y - 1
    #min_vx = ceil((-1 + sqrt(8 * target_min_x + 1))/2)
    min_vx = ceil(-solve_quadratic(0,-target_min_x)[0])
    max_vx = target_max_x
    
    # max possible time is latest time that we can hit the target at the max
    # velocity. We know this is the max time because the max velocity will take
    # the longest to come down
    max_time = floor(solve_quadratic(max_vy, target_min_y)[1])

    vx_candidates = range(min_vx, max_vx+1)
    vy_candidates = range(min_vy, max_vy+1)

    # store the times that can hit the target for each x velocity
    vx_times = {}
    for vx in vx_candidates:
        min_t = ceil(solve_quadratic(vx,target_min_x)[0])
        if max_t := solve_quadratic(vx,target_max_x):
            max_t = floor(max_t[0])
        else:
            max_t = max_time
        vx_times[vx] = set(range(min_t, max_t+1))

    hits = 0
    # find the times that can hit the target for each y velocity then find
    # x-velocities that share a time that hits the target
    for vy in vy_candidates:
        min_t = ceil(solve_quadratic(vy, target_max_y)[1])
        max_t = floor(solve_quadratic(vy, target_min_y)[1])
        times_for_vy = set(range(min_t, max_t+1))
        for vx, times_for_vx in vx_times.items():
            if len(times_for_vx.intersection(times_for_vy)) > 0:
                hits += 1
    print(f'Part 2 answer: {hits}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day17input.txt')

def test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""target area: x=20..30, y=-10..-5""")

if __name__ == '__main__':
    part1(puzzle_input().get_data())
    part2(puzzle_input().get_data())

