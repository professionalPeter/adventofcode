"""Solutions for Day 04 of Advent of Code 2021

https://adventofcode.com/2021/day/04
"""

from aoc import Input
from collections import defaultdict

class Board:
    def __init__(self, definition):
        self.nums = defaultdict(lambda: None)
        self.marks = [[False for i in range(len(definition[0].split()))] for j in range(len(definition))]
        for row, row_def in enumerate(definition):
            for col, square_num in enumerate(row_def.split()):
                self.nums[int(square_num)] = (row, col)

    def mark(self, num):
        pos = self.nums[num]
        if not pos:
            return
        self.marks[pos[0]][pos[1]] = True

    def did_win(self):
        col_count = len(self.marks[0])
        cols = [True] * col_count
        for row_idx, row in enumerate(self.marks):
            if all(row):
                return True
            for idx in range(col_count):
                cols[idx] = cols[idx] and row[idx]
        return any(cols)

    def print(self):
        print(self.nums)
        for row in self.marks:
            print(row)


def play(boards, draws, end_after):
    active = {*range(len(boards))}

    for num in draws:
        for idx in list(active):
            board = boards[idx]
            board.mark(num)
            if board.did_win():
                active.remove(idx)
                if (len(boards) - len(active)) == end_after:
                    print("winner:", idx)
                    return idx, num

def part1(inputs = None):
    """Output the answer to part 1 - """
    draws = [int(num) for num in inputs[0][0].split(',')]
    boards = [Board(definition) for definition in inputs[1:]]

    winner, win_num = play(boards, draws, 1)

    print(boards[winner].nums)

    unmarked = [num for num, pos in boards[winner].nums.items() if pos and not boards[winner].marks[pos[0]][pos[1]]]
    unmarked_sum = sum(unmarked)

    print(f'Part 1 answer: {unmarked_sum * win_num}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    draws = [int(num) for num in inputs[0][0].split(',')]
    boards = [Board(definition) for definition in inputs[1:]]

    print(len(boards))
    winner, win_num = play(boards, draws, len(boards))

    print(boards[winner].nums)

    unmarked = [num for num, pos in boards[winner].nums.items() if pos and not boards[winner].marks[pos[0]][pos[1]]]
    unmarked_sum = sum(unmarked)

    print(f'Part 2 answer: {unmarked_sum * win_num}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day04input.txt')

def test_input1():
    """Returns the test data set from the description of part 1"""
    return Input.from_data("""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
 19  8  7 25 23
 20 11 10 24  4
 14 21 16 12  6

 14 21 17 24  4
 10 16 15  9 19
 18  8 23 26 20
 22 11 13  6  5
  2  0 12  3  7""")

def test_input2():
    """Returns the test data set from the description of part 2"""
    return Input.from_data("""""")

if __name__ == '__main__':
    #part1(puzzle_input().parse_records())
    part2(puzzle_input().parse_records())
