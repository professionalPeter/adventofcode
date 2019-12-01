from itertools import cycle

def sum():
    """Return the sum of the integer strings in the input file"""
    x = 0
    with open('input.txt') as fp:
        for line in fp:
            x += int(line)
    return x

def find_repeated_answer():
    """Repeatedly sum the integer strings in the input file until a duplicate result is found"""
    x = 0
    answer = {x}
    with open('input.txt') as fp:
        for line in cycle(fp):
            x += int(line)
            if x in answer:
                return x
            answer.add(x)

print(f'Part 1: {sum()}')
print(f'Part 2: {find_repeated_answer()}')

