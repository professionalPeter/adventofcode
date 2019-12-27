"""Solutions for Day 16 of Advent of Code 2019

https://adventofcode.com/2019/day/16
"""
from itertools import cycle, count, zip_longest

BASE_PATTERN = [0,1,0,-1]

def part1(inputs = None):
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {None}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day16input.txt') as file:
        return file.read().rstrip()

def test_input1():
    """Returns the test data set from the description of part 1"""
    return '12345678'

def part2_test_input():
    """Returns the test data set from the description of part 2"""
    return """"""

def next_pattern(index):
    pattern = []
    for i in BASE_PATTERN:
        pattern += [i] * index
    return pattern

def next_signal(signal):
    output_signal = ''
    for index in range(1,len(signal)+1):
        pattern = cycle(next_pattern(index))
        next(pattern)

        digit = 0
        for i,p in zip(signal, pattern):
            digit += int(i) * int(p)

        output_signal += str(digit)[-1]
    return output_signal

def int_list_from_str(string):
    return [int(i) for i in string]

"""
def next_signal2(signal):
    out = ''
    digit_list = int_list_from_str(signal)
    transition_index = len(signal)//2
    for output_index in range(1,transition_index+1):
        d = 0
        sign = cycle([1,-1])
        for input_index, sign in zip(count(1,2), cycle([1,-1])):
            start = output_index * input_index - 1
            end = start + output_index
            if start >= len(signal):
                break
            d += sign * sum(digit_list[start:end])
        out += chr(abs(d)%10+48)
    sum_of_remaining = sum(digit_list[transition_index:])

    #for i in range(transition_index,len(signal)+1):
    #    out += str(sum(digit_list[i:]) % 10)
    for digit in digit_list[transition_index:]:
        d = sum_of_remaining
        out += chr(abs(d)%10+48)
        sum_of_remaining -= digit
        
    return out

"""
"""
    sum_of_remaining = 0
    char = '0'
    out = [out]
    for char in signal[-1:transition_index-1:-1]:
        sum_of_remaining += int(char)
        out.append(str(sum_of_remaining)[-1])
    return ''.join(out)
"""

def next_signal2(signal, skip_count):
    assert skip_count >= len(signal)//2 and skip_count < len(signal), f'{skip_count}, {len(signal)}'


    digit_list = int_list_from_str(signal[skip_count:])
    sum_of_remaining = sum(digit_list)

    out = '0' * skip_count
    for digit in digit_list:
        out += chr(abs(sum_of_remaining)%10+48)
        sum_of_remaining -= digit
    return out


"""
def next_signal2(signal):
    out = ''
    digit_list = int_list_from_str(signal)
    transition_index = len(signal)//3 + 1
    window_len = transition_index + 1
    for output_index in range(1,transition_index+1):
        d = 0
        sign = cycle([1,-1])
        for input_index, sign in zip(count(1,2), cycle([1,-1])):
            start = output_index * input_index - 1
            end = start + output_index
            if start >= len(signal):
                break
            d += sign * sum(digit_list[start:end])
        out += chr(abs(d)%10+48)

    #print('qtr:', out, transition_index)
    sum_of_window = sum(digit_list[transition_index:transition_index+window_len])
    #print('win: ', sum_of_window)
    for rem_char, add_char0, add_char1 in zip_longest(digit_list[transition_index:], digit_list[transition_index+window_len::2], digit_list[transition_index+window_len+1::2],fillvalue=0):
        d = sum_of_window
        out += chr(abs(d)%10+48)
        sum_of_window += -rem_char + add_char0 + add_char1
        
    return out

"""

def flawed_frequency_transform(signal, steps):
    for _ in range(steps):
        signal = next_signal(signal)
    return signal
def flawed_frequency_transform2(signal, steps, skip_count):
    for _ in range(steps):
        signal = next_signal2(signal, skip_count)
    return signal
        
def cmp(signal, steps):
    signal0 = signal1 = signal
    for i in range(steps):
        signal0 = next_signal(signal0)
        signal1 = next_signal2(signal1)
        if signal0 != signal1:
            print(i, signal0, signal1, int(signal1)-int(signal0))
            assert False
    return signal0

if __name__ == '__main__':
    part1(test_input1())
    part2(part2_test_input())


    input_signal = '80871224585914546619083218645595' #puzzle_input()
    input_signal = '00000000005914546619000000000000' #puzzle_input()
    input_signal = '00000000085914546610000000000595' #puzzle_input()
    input_signal = '00000000585914546000000000645595' #puzzle_input()
    input_signal = '00000004585914500000000218645590' #puzzle_input()
    input_signal = '808712245|85914546619083218645595' #puzzle_input()
    input_signal = '012345678901'
    input_signal = '12345678'
    input_signal = '80871224585914546619083218645595' #puzzle_input()
    input_signal = puzzle_input() * 10000
    skip_count = int(input_signal[:7])


    import time
    output = 0
    start = time.time()
    #cmp(input_signal, 100)
    #output = flawed_frequency_transform(input_signal, 100)
    print('Orig:', output)
    print(time.time() - start)
    start = time.time()
    output = flawed_frequency_transform2(input_signal, 100, skip_count)
    #print('New :', output)
    print(time.time() - start)
    print(output[:8])
    #print(next_signal2(input_signal))

