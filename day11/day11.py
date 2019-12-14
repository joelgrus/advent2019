"""
After solving this problem I went back and refactored this code again,
under the assumption that I'd probably have to use it again on a later day.
"""
from typing import List, NamedTuple, Tuple, Iterable, Set
from enum import Enum
import itertools
from collections import deque, defaultdict
import logging


logging.basicConfig(level=logging.INFO)


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
    logging.debug(f"parsing {opcode}")

    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


class IntcodeComputer:
    def __init__(self, program: List[int]) -> None:
        self.program = defaultdict(int)
        self.program.update({i: value for i, value in enumerate(program)})
        self.inputs = deque()
        self.pos = 0
        self.relative_base = 0

    def _get_value(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos]]}")
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos] + self.relative_base]}")
            return self.program[self.program[pos] + self.relative_base]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def _loc(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos] + self.relative_base}")
            return self.program[pos] + self.relative_base

    def __call__(self, input_values: Iterable[int] = ()) -> int:
        self.inputs.extend(input_values)

        while True:
            logging.debug(f"program: {self.program}")
            logging.debug(f"pos: {self.pos}, inputs: {self.inputs}, relative_base: {self.relative_base}")

            opcode, modes = parse_opcode(self.program[self.pos])

            logging.debug(f"opcode: {opcode}, modes: {modes}")

            if opcode == Opcode.END_PROGRAM:
                raise EndProgram

            elif opcode == Opcode.ADD:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 + value2
                self.pos += 4

            elif opcode == Opcode.MULTIPLY:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 * value2
                self.pos += 4

            elif opcode == Opcode.STORE_INPUT:
                # Get input and store at location
                loc = self._loc(self.pos + 1, modes[0])
                input_value = self.inputs.popleft()
                self.program[loc] = input_value
                self.pos += 2

            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self._get_value(self.pos + 1, modes[0])
                self.pos += 2
                logging.debug(f"output: {value}")
                return value

            elif opcode == Opcode.JUMP_IF_TRUE:
                # jump if true
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 != 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.JUMP_IF_FALSE:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 == 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.LESS_THAN:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 < value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 == value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                value = self._get_value(self.pos + 1, modes[0])

                logging.debug(f"value: {value}")

                self.relative_base += value
                self.pos += 2

            else:
                raise ValueError(f"invalid opcode: {opcode}")


def run(program: Program, inputs: List[int]) -> List[int]:
    outputs = []
    computer = IntcodeComputer(program)

    try:
        while True:
            outputs.append(computer(inputs))
            inputs = ()
    except EndProgram:
        return outputs

PROGRAM = [3,8,1005,8,319,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,28,2,1008,7,10,2,4,17,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,59,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,81,1006,0,24,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,105,2,6,13,10,1006,0,5,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,134,2,1007,0,10,2,1102,20,10,2,1106,4,10,1,3,1,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,172,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,194,1,103,7,10,1006,0,3,1,4,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,228,2,109,0,10,1,101,17,10,1006,0,79,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,260,2,1008,16,10,1,1105,20,10,1,3,17,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,295,1,1002,16,10,101,1,9,9,1007,9,1081,10,1005,10,15,99,109,641,104,0,104,1,21101,387365733012,0,1,21102,1,336,0,1105,1,440,21102,937263735552,1,1,21101,0,347,0,1106,0,440,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,3451034715,1,1,21101,0,394,0,1105,1,440,21102,3224595675,1,1,21101,0,405,0,1106,0,440,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,838337454440,1,21102,428,1,0,1105,1,440,21101,0,825460798308,1,21101,439,0,0,1105,1,440,99,109,2,22101,0,-1,1,21102,1,40,2,21101,0,471,3,21101,461,0,0,1106,0,504,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,466,467,482,4,0,1001,466,1,466,108,4,466,10,1006,10,498,1102,1,0,466,109,-2,2105,1,0,0,109,4,2101,0,-1,503,1207,-3,0,10,1006,10,521,21101,0,0,-3,21202,-3,1,1,22102,1,-2,2,21101,1,0,3,21102,540,1,0,1105,1,545,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,568,2207,-4,-2,10,1006,10,568,22102,1,-4,-4,1106,0,636,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,587,1,0,1105,1,545,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,606,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,628,22102,1,-1,1,21102,1,628,0,105,1,503,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def turn(current_direction: Direction, should_turn: int) -> Direction:
    if current_direction == Direction.UP:
        return Direction.LEFT if should_turn == 0 else Direction.RIGHT
    elif current_direction == Direction.RIGHT:
        return Direction.UP if should_turn == 0 else Direction.DOWN
    elif current_direction == Direction.DOWN:
        return Direction.RIGHT if should_turn == 0 else Direction.LEFT
    elif current_direction == Direction.LEFT:
        return Direction.DOWN if should_turn == 0 else Direction.UP

def move_forward(x: int, y: int, direction: Direction) -> Tuple[int, int]:
    if direction == Direction.UP:
        return x, y + 1
    elif direction == Direction.RIGHT:
        return x + 1, y
    elif direction == Direction.DOWN:
        return x, y - 1
    elif direction == Direction.LEFT:
        return x - 1, y

def robot(program: Program) -> int:
    computer = IntcodeComputer(program)
    grid = defaultdict(int)
    grid[(0, 0)] = 1
    x = y = 0
    direction = Direction.UP
    painted = set()

    step = 0

    try:
        while True:
            step += 1
            print(step, len(painted))
            # print(f"grid: {grid}")
            # print(f"x, y: {x} {y}")
            # print(f"direction: {direction}")
            current_color = grid[(x, y)]
            color_to_paint = computer([current_color])
            # print(f"color to paint: {color_to_paint}")
            should_turn = computer()
            # print(f"should turn: {should_turn}")
            painted.add((x, y))
            grid[(x, y)] = color_to_paint
            direction = turn(direction, should_turn)
            x, y = move_forward(x, y, direction)

    except EndProgram:
        return {pos for pos, color in grid.items() if color == 1}

painted = robot(PROGRAM)

def show(positions: Set[Tuple[int, int]]):
    x_min = min(x for (x, y) in positions)
    x_max = max(x for (x, y) in positions)
    y_min = min(y for x, y in positions)
    y_max = max(y for x, y in positions)

    for y in reversed(range(y_min, y_max + 1)):
        row = ["*" if (x, y) in positions else " " for x in range(x_min, x_max + 1)]
        print("".join(row))

show(painted)
