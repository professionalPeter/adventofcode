"""Solutions for Day 12 of Advent of Code 2021

https://adventofcode.com/2021/day/12
"""

from aoc import Input
from collections import defaultdict
from copy import deepcopy
#import pudb; pu.db

def find_paths(path, nodes, visits_allowed):
    initial = path[-1]
    if initial == 'end':
        final_path = ','.join(path)
        #print(final_path)
        return set([final_path])
    path_set = set()
    for node in nodes[initial]:
        if node.islower():
            if visits_allowed[node] > 0:
                visits_allowed[node] -= 1
            else:
                continue
        path_set = path_set.union(find_paths(path + [node], nodes, visits_allowed))
        if node.islower():
            visits_allowed[node] += 1
    return path_set

def part1(inputs = None):
    """Output the answer to part 1 - """
    nodes = defaultdict(set)
    for line in inputs:
        components = line.split('-')
        nodes[components[0]].add(components[1])
        nodes[components[1]].add(components[0])

    visits_allowed = {node:1 for node in nodes if node.islower()}
    visits_allowed['start'] = 0
    visits_allowed['end'] = 1
    path_set = find_paths(['start'], nodes, visits_allowed)
    print(f'Part 1 answer: {len(path_set)}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    nodes = defaultdict(set)
    for line in inputs:
        components = line.split('-')
        nodes[components[0]].add(components[1])
        nodes[components[1]].add(components[0])

    lower_nodes = [node for node in nodes if node.islower() and node != 'start' and node != 'end']

    path_set = set()
    for special_node in lower_nodes:
        visits_allowed = {node:1 for node in lower_nodes}
        visits_allowed[special_node] = 2
        visits_allowed['start'] = 0
        visits_allowed['end'] = 1
        path_set = path_set.union(find_paths(['start'], nodes, visits_allowed))
    print(f'Part 2 answer: {len(path_set)}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day12input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""")

def test_input3():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""dc-end
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())

