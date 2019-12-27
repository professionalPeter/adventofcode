"""Solutions for Day DAY of Advent of Code 2019

https://adventofcode.com/2019/day/DAY
"""
from itertools import product, count
from intcode import IntCodeProcessor, ExecutionError, ExecutionCode

def part1(inputs = None):
    """Output the answer to part 1 - """
    cpu = IntCodeProcessor(path='day19input.txt')
    count = 0
    size = 50
    for x,y in product(range(size), range(size)):
        result = cpu.execute_program([x,y])
        if result == [1]:
            #print(x,y)
            count += 1
        elif result != [0]:
            print(result)
    print(beam)
    print(f'Part 1 answer: {count}/{total}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('dayDAYinput.txt') as file:
        return file.read()

def test_input0():
    """Returns the test data set 0"""
    return """"""

def test_input1():
    """Returns the test data set 1"""
    return """"""

if __name__ == '__main__':
    #part1()
    part2()

    cpu = IntCodeProcessor(path='day19input.txt')
    size = 50

    def sample_beam_at(y):
        x = 0
        while cpu.execute_program([x,y]) == [0]:
            x += 1
        begin = x
        x += 1
        while cpu.execute_program([x,y]) == [1]:
            x += 1
        end = x
        return begin, end

    size = 100
    # find a line that's as wide as the square (i.e. right edge = left edge + 9)
    first_beam = (0, 0)
    rows = count(1142, 500)
    while first_beam[1] - first_beam[0] < size:
        y = next(rows)
        print(y)
        first_beam = sample_beam_at(y)
    print(y, first_beam)

    second_beam = (first_beam[1], first_beam[1])
    low = y
    # find first line where we can fit the whole square
    while first_beam[1] - second_beam[0] < size:
        y = next(rows)
        print(y)
        first_beam = sample_beam_at(y)
        second_beam = sample_beam_at(y+size-1)
    print(y, first_beam, second_beam)

    high = y
    while high - low > 1:
        mid = low + (high - low)//2
        first_beam = sample_beam_at(mid)
        second_beam = sample_beam_at(mid+size-1)
        square_fits = first_beam[1] - second_beam[0] >= size
        if square_fits:
            high = mid
        else:
            low = mid
        print('mid:', mid, 'square fits:', square_fits, 'low:', 'high:', high)
