
from typing import List, NamedTuple, Tuple, Iterable, Set, Dict, Callable
from enum import Enum
import itertools
from collections import deque, defaultdict
import logging
import copy


logging.basicConfig(level=logging.INFO)


PROGRAM = [109,424,203,1,21101,11,0,0,1106,0,282,21102,1,18,0,1105,1,259,1202,1,1,221,203,1,21101,0,31,0,1105,1,282,21102,38,1,0,1106,0,259,21002,23,1,2,21202,1,1,3,21102,1,1,1,21102,57,1,0,1106,0,303,1202,1,1,222,20102,1,221,3,20102,1,221,2,21102,259,1,1,21102,80,1,0,1105,1,225,21101,0,145,2,21102,91,1,0,1105,1,303,2101,0,1,223,20101,0,222,4,21102,259,1,3,21101,225,0,2,21102,1,225,1,21102,1,118,0,1105,1,225,20101,0,222,3,21101,0,197,2,21101,133,0,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21101,0,148,0,1105,1,259,1202,1,1,223,21001,221,0,4,21001,222,0,3,21102,1,19,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,195,1,0,105,1,109,20207,1,223,2,21002,23,1,1,21102,-1,1,3,21101,0,214,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1201,-4,0,249,22101,0,-3,1,22101,0,-2,2,21202,-1,1,3,21102,250,1,0,1106,0,225,22101,0,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22102,1,-2,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21201,-2,0,3,21101,343,0,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21102,384,1,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22102,1,1,-4,109,-5,2105,1,0]

class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9

    END_PROGRAM = 99


Modes = List[int]
Program = List[int]


class EndProgram(Exception): pass


def parse_opcode(opcode: int, num_modes: int = 3) -> Tuple[Opcode, Modes]:
    # logging.debug(f"parsing {opcode}")

    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


class IntcodeComputer:
    def __init__(self, program: List[int], get_input: Callable[[], int]) -> None:
        self.program = defaultdict(int)
        self.program.update({i: value for i, value in enumerate(program)})
        self.get_input = get_input
        self.pos = 0
        self.relative_base = 0

    def save(self):
        return [
            copy.deepcopy(self.program),
            self.get_input,
            self.pos,
            self.relative_base
        ]

    @staticmethod
    def load(program, get_input, pos, relative_base):
        computer = IntcodeComputer([], get_input)
        computer.program = program
        computer.pos = pos
        computer.relative_base = relative_base
        return computer

    def _get_value(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos]]}")
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos] + self.relative_base]}")
            return self.program[self.program[pos] + self.relative_base]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def _loc(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos] + self.relative_base}")
            return self.program[pos] + self.relative_base

    def go(self) -> int:

        while True:
            # logging.debug(f"program: {self.program}")
            # logging.debug(f"pos: {self.pos}, inputs: {self.inputs}, relative_base: {self.relative_base}")

            opcode, modes = parse_opcode(self.program[self.pos])

            # logging.debug(f"opcode: {opcode}, modes: {modes}")

            if opcode == Opcode.END_PROGRAM:
                raise EndProgram

            elif opcode == Opcode.ADD:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 + value2
                self.pos += 4

            elif opcode == Opcode.MULTIPLY:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 * value2
                self.pos += 4

            elif opcode == Opcode.STORE_INPUT:
                # Get input and store at location
                loc = self._loc(self.pos + 1, modes[0])
                input_value = self.get_input()
                self.program[loc] = input_value
                self.pos += 2

            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self._get_value(self.pos + 1, modes[0])
                self.pos += 2
                # logging.debug(f"output: {value}")

                ####
                ####

                return value

            elif opcode == Opcode.JUMP_IF_TRUE:
                # jump if true
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                # logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 != 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.JUMP_IF_FALSE:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                # logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 == 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.LESS_THAN:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 < value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 == value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                value = self._get_value(self.pos + 1, modes[0])

                # logging.debug(f"value: {value}")

                self.relative_base += value
                self.pos += 2

            else:
                raise ValueError(f"invalid opcode: {opcode}")


# total = 0

# for i in range(50):
#     for j in range(50):
#         inputs = [i, j]
#         it = iter(inputs)
#         get_input = lambda: next(it)
#         computer = IntcodeComputer(PROGRAM, lambda: next(it))

#         total += computer.go()


def check(i: int, j: int) -> int:
    inputs = [i, j]
    it = iter(inputs)
    get_input = lambda: next(it)
    computer = IntcodeComputer(PROGRAM, get_input)
    return computer.go()


hilo = {}

i = 6
jlo = 5
jhi = 5

# for i in range(6, 100):
#     row = []
#     for j in range(40):
#         result = check(i, j)
#         row.append(str(result))
#     print(''.join(row))

results = {}

for i in range(6, 2000):
    while not check(i, jlo):
        jlo += 1
    jhi = max(jhi, jlo)
    while check(i, jhi):
        jhi += 1
    jhi -= 1

    results[i] = (jlo, jhi)

    if (i - 99) in results:
        klo, khi = results[i - 99]
        if khi >= jlo + 99:
            top_left = (i - 99, jlo)

            print(top_left[1] * 10_000 + top_left[0])
            break

    print(i, jlo, jhi)


