'An Int Code program processor'
from enum import IntEnum
import logging

logger = logging.getLogger('com.pgl.advent_of_code')
logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.DEBUG)

class OpCode(IntEnum):
    'Int Code opcodes'
    ADD = 1
    MULT = 2
    SAVE_INPUT = 3
    OUTPUT = 4
    JMP_IF_TRUE = 5
    JMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

class Command:
    'contains the opcode and parameter modes for an instruction'
    def __init__(self, command):
        if int(command) < 0:
            raise ValueError(f"Invalid command {command}. Commands must be >= 0")
        command = str(command)
        self.opcode = OpCode(int(command[-2:]))
        self._parameter_modes = [int(mode) for mode in command[-3::-1]]
        self._validate_paramter_modes()

    def parameter_mode(self, index):
        return self._parameter_modes[index] if index < len(self._parameter_modes) else ParameterMode.POSITION

    def _validate_paramter_modes(self):
        invalid_modes = [mode for mode in self._parameter_modes if mode not in set([0,1])]
        if len(invalid_modes) > 0:
            raise ValueError(f'Invalid modes {invalid_modes} in opcode {opcode}')

class IntCodeProcessor:
    'An Int Code program processor'
    def __init__(self, initial_state = [], path = None):
        # make sure we're only dealing with ints
        if path is not None:
            initial_state = self._load_program(path) 
        self._initial_state = [int(value) for value in initial_state]
        self._memory = None
        self._instruction_pointer = None

    def _load_program(self, path):
        with open(path) as fp:
            return [x for x in fp.read().rstrip().split(',')]

    def execute_program_with_inputs(self, noun, verb):
        'Execute the program for the given memory state, noun, and verb'
        self._memory = self._initial_state.copy()

        # set the noun and verb
        self._memory[1] = noun
        self._memory[2] = verb

        self._instruction_pointer = 0
        while self._memory[self._instruction_pointer] != OpCode.HALT:
            self._execute_instruction()
        return self._memory[0]

    def execute_program(self, input_channel = None):
        'Execute the program for the given memory state, noun, and verb'
        self._memory = self._initial_state.copy()

        self._instruction_pointer = 0
        self._input_channel = input_channel
        self.outputs = []
        while self._memory[self._instruction_pointer] != OpCode.HALT:
            result = self._execute_instruction()
            if result is not None:
                self.outputs.append(result)
                logger.debug(f'Output: {self.outputs}')
        return self.outputs

    def _execute_instruction(self):
        ip = self._instruction_pointer
        command = Command(self._step())
        logger.debug(f'{ip}: {command.opcode} {command._parameter_modes}')

        if command.opcode == OpCode.ADD:
            inputs = [self._read(command.parameter_mode(index)) for index in range(2)]
            self._write(sum(inputs))
        elif command.opcode == OpCode.MULT:
            inputs = [self._read(command.parameter_mode(index)) for index in range(2)]
            self._write(inputs[0] * inputs[1])
        elif command.opcode == OpCode.SAVE_INPUT:
            self._write(self._read_input_channel())
        elif command.opcode == OpCode.OUTPUT:
            return self._read(command.parameter_mode(0))
        elif command.opcode == OpCode.JMP_IF_TRUE:
            test_value = self._read(command.parameter_mode(0))
            jump_position = self._read(command.parameter_mode(1))
            if test_value != 0:
                self._instruction_pointer = jump_position
        elif command.opcode == OpCode.JMP_IF_FALSE:
            test_value = self._read(command.parameter_mode(0))
            jump_position = self._read(command.parameter_mode(1))
            if test_value == 0:
                self._instruction_pointer = jump_position
        elif command.opcode == OpCode.EQUALS:
            value0 = self._read(command.parameter_mode(0))
            value1 = self._read(command.parameter_mode(1))
            result = 1 if value0 == value1 else 0
            self._write(result)
        elif command.opcode == OpCode.LESS_THAN:
            value0 = self._read(command.parameter_mode(0))
            value1 = self._read(command.parameter_mode(1))
            result = 1 if value0 < value1 else 0
            self._write(result)
        else:
            raise ValueError(f'{command.opcode} is not a supported opcode')

    def _read_input_channel(self):
        logger.debug(f'Read from input channel: {self._input_channel}')
        return self._input_channel

    def _write(self, value):
        output_address = self._read(ParameterMode.IMMEDIATE)
        self._memory[output_address] = value
        logger.debug(f'WRITE value: {value} position: {output_address}')

    def _step(self):
        value = self._memory[self._instruction_pointer]
        self._instruction_pointer += 1
        return value

    def _read(self, mode = ParameterMode.POSITION):
        parameter = self._step()
        result = parameter if mode == ParameterMode.IMMEDIATE else self._memory[parameter]
        logger.debug(f'READ parameter: {parameter} mode: {mode} value: {result}')
        return result

    def _jump_if(success):
        test_value = self._read(command.parameter_mode(0))
        jump_position = self._read(command.parameter_mode(1))
        test_pass = test_value == 0
        if test_pass AND success:
            self._instruction_pointer = jump_position


