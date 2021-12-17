"""Solutions for Day 16 of Advent of Code 2021

https://adventofcode.com/2021/day/16
"""

from aoc import Input
from math import prod

def consume_bits(bin_str, ip, ilen):
    consumed = bin_str[ip:ip+ilen]
    ip += ilen
    return consumed, ip

def consume_literal(bin_str, ip):
    literal = ''
    should_continue = True
    while should_continue:
        continue_bit, ip = consume_bits(bin_str, ip, 1)
        should_continue = continue_bit == '1'
        bits, ip = consume_bits(bin_str, ip, 4)
        literal += bits
    return int(literal, 2), ip

def consume_operator_with_packet_count(bin_str, ip):
    count, ip = consume_bits(bin_str, ip, 11)
    arg_ip = ip
    count = int(count, 2)
    ver_sum = 0
    args = []
    for index in range(count):
        value, ip, ver = consume_packet(bin_str, ip)
        args.append(value)
        ver_sum += ver
    return args, ip, ver_sum

def consume_operator_with_bit_length(bin_str, ip):
    length, ip = consume_bits(bin_str, ip, 15)
    length = int(length, 2)
    
    base_ip = ip
    ver_sum = 0
    args = []
    while ip - base_ip < length:
        value, ip, ver = consume_packet(bin_str, ip)
        args.append(value)
        ver_sum += ver
    return args, ip, ver_sum

def consume_operator(bin_str, ip):
    length_type, ip = consume_bits(bin_str, ip, 1)
    if length_type == '0':
        return consume_operator_with_bit_length(bin_str, ip)
    else:
        return consume_operator_with_packet_count(bin_str, ip)

def consume_body(bin_str, ip):
    # extract type
    type_id, ip = consume_bits(bin_str, ip, 3)
    
    if type_id == '100':
        #extract literal
        args, ip = consume_literal(bin_str, ip)
        ver_sum = 0
    else:
        args, ip, ver_sum = consume_operator(bin_str, ip)
    
    return type_id, args, ip, ver_sum

def consume_packet(bin_str, ip):
    OPERATIONS = {
            '000': sum,
            '001': prod,
            '010': min,
            '011': max,
            '100': lambda v: v,
            '101': lambda v: 1 if v[0] > v[1] else 0,
            '110': lambda v: 1 if v[0] < v[1] else 0,
            '111': lambda v: 1 if v[0] == v[1] else 0,
    }
    
    #extract version
    ver, ip = consume_bits(bin_str, ip, 3)
    ver_sum = int(ver, 2)
    
    opcode, args, ip, body_ver_sum = consume_body(bin_str, ip)
    
    value = OPERATIONS[opcode](args)
    return value, ip, ver_sum + body_ver_sum

def part1(inputs = None):
    """Output the answer to part 1 - """
    binary_str = '{num:0{width}b}'.format(num=int(inputs,16), width=len(inputs)*4)
    _, _, ver_sum = consume_packet(binary_str, 0)
    print(f'Part 1 answer: {ver_sum}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    binary_str = '{num:0{width}b}'.format(num=int(inputs,16), width=len(inputs)*4)
    value, _, _ = consume_packet(binary_str, 0)
    print(f'Part 2 answer: {value}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    return Input.from_file('day16input.txt')

def test_input():
    """Returns the test data set from the description of part 1"""
    index = 14
    data = ["D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
    "C200B40A82",
    "04005AC33890",
    "880086C3E88112",
    "CE00C43D881120",
    "D8005AC2A8F0",
    "F600BC2D8F",
    "9C005AC2F8F0",
    '9C0141080250320F1802104A08']
    return Input.from_data(data[index])

if __name__ == '__main__':
    part1(puzzle_input().get_data())
    part2(puzzle_input().get_data())

