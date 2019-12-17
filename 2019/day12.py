"""Solutions for Day 12 of Advent of Code 2019

https://adventofcode.com/2019/day/12
"""
from itertools import product

def part1(inputs = None):
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {None}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day12input.txt') as file:
        return file.read()

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """"""
def apply_gravity_to_all(positions, velocities):
    return [apply_gravity(v, p, positions) for v,p in zip(velocities, positions)]

def apply_gravity(velocity, position, other_positions):
    deltas = [velocity_delta(position, other) for other in other_positions]
    return sum_vectors([velocity] + deltas)

def velocity_delta(position0, position1):
    return [velocity_component_delta(p0, p1) for p0,p1 in zip(position0, position1)]

def velocity_component_delta(p0, p1):
    diff = p1 - p0
    if diff > 0:
        return 1
    elif diff < 0:
        return -1
    else:
        return 0

def apply_velocity_to_all(positions, velocities):
    return [sum_vectors(elements) for elements in zip(positions, velocities)]

def sum_vectors(iterable):
    return [sum(elements) for elements in zip(*iterable)]

def parse_input(input_file):
    return [parse_line(line) for line in input_file.splitlines()]

def parse_line(line):
    return [int(component[2:]) for component in line.strip('<>').split(', ')]
def simulate_moons(positions, steps):
    velocities = [[0,0,0] for _ in range(len(positions))]
    for _ in range(steps):
        velocities = apply_gravity_to_all(positions, velocities)
        positions = apply_velocity_to_all(positions, velocities)
    return positions, velocities

if __name__ == '__main__':
    part1(part1_test_input())
    part2(part2_test_input())
    
    positions = parse_input(puzzle_input())
    positions, velocities = simulate_moons(positions, 1000)

    kinetic_energy = [sum([abs(element) for element in vector]) for vector in velocities]
    potential_energy = [sum([abs(element) for element in position]) for position in positions]
    total_energy = [k*p for k,p in zip(kinetic_energy, potential_energy)]
    print(sum(total_energy))

