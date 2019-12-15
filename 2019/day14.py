"""Solutions for Day 14 of Advent of Code 2019

https://adventofcode.com/2019/day/14
"""
import re
import time

ORE = 'ORE'

def part1(recipe_data):
    """Output the answer to part 1 - How many units of Ore to produce 1 fuel"""
    recipes = parse_recipes(recipe_data) 
    state = State()
    produce(1, 'FUEL', state, recipes)
    print(f'Part 1 answer: {state.spent[ORE]}')

def part2(recipe_data):
    """Output the answer to part 2 - How many units of fuel can be produced with 1 trillion ore

    WARNING: This runs SUPER SLOW (about 13 minutes for the puzzle answer). Needless to say, I could probably optimize this quite a bit
    """
    recipes = parse_recipes(recipe_data) 
    state = State()
    start = time.time()
    fuel_produced = 0
    target = 1_000_000_000_000
    while state.spent.get(ORE,0) < target:
        produce(1, 'FUEL', state, recipes)
        fuel_produced += 1
        if fuel_produced % 1_000_000 == 0:
            print(f'Produced: {fuel_produced}')
    end = time.time()
    print(state)
    print(f'time: {end-start}')
    print(f'Part 2 answer: {fuel_produced if state.spent[ORE]%target == 0 else fuel_produced - 1}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day14input.txt') as file:
        return file.read()

def part1_test_input1():
    """Returns the test data set from the description of part 1"""
    return """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

def part1_test_input2():
    """Returns the 2nd test data set from the description of part 1"""
    return """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""


def part1_test_input3():
    """Returns the 3rd test data set from the description of part 1"""
    return """9 ORE => 2 A
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

def part1_test_input4():
    """Returns the 4th test data set from the description of part 1"""
    return """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

def part1_test_input5():
    """Returns the 5th test data set from the description of part 1"""
    return """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

def parse_recipe_line(line):
    return [(int(unit), chem) for unit, chem in re.findall('(\d+) ([A-Z]+)', line)]

def parse_recipes(recipe_data):
    recipe_components = [parse_recipe_line(recipe) for recipe in recipe_data.splitlines()]
    # c is a list with the form [(16, F), (3, B), (2, Q) where 16 Fs + 3 Bs produces 2 Qs
    return {c[-1][1]:(c[-1][0], ingredient_list_to_dict(c[0:-1])) for c in recipe_components}

def ingredient_list_to_dict(ingredients):
    return {chem: unit for unit, chem in ingredients}

class State:
    def __init__(self):
        self.bank = {}
        self.spent = {}
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'bank: {self.bank} spent: {self.spent}'

def produce(need_quant, chem, state, recipes):
    """ Update the state to reflect the production of need_quant of the specified chemical (chem)

    recipes contains the recipes from transforming chemicals
    """
    if chem == ORE:
        state.spent[ORE] = state.spent.get(ORE, 0) + need_quant
        return []

    output_quant, inputs = recipes[chem]
    recipe_repetitions, still_needed = divmod(need_quant, output_quant)
    if still_needed > 0:
        recipe_repetitions += 1
        state.bank[chem] = state.bank.get(chem, 0) + output_quant - still_needed

    for next_chem, next_quant in inputs.items():
        next_quant *= recipe_repetitions
        banked = state.bank.get(next_chem, 0)
        if next_quant >= banked:
            next_quant -= banked
            state.bank[next_chem] = 0
            produce(next_quant, next_chem, state, recipes)
        else:
            state.bank[next_chem] -= next_quant

if __name__ == '__main__':
    part1(puzzle_input())

    # By default runs super slow (~13 minutes) so uncomment only if you really want to run it 
    #part2(puzzle_input())
