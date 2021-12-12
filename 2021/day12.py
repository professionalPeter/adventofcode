"""Solutions for Day 12 of Advent of Code 2021

https://adventofcode.com/2021/day/12
"""

from aoc import Input
from collections import defaultdict
#import pudb; pu.db

def find_paths(path, nodes, revisit_allowed):
    last_node = path[-1]
    if last_node == 'end':
        #print(','.join(path))
        return 1
    path_count = 0
    for node in nodes[last_node]:
        if node == 'start':
            continue
        elif node.islower() and node in path:
            if revisit_allowed:
                path_count += find_paths(path + [node], nodes, False)
            else:
                continue
        else:
            path_count += find_paths(path + [node], nodes, revisit_allowed)
    return path_count

def part1(inputs = None):
    """Output the answer to part 1 - """
    nodes = defaultdict(set)
    for line in inputs:
        a,b = line.split('-')
        nodes[a].add(b)
        nodes[b].add(a)

    path_count = find_paths(['start'], nodes, False)
    print(f'Part 1 answer: {path_count}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    nodes = defaultdict(set)
    for line in inputs:
        a,b = line.split('-')
        nodes[a].add(b)
        nodes[b].add(a)

    path_count = find_paths(['start'], nodes, True)
    print(f'Part 2 answer: {path_count}')

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

