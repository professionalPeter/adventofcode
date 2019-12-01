
def calc_simple_fuel_requirement(mass):
    """Return the fuel required for a given mass"""
    return int(mass/3) - 2

def calc_total_fuel_requirement(mass):
    """Return the total fuel requirement for the mass including 
       the recursive fuel requirements"""
    fuel_for_this_mass = calc_simple_fuel_requirement(mass)
    if fuel_for_this_mass <= 0:
        return 0
    return  fuel_for_this_mass + calc_total_fuel_requirement(fuel_for_this_mass)

def part1():
    """Output the answer for part 1"""
    x = 0
    with open('day1input.txt') as fp:
        return sum([calc_simple_fuel_requirement(int(mass)) for mass in fp])

def part2():
    """Output the answer for part 2"""
    x = 0
    with open('day1input.txt') as fp:
        return sum([calc_total_fuel_requirement(int(mass)) for mass in fp])

print(f'Part 1 answer: {part1()}')
print(f'Part 2 answer: {part2()}')
