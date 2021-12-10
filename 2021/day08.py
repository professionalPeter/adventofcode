"""Solutions for Day 08 of Advent of Code 2021

https://adventofcode.com/2021/day/08
"""

from aoc import Input
from collections import defaultdict

def part1(inputs = None):
    """Output the answer to part 1 - """
    answer = 0
    for line in inputs:
        signals_and_output = line.split(' | ')
        answer += sum(1 for number in signals_and_output[1].split() if len(number) in {2,3,4,7})
    print(f'Part 1 answer: {answer}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    number_codes = [None] * 10
    answer = 0
    for line in inputs:
        signals_and_output = line.split(' | ')
        signals = [{*value} for value in signals_and_output[0].split()]
        number_codes[1] = next(filter(lambda s: len(s) == 2, signals))
        number_codes[7] = next(filter(lambda s: len(s) == 3, signals))
        number_codes[4] = next(filter(lambda s: len(s) == 4, signals))
        number_codes[8] = next(filter(lambda s: len(s) == 7, signals))
        number_codes[9] = next(filter(lambda s: len(s) == 6 and number_codes[4].union(number_codes[7]).issubset(s), signals))
        number_codes[0] = next(filter(lambda s: len(s) == 6 and s != number_codes[9] and number_codes[1].issubset(s), signals))
        number_codes[6] = next(filter(lambda s: len(s) == 6 and s != number_codes[9] and s != number_codes[0], signals))
        number_codes[3] = next(filter(lambda s: len(s) == 5 and number_codes[1].issubset(s), signals))
        number_codes[5] = next(filter(lambda s: len(s) == 5 and s.issubset(number_codes[6]), signals))
        number_codes[2] = next(filter(lambda s: len(s) == 5 and s != number_codes[3] and s!= number_codes[5], signals))
        
        code_to_numbers = { frozenset(code): str(number) for number, code in enumerate(number_codes) }  
        digits = [code_to_numbers[frozenset(output_code)] for output_code in signals_and_output[1].split()]
        answer += int(''.join(digits))
    print(f'Part 2 answer: {answer}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day08input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf""")

if __name__ == '__main__':
    part1(puzzle_input().parse_lines())
    part2(puzzle_input().parse_lines())

