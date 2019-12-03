'An Int Code program processor'
from enum import IntEnum

class OpCode(IntEnum):
    'Int Code opcodes'
    ADD = 1
    MULT = 2
    HALT = 99

class IntCodeProcessor:
    'An Int Code program processor'
    def __init__(self, initial_state):
        # make sure we're only dealing with ints
        self._initial_state = [int(value) for value in initial_state]
        self._memory = None
        self._instruction_pointer = None


    def execute_program(self, noun, verb):
        'Execute the program for the given memory state, noun, and verb'
        self._memory = self._initial_state.copy()

        # set the noun and verb
        self._memory[1] = noun
        self._memory[2] = verb

        self._instruction_pointer = 0
        while self._memory[self._instruction_pointer] != OpCode.HALT:
            self._execute_instruction()
        return self._memory[0]

    def _execute_instruction(self):
        opcode = self._step()

        if opcode == OpCode.ADD:
            input_address_0 = self._step()
            input_address_1 = self._step()
            output_address = self._step()
            self._memory[output_address] = self._memory[input_address_0] + self._memory[input_address_1]
        elif opcode == OpCode.MULT:
            input_address_0 = self._step()
            input_address_1 = self._step()
            output_address = self._step()
            self._memory[output_address] = self._memory[input_address_0] * self._memory[input_address_1]
        else:
            raise ValueError(f'{opcode} is not a supported opcode')

    def _step(self):
        value = self._memory[self._instruction_pointer]
        self._instruction_pointer += 1
        return value


if __name__ == '__main__':
    with open('day2input.txt') as fp:
        program = [x for x in fp.read().rstrip().split(',')]
    processor = IntCodeProcessor(program)

    #TODO Turn these into real unit tests!
    print(f'Day2 Part 1 pass? {processor.execute_program(12, 2) == 6627023}')
    print(f'Repeated execution pass? {processor.execute_program(12, 2) == 6627023}')
    print(f'Day2 Part 2 pass? {processor.execute_program(40, 19) == 19690720}')
