from intcode import IntCodeProcessor

cpu = IntCodeProcessor(path = 'day05input.txt')
print('Part 1 answer: ', cpu.execute_program(1)[-1])
print('Part 2 answer: ', cpu.execute_program(5)[0])
