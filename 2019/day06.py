"""Solutions for Day 6 of Advent of Code 2019

https://adventofcode.com/2019/day/6
"""
from itertools import product

def part1(orbits = None):
    """Output the answer to part 1 - the sum of all direct and indirect orbits"""
    orbits = orbits or parse_input(puzzle_input())
    total_orbits = sum([count_orbits(orbiter, orbits) for orbiter in orbits])
    print(f'Part 1 answer: {total_orbits}')

def part2(orbits = None):
    """Output the answer to part 2 - the number of orbital transfers from YOU to SAN(ta)"""
    orbits = orbits or parse_input(puzzle_input())
    you_path_to_com = path_to_com('YOU', orbits)
    san_path_to_com = path_to_com('SAN', orbits)
    common_orbit = first_common_orbit(you_path_to_com, san_path_to_com)
    print(f'Part 2 answer: {you_path_to_com.index(common_orbit) + san_path_to_com.index(common_orbit)}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day06input.txt') as file:
        return file.read()

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""

def parse_input(raw_input):
    """Returns orbits by parsing data in the format of the official puzzle input"""
    orbit_pairs = [line.split(')') for line in raw_input.splitlines()]
    return {orbit_pair[1]:orbit_pair[0] for orbit_pair in orbit_pairs}

def path_to_com(start, orbits):
    """Return the sequence of orbits from the start to the object that does not orbit anything"""
    orbited = orbits.get(start)
    return [] if orbited is None else [orbited] + path_to_com(orbited, orbits)

def count_orbits(orbiter, orbits):
    """Return the count of orbits from the start to the object that does not orbit anything"""
    return len(path_to_com(orbiter, orbits))

def first_common_orbit(orbit_list0, orbit_list1):
    """Finds the first shared orbit in the two given lists"""
    return next((item0 for item0, item1 in product(orbit_list0 , orbit_list1) if item0 == item1), None)

if __name__ == '__main__':
    part1()
    part2()
