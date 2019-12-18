'An Int Code program processor'
from enum import IntEnum, Enum, auto
import logging

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

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
    ADJUST_RELATIVE_BASE = 9
    HALT = 99

class ExecutionError(Exception):
    def __init__(self, code):
        self.reason = code

class ExecutionCode(Enum):
    'Reasons for execution halting'
    NEED_INPUT = auto()

class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class Command:
    'contains the opcode and parameter modes for an instruction'
    def __init__(self, command):
        if int(command) < 0:
            raise ValueError(f"Invalid command {command}. Commands must be >= 0")
        command = str(command)
        self.opcode = OpCode(int(command[-2:]))
        self._parameter_modes = [int(mode) for mode in command[-3::-1]]
        self._validate_paramter_modes(command)

    def parameter_mode(self, index):
        return self._parameter_modes[index] if index < len(self._parameter_modes) else ParameterMode.POSITION

    def _validate_paramter_modes(self, command):
        invalid_modes = [mode for mode in self._parameter_modes if mode not in set(mode.value for mode in ParameterMode)]
        if len(invalid_modes) > 0:
            raise ValueError(f'Invalid modes {invalid_modes} in command {command}')

class IntCodeProcessor:
    'An Int Code program processor'
    def __init__(self, initial_state = [], path = None, overrides = None):
        # make sure we're only dealing with ints
        if path is not None:
            initial_state = IntCodeProcessor.load_program(path) 
        self._initial_state = [int(value) for value in initial_state]
            
        if overrides is not None:
            self._initial_state[:len(overrides)] = overrides

        self._memory = None
        self._instruction_pointer = None
        self._relative_base = None
        self._reset_execution()
    def dump_memory(self, start=None, end=None):
        start = start or self._instruction_pointer
        end = end or start + 15
        end = end if end < len(self._memory) else len(self._memory)-1
        for index, value in enumerate(self._memory[start:end]):
            print(f'{index+start}: {value}')

    @classmethod
    def load_program(cls, path):
        with open(path) as fp:
            return [x for x in fp.read().rstrip().split(',')]

    def _reset_execution(self):
        self._memory = [0] * 10_000
        for index, value in enumerate(self._initial_state):
            self._memory[index] = value
        self._instruction_pointer = 0
        self._relative_base = 0
        self.outputs = []
    
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

    def execute_program(self, input_channel = None, reset = True):
        'Execute the program for the given memory state, noun, and verb'

        if reset:
            self._reset_execution()
        self._set_input_channel(input_channel)
        while self._memory[self._instruction_pointer] != OpCode.HALT:
            saved_instruction_pointer = self._instruction_pointer
            try:
                result = self._execute_instruction()
                if result is not None:
                    self.outputs.append(result)
                    logger.info(f'Output: {self.outputs}')
            except ExecutionError as err:
                self._instruction_pointer = saved_instruction_pointer
                raise err
        logger.info('HALT')
        return self.outputs

    def _set_input_channel(self, input_channel):
        """Sets the processors input channel ti the given input channel

        This method accepts for both ints and lists of ints
        """
        if input_channel is None:
            self._input_channel = iter(list())
            return

        try:
            self._input_channel = iter(input_channel)
        except TypeError:
            self._input_channel = iter([input_channel])

    def _execute_instruction(self):
        ip = self._instruction_pointer
        command = Command(self._step())
        logger.info(f'{ip}: {command.opcode.name} {command._parameter_modes} ({command.opcode})')

        if command.opcode == OpCode.ADD:
            inputs = [self._read(command.parameter_mode(index)) for index in range(2)]
            result = sum(inputs)
            self._write(result, command.parameter_mode(2))
            logger.info(f'ADD values: ({inputs[0]},{inputs[1]}) result: {result}, target: ')
        elif command.opcode == OpCode.MULT:
            inputs = [self._read(command.parameter_mode(index)) for index in range(2)]
            result = inputs[0] * inputs[1]
            self._write(result, command.parameter_mode(2))
            logger.info(f'MULT values: ({inputs[0]},{inputs[1]}) result: {result}, target: ')
        elif command.opcode == OpCode.SAVE_INPUT:
            result = self._read_input_channel()
            self._write(result, command.parameter_mode(0))
            logger.info(f'SAVE_INPUT: {result}')
        elif command.opcode == OpCode.OUTPUT:
            result = self._read(command.parameter_mode(0))
            logger.info(f'OUTPUT: {result}')
            return result
        elif command.opcode == OpCode.JMP_IF_TRUE:
            test_value = self._read(command.parameter_mode(0))
            jump_position = self._read(command.parameter_mode(1))
            result = test_value != 0
            if result:
                self._instruction_pointer = jump_position
            logger.info(f'JUMP IF TRUE value: {test_value} result: {result} target: {jump_position}')
        elif command.opcode == OpCode.JMP_IF_FALSE:
            test_value = self._read(command.parameter_mode(0))
            jump_position = self._read(command.parameter_mode(1))
            result = test_value == 0
            if result:
                self._instruction_pointer = jump_position
            logger.info(f'JUMP IF FALSE value: {test_value} result: {result} target: {jump_position}')
        elif command.opcode == OpCode.EQUALS:
            value0 = self._read(command.parameter_mode(0))
            value1 = self._read(command.parameter_mode(1))
            result = 1 if value0 == value1 else 0
            self._write(result, command.parameter_mode(2))
            logger.info(f'EQUALS value0: {value0} value1: {value1} result: {result} target: ')
        elif command.opcode == OpCode.LESS_THAN:
            value0 = self._read(command.parameter_mode(0))
            value1 = self._read(command.parameter_mode(1))
            result = 1 if value0 < value1 else 0
            self._write(result, command.parameter_mode(2))
            logger.info(f'LESS THAN value0: {value0} value1: {value1} result: {result} target: ')
        elif command.opcode == OpCode.ADJUST_RELATIVE_BASE:
            offset = self._read(command.parameter_mode(0))
            self._relative_base += offset
            logger.info(f'RELATIVE BASE offset: {offset} new base: {self._relative_base}')
        else:
            raise ValueError(f'{command.opcode} is not a supported opcode')

    def _read_input_channel(self):
        try:
            result = next(self._input_channel)
            logger.debug(f'READ input: {result}')
            return result
        except StopIteration:
            pass # pass so that StopIteration doesn't show up in the handling of the ExecutionError 
        raise ExecutionError(ExecutionCode.NEED_INPUT)

    def _write(self, value, mode):
        base = self._relative_base if mode == ParameterMode.RELATIVE else 0
        offset = self._step()
        output_address = base + offset
        
        self._memory[output_address] = value
        logger.debug(f'WRITE value: {value} base: {base} offset: {offset} position: {output_address}')

    def _step(self):
        value = self._memory[self._instruction_pointer]
        self._instruction_pointer += 1
        return value

    def _read(self, mode):
        parameter = self._step()
        if mode == ParameterMode.IMMEDIATE:
            result = parameter
        else:
            base = self._relative_base if mode == ParameterMode.RELATIVE else 0
            result = self._memory[base + parameter]
        logger.debug(f'READ parameter: {parameter} mode: {mode} value: {result}')
        return result

    def _jump_if(self, success):
        test_value = self._read(command.parameter_mode(0))
        jump_position = self._read(command.parameter_mode(1))
        test_pass = test_value == 0
        if test_pass and success:
            self._instruction_pointer = jump_position


