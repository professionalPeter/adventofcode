"""Solutions for Day 06 of Advent of Code 2021

https://adventofcode.com/2021/day/06
"""

from aoc import Input
from collections import namedtuple
from collections import defaultdict

Fish = namedtuple('Fish', 'spawn_timer sim_timer')

def do_spawn(fish):
    return [Fish(8, sim_timer) for sim_timer in range(fish.sim_timer - 1 - fish.spawn_timer, -1, -7)]

def sim_school(school, memo):
    if len(school) == 1:
        last_fish = school[0]
        if memo[last_fish]:
            #print('used memo:', last_fish)
            return memo[last_fish]
        elif last_fish.spawn_timer > last_fish.sim_timer:
            #print('fish end:', last_fish)
            return 1
        else:
            spawn = do_spawn(last_fish)
            #print('expand_last:', last_fish)
            result = 1 + sim_school(spawn, memo)
            #print('set memo:', last_fish, result)
            memo[last_fish] = result
            return result
    else:
        #print('sim:', school)
        return sum(sim_school([fish], memo) for fish in school)

def do_sim(initial_spawn_timers, sim_length):
    fish = [Fish(spawn_timer, sim_length) for spawn_timer in initial_spawn_timers]
    memo = defaultdict(int)
    answer = sim_school(fish, memo)
    return answer

def part1(inputs = None):
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {do_sim(inputs, 80)}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {do_sim(inputs, 256)}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day06input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""3,4,3,1,2""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_ints(sep=','))
    part2(puzzle_input().parse_ints(sep=','))

