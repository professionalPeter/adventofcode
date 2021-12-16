"""Solutions for Day 14 of Advent of Code 2021

https://adventofcode.com/2021/day/14
"""

from aoc import Input
from collections import Counter
from itertools import pairwise

def part1(inputs = None):
    """Output the answer to part 1 - """
    polymer = inputs[0][0]
    insertion_table = {}
    for line in inputs[1]:
        k,v = line.split(' -> ')
        insertion_table[k] = v
    
    for step in range(10):
        next_polymer = polymer[0]
        for left, right in pairwise(polymer):
            next_polymer += insertion_table[left+right] + right
        polymer = next_polymer
    frequencies = Counter(polymer).most_common() 
    print(f'Part 1 answer: {frequencies[0][1] - frequencies[-1][1]}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    polymer = inputs[0][0]
    insertion_table = {}
    for line in inputs[1]:
        k,v = line.split(' -> ')
        insertion_table[k] = v
    
    pairs = Counter([left + right for left, right in pairwise(polymer)])
    for step in range(40):
        next_pairs = Counter()
        for pair in pairs:
            left = pair[0] + insertion_table[pair]
            right = insertion_table[pair] + pair[1]
            next_pairs[left]  += pairs[pair]
            next_pairs[right] += pairs[pair]
        pairs = next_pairs
    
    letter_counts = Counter()
    for key, value in pairs.items():
        letter_counts[key[0]] += value
    letter_counts[polymer[-1]] += 1
    frequencies = letter_counts.most_common() 
    print(f'Part 2 answer: {frequencies[0][1] - frequencies[-1][1]}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day14input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    part1(puzzle_input().parse_records())
    part2(puzzle_input().parse_records())