if __name__ == '__main__':
    #TODO Turn these into real unit tests!
    print(f'Input/Output test - single int: {IntCodeProcessor([3,0,4,0,99]).execute_program(22) == [22]}')
    print(f'Input/Output test - list: {IntCodeProcessor([3,0,4,0,3,0,4,0,99]).execute_program([1001, 1002]) == [1001, 1002]}')
    try:
        IntCodeProcessor([3,0,3,0,4,0,99]).execute_program([1001])
    except ExecutionError as err:
        result = err
    print(f'Input/Output test - underflow: { result.reason == ExecutionCode.NEED_INPUT }')
    print(f'Input test - relative mode: {IntCodeProcessor([109,1000,203,0,4,1000,99]).execute_program(22) == [22]}')
    print(f'Output test - relative mode: {IntCodeProcessor([109,1000,3,1000,204,0,99]).execute_program(22) == [22]}')

    processor = IntCodeProcessor([3,0,3,0,4,0,99])
    try:
        processor.execute_program([1001])
    except ExecutionError as err:
        result = processor.execute_program([1002], reset = False)
    print(f'Input/Output test - resume execution: { result == [1002] }')
    print(f'execute_program test - executes when reset == false on first call: {IntCodeProcessor([3,0,4,0,99]).execute_program(22, reset = False) == [22]}')
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


    processor = IntCodeProcessor([99,99,99], overrides=[104,22])
    print(f'Overrides are applied during execution: {processor.execute_program() == [22]}')
    processor = IntCodeProcessor([109, 3, 2101, 10, 0, 0, 4, 0, 99])
    print(f'Relative mode test: {processor.execute_program() == [20]}')
    program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    processor = IntCodeProcessor(program)
    print(f'Extended memory test: {processor.execute_program() == program}')
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
Make HALT handled inside execute_instruction
Create a clear output, or cleaner way of connecting one to another
Make logging consistent and clean (maybe get rid of the reads and writes or demote them?)
MAke a better decision on where NEED_INPUT should be raised
Consolidate the logic for adding the offset to the relative base
Validate that input is all integers
Fill in target component of info log lines
Take away load_program since override bytes now exists?
Should you be able to override on execution instead of init?
"""
