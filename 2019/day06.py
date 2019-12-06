def part1_test_input():
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

def puzzle_input():
    with open('day06input.txt') as file:
        return file.read()

orbit_pairs = [line.split(')') for line in puzzle_input().splitlines()]

orbits = {}
for orbit_pair in orbit_pairs:
    orbits[orbit_pair[1]] = orbit_pair[0]


def path_to_com(orbiter):
    center = orbits.get(orbiter)
    if center is None:
        return []
    else:
        return [center] + path_to_com(center)

def count_orbits(orbiter):
    return len(path_to_com(orbiter))

def dump_orbits():
    for orbiter, center in orbits.items():
        print(f'{orbiter}: {center} - {count_orbits(orbiter)}')

total_orbits = sum([count_orbits(orbiter) for orbiter in orbits])
print(total_orbits)



def first_common_orbit(orbit_list0, orbit_list1):
    for list0_item in orbit_list0:
        for list1_item in orbit_list1:
            if list0_item == list1_item:
                return list0_item
    return None

you_path_to_com = path_to_com('YOU')
san_path_to_com = path_to_com('SAN')
common_orbit = first_common_orbit(you_path_to_com, san_path_to_com)
print(you_path_to_com.index(common_orbit) + san_path_to_com.index(common_orbit))
