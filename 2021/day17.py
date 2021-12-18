"""Solutions for Day 17 of Advent of Code 2021

https://adventofcode.com/2021/day/17
"""

from aoc import Input
from math import sqrt, ceil, floor
import re

def part1(inputs = None):
    """Output the answer to part 1 - """
    target_min_y = -78
    max_vy = -target_min_y - 1
    max_height = (max_vy * (max_vy + 1))/2
    print(f'Part 1 answer: {max_height}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    match = re.search('.*x=(.*)\.\.(.*), y=(.*)\.\.(.*)', inputs)
    target_min_x = int(match.group(1))
    target_max_x = int(match.group(2))
    target_min_y = int(match.group(3))
    target_max_y = int(match.group(4))
    print('targets: ', target_min_x, target_max_x, target_min_y, target_max_y)
    
    min_vy = target_min_y
    max_vy = -target_min_y - 1
    min_vx = ceil((-1 + sqrt(8 * target_min_x + 1))/2)
    max_vx = target_max_x
    print(min_vy, max_vy, min_vx, max_vx, max_vy - min_vy + 1, max_vx - min_vx + 1)
    
    max_time_b = 2 * max_vy + 1
    max_time = (max_time_b + sqrt(max_time_b**2 - 8*target_min_y))/2
    print('max_time_b', max_time_b, 'max_time:', max_time, target_min_y)
    
    hits = []
    candidate_vx = range(min_vx, max_vx+1)
    print('vx range: ', candidate_vx)
    for vx in candidate_vx:
        potential_times = set()
        quadratic_b = (2*vx+1)
        radicand = quadratic_b**2 - 8*target_min_x
        if radicand >= 0:
            potential_times.add(ceil((quadratic_b - sqrt(radicand))/2))
            radicand = quadratic_b**2 - 8*target_max_x
            if radicand >= 0:
                potential_times.add(floor((quadratic_b - sqrt(radicand))/2))
        print('vx:', vx, 'potential_times: ', potential_times, 'vy range:', range(min_vy, max_vy+1))
        for vy in range(min_vy, max_vy+1):
            for t in potential_times:
                y = (-(t**2) + t * (2*vy+1))/2
                print('vy:', vy, 'y:', y, range(target_min_y, target_max_y + 1))
                if y in range(target_min_y, target_max_y + 1):
                    hits.append((vx, vy))
    print(f'Part 2 answer: {hits}\n{len(hits)}, {len(set(hits))}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day17input.txt')

def test_input():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""target area: x=20..30, y=-10..-5""")

if __name__ == '__main__':
    part1(test_input().get_data())
    part2(test_input().get_data())

