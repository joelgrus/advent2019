"""
After solving this problem I went back and refactored this code,
under the assumption that I'd probably have to use it again on a later day.
"""
from typing import List, NamedTuple, Tuple
from enum import Enum
import itertools

class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    END_PROGRAM = 99

Modes = List[int]

def parse_opcode(opcode: int, num_modes: int = 3) -> Tuple[Opcode, Modes]:
    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


Program = List[int]

def run_program(program: Program, input: List[int]) -> List[int]:
    program = program[:]
    output = []

    pos = 0

    def get_value(pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            return program[program[pos]]
        elif mode == 1:
            # immediate mode
            return program[pos]
        else:
            raise ValueError(f"unknown mode: {mode}")

    while True:
        opcode, modes = parse_opcode(program[pos])

        if opcode == Opcode.END_PROGRAM:
            break
        elif opcode == Opcode.ADD:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])
            program[program[pos + 3]] = value1 + value2
            pos += 4
        elif opcode == Opcode.MULTIPLY:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])
            program[program[pos + 3]] = value1 * value2
            pos += 4
        elif opcode == Opcode.STORE_INPUT:
            # Get input and store at location
            loc = program[pos + 1]
            input_value = input[0]
            input = input[1:]
            program[loc] = input_value
            pos += 2
        elif opcode == Opcode.SEND_TO_OUTPUT:
            # Get output from location
            value = get_value(pos + 1, modes[0])
            output.append(value)
            pos += 2

        elif opcode == Opcode.JUMP_IF_TRUE:
            # jump if true
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 != 0:
                pos = value2
            else:
                pos += 3

        elif opcode == Opcode.JUMP_IF_FALSE:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 == 0:
                pos = value2
            else:
                pos += 3

        elif opcode == Opcode.LESS_THAN:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 < value2:
                program[program[pos + 3]] = 1
            else:
                program[program[pos + 3]] = 0
            pos += 4

        elif opcode == Opcode.EQUALS:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 == value2:
                program[program[pos + 3]] = 1
            else:
                program[program[pos + 3]] = 0
            pos += 4

        else:
            raise RuntimeError(f"invalid opcode: {opcode}")

    return output


def run_amplifier(program: List[int], input_signal: int, phase: int) -> int:
    inputs = [phase, input_signal]
    output, = run_program(program, inputs)

    return output 


def run(program: List[int], phases: List[int]) -> int:
    last_output = 0
    
    for phase in phases:
        last_output = run_amplifier(program, last_output, phase)

    return last_output

assert run([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
           [4,3,2,1,0]) == 43210

assert run([3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0], 
           [0,1,2,3,4]) == 54321

def best_output(program: List[int]) -> int:
    return max(run(program, phases)
               for phases in itertools.permutations(range(5)))

assert best_output([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210

assert best_output([3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]) \
    == 54321

PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,42,67,84,109,126,207,288,369,450,99999,3,9,102,4,9,9,1001,9,4,9,102,2,9,9,101,2,9,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,101,5,9,9,1002,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,102,4,9,9,101,2,9,9,102,4,9,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,99]

print(best_output(PROGRAM))