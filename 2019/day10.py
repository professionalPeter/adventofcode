"""Solutions for Day 10 of Advent of Code 2019

https://adventofcode.com/2019/day/10
"""
from math import sqrt, atan2, pi, sin, cos
from itertools import product

def part1(grid):
    """Output the answer to part 1 - """
    asteroids = find_asteroids(grid)
    bases = find_unique_vectors_for_all_targets(asteroids)
    base_scores = {location:len(unique_vectors.keys()) for location,unique_vectors in bases.items()}
    best_location = max(base_scores, key=base_scores.get)
    print(best_location, base_scores[best_location])

def part2(grid):
    """Output the answer to part 2 - """
    origin = (37,25)
    asteroids = find_asteroids(grid)
    asteroids_polar = polar_coords_to_targets(origin, asteroids)
    asteroids_by_angle = sort_coord_groups_by_magnitude(group_polar_coords_by_angle(asteroids_polar))
    sweep = []
    while asteroids_by_angle:
        sweep += sweep_asteroids(origin, asteroids_by_angle)
    elven_bet_winner = sweep[199]
    print(f'Part 2 answer: {elven_bet_winner[0] * 100 + elven_bet_winner[1]}')

def find_asteroids(grid):
    grid = grid.splitlines()
    asteroids = []
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == '#':
                asteroids.append((x,y))
    return asteroids

def polar_coords_to_targets(origin, targets):
    return [polar_coordinates_between(origin, p) for p in targets if p != origin]

def group_polar_coords_by_angle(coord_list):
    rounded_coords = [(m, round(a,8)) for m,a in coord_list]

    # I tried itertools groupby instead of doing this manually, but I couldn't figure out why it kept
    # put two angles that appeared identical (affter rounding) into the different groups
    angle_groups = {}
    for mag, angle in rounded_coords:
        if angle_groups.get(angle) is None:
            angle_groups[angle] = []
        angle_groups[angle].append((mag, angle))
    return angle_groups

def sort_coord_groups_by_magnitude(coord_groups):
    return {angle:sorted([magnitude for magnitude, angle in coord_group]) for angle,coord_group in coord_groups.items()}

def sweep_asteroids(origin, magnitude_groups):
    sweep = []
    for angle in sorted(magnitude_groups):
        sweep.append(grid_point_with_polar_offset(origin, (magnitude_groups[angle].pop(0), angle)))
        if not magnitude_groups[angle]:
            del magnitude_groups[angle]
    return sweep

def find_unique_vectors_for_all_targets(targets):
    return {origin:group_polar_coords_by_angle(polar_coords_to_targets(origin, targets)) for origin in targets}
    return location_vectors

def polar_coordinates_between(origin, point):
    y = point[1] - origin[1]
    x = point[0] - origin[0]
    magnitude = sqrt(x*x + y*y)
    angle = atan2(y, x)
    if y < 0 and x < 0:
        angle += 2 * pi
    return (magnitude, angle)

def grid_point_with_polar_offset(origin, polar_coord):
    x = polar_coord[0] * cos(polar_coord[1])
    y = (polar_coord[0] * sin(polar_coord[1]))
    return int(round(origin[0] + x)), int(round(origin[1] + y))

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day10input.txt') as file:
        return file.read()

def part1_test_input():
    """Returns the test data set from the description of part 1"""
    return """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

def part2_test_input_small():
    """Returns the test data set from the description of part 2"""
    return """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
"""
def part2_test_input_big():
    """Returns the test data set from the description of part 2"""
    return """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

if __name__ == '__main__':
    part1(puzzle_input())
    part2(puzzle_input())