if __name__ == '__main__':
    #TODO Turn these into real unit tests!
    print(f'Input/Output test: {IntCodeProcessor([3,0,4,0,99]).execute_program(22) == [22]}')
    processor = IntCodeProcessor([1101,100,-1,4,0])
    processor.execute_program()
    print(f'Negative parameter test: {processor._memory[4] == 99}')
    print(f'Parameter mode order: {IntCodeProcessor([1001,0,3000,0,4,0,99]).execute_program() == [4001]}')
    processor = IntCodeProcessor([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
    print(f'Jump test with position mode (input 0): {processor.execute_program(0) == [0]}')
    print(f'Jump test with position mode (input 1): {processor.execute_program(1) == [1]}')
    processor = IntCodeProcessor([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    print(f'Jump test with immediate mode (input 0): {processor.execute_program(0) == [0]}')
    print(f'Jump test with immediate mode (input 1): {processor.execute_program(99) == [1]}')
    processor = IntCodeProcessor([3,9,8,9,10,9,4,9,99,-1,8])
    print(f'Equals test when matching position mode: {processor.execute_program(8) == [1]}')
    print(f'Equals test when not matching position mode: {processor.execute_program(99) == [0]}')
    processor = IntCodeProcessor([3,3,1108,-1,8,3,4,3,99])
    print(f'Equals test when matching immediate mode: {processor.execute_program(8) == [1]}')
    print(f'Equals test when not matching immediate mode: {processor.execute_program(99) == [0]}')
    processor = IntCodeProcessor([3,9,7,9,10,9,4,9,99,-1,8])
    print(f'Less Than test when less than position mode: {processor.execute_program(7) == [1]}')
    print(f'Less Than test when not less than position mode: {processor.execute_program(8) == [0]}')
    processor = IntCodeProcessor([3,3,1107,-1,8,3,4,3,99])
    print(f'Less Than test when less than immediate mode: {processor.execute_program(7) == [1]}')
    print(f'Less Than test when not less than immediate mode: {processor.execute_program(8) == [0]}')

    processor = IntCodeProcessor(path= 'day02input.txt')
    print(f'Day2 Part 1 pass? {processor.execute_program_with_inputs(12, 2) == 6627023}')
    print(f'Repeated execution pass? {processor.execute_program_with_inputs(12, 2) == 6627023}')
    print(f'Day2 Part 2 pass? {processor.execute_program_with_inputs(40, 19) == 19690720}')

    processor = IntCodeProcessor(path= 'day05input.txt')
    print(f'Day 5 part 1 pass: {processor.execute_program(1) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 15426686]}')
    print(f'Day 5 part 2 pass: {processor.execute_program(5) == [11430197]}')

"""
Future polish:
Combine handlers of similar opcodes
Get rid of the noun, verb executer and move it back to day02
"""
