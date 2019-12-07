"""
After solving this problem I went back and refactored this code,
under the assumption that I'd probably have to use it again on a later day.
"""
from typing import List, NamedTuple, Tuple
from enum import Enum
import itertools
from collections import deque

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


class Amplifier:
    def __init__(self, program: List[int], phase: int) -> None:
        self.program = program[:]
        self.inputs = deque([phase])
        self.pos = 0

    def get_value(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            return self.program[pos]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def step(self, input_value: int) -> int:
        self.inputs.append(input_value)

        while True:
            opcode, modes = parse_opcode(self.program[self.pos])

            # print(self.pos, self.inputs, opcode, modes)

            if opcode == Opcode.END_PROGRAM:
                return None
            elif opcode == Opcode.ADD:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])
                self.program[self.program[self.pos + 3]] = value1 + value2
                self.pos += 4
            elif opcode == Opcode.MULTIPLY:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])
                self.program[self.program[self.pos + 3]] = value1 * value2
                self.pos += 4
            elif opcode == Opcode.STORE_INPUT:
                # Get input and store at location
                loc = self.program[self.pos + 1]
                input_value = self.inputs.popleft()
                self.program[loc] = input_value
                self.pos += 2
            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self.get_value(self.pos + 1, modes[0])
                self.pos += 2
                return value

            elif opcode == Opcode.JUMP_IF_TRUE:
                # jump if true
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 != 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.JUMP_IF_FALSE:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 == 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.LESS_THAN:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 < value2:
                    self.program[self.program[self.pos + 3]] = 1
                else:
                    self.program[self.program[self.pos + 3]] = 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 == value2:
                    self.program[self.program[self.pos + 3]] = 1
                else:
                    self.program[self.program[self.pos + 3]] = 0
                self.pos += 4

            else:
                raise RuntimeError(f"invalid opcode: {opcode}")


def run_amplifiers(program: List[int], phases: List[int]) -> int:
    amplifiers = [Amplifier(program, phase) for phase in phases]
    n = len(amplifiers)
    num_finished = 0

    last_output = 0
    last_non_none_output = None
    aid = 0

    while num_finished < n:
        # print(aid, last_output, num_finished)
        last_output = amplifiers[aid].step(last_output)
        if last_output is None:
            num_finished += 1
        else:
            last_non_none_output = last_output
        aid = (aid + 1) % n

    return last_non_none_output


PROG1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
PHASES1 = [9,8,7,6,5]
assert run_amplifiers(PROG1, PHASES1) == 139629729

PROG2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
PHASES2 = [9,7,8,5,6]
assert run_amplifiers(PROG2, PHASES2) == 18216

def best_output(program: List[int]) -> int:
    return max(run_amplifiers(program, phases)
               for phases in itertools.permutations([5, 6, 7, 8, 9]))

assert best_output(PROG1) == 139629729
assert best_output(PROG2) == 18216

PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,42,67,84,109,126,207,288,369,450,99999,3,9,102,4,9,9,1001,9,4,9,102,2,9,9,101,2,9,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,101,5,9,9,1002,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,102,4,9,9,101,2,9,9,102,4,9,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,99]

print(best_output(PROGRAM))
