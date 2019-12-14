"""
After solving this problem I went back and refactored this code again,
under the assumption that I'd probably have to use it again on a later day.
"""
from typing import List, NamedTuple, Tuple, Iterable, Set, Dict
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
    # logging.debug(f"parsing {opcode}")

    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


class IntcodeComputer:
    def __init__(self, program: List[int]) -> None:
        self.program = program[:]
        self.inputs = deque()
        self.pos = 0
        self.relative_base = 0

    def _expand(self, pos: int) -> None:
        while len(self.program) <= pos:
            self.program.append(0)

    def _get_value(self, pos: int, mode: int) -> int:
        self._expand(pos)

        if mode == 0:
            # pointer mode
            self._expand(self.program[pos])
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos]]}")
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            self._expand(self.program[pos] + self.relative_base)
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos] + self.relative_base]}")
            return self.program[self.program[pos] + self.relative_base]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def _loc(self, pos: int, mode: int) -> int:
        self._expand(pos)

        if mode == 0:
            # pointer mode
            self._expand(self.program[pos])
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            self._expand(self.program[pos] + self.relative_base)
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos] + self.relative_base}")
            return self.program[pos] + self.relative_base

    def __call__(self, input_values: Iterable[int] = ()) -> int:
        self.inputs.extend(input_values)

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
                input_value = self.inputs.popleft()
                self.program[loc] = input_value
                self.pos += 2

            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self._get_value(self.pos + 1, modes[0])
                self.pos += 2
                # logging.debug(f"output: {value}")

                ####
                self.inputs.clear()
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

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


with open('day13.txt') as f:
    program = [int(n) for n in f.read().strip().split(",")]


def count_blocks(program: Program) -> int:
    screen: Dict[Tuple[int, int], Tile] = {}
    computer = IntcodeComputer(program)

    try:
        while True:
            x = computer()
            y = computer()
            tile = Tile(computer())
            screen[(x, y)] = tile
    except EndProgram:
        # return len([tile for tile in screen.values() if tile == Tile.BLOCK])
        return screen
# print(count_blocks(program))

# screen = count_blocks(program)

def show(tile: Tile) -> str:
    if tile == Tile.BALL:
        return 'o'
    elif tile == Tile.BLOCK:
        return '#'
    elif tile == Tile.EMPTY:
        return ' '
    elif tile == Tile.PADDLE:
        return '-'
    elif tile == Tile.WALL:
        return 'X'
    else:
        raise RuntimeError(f"bad tile: {tile}")

def draw(screen: Dict[Tuple[int, int], Tile]) -> None:
    if not screen:
        return
    x_min = min(x for x, y in screen)
    x_max = max(x for x, y in screen)
    y_min = min(y for x, y in screen)
    y_max = max(y for x, y in screen)

    for y in range(y_min, y_max + 1):
        row = [show(screen.get((x, y), Tile.EMPTY)) for x in range(x_min, x_max + 1)]
        print("".join(row))


def play_breakout(program: Program) -> int:
    screen: Dict[Tuple[int, int], Tile] = {}
    score = 0
    program[0] = 2
    computer = IntcodeComputer(program)

    ball_x = None
    paddle_x = None
    num_blocks = 0

    step = 0

    try:
        while True:
            if ball_x is None or paddle_x is None:
                input_value = []
            elif paddle_x < ball_x:
                input_value = [1]
            elif ball_x < paddle_x:
                input_value = [-1]
            else:
                input_value = [0]

            x = computer(input_value)
            y = computer()

            if x == -1 and y == 0:
                score = computer()
                print("score", score)
                print("ball x", ball_x)
                print("paddle x", paddle_x)
                print("input value", input_value)
                print("num_blocks", num_blocks)

            else:
                tile = Tile(computer())
                previous_tile = screen.get((x, y), Tile.EMPTY)

                if tile == Tile.BLOCK and previous_tile != Tile.BLOCK:
                    num_blocks += 1
                elif previous_tile == Tile.BLOCK and tile != Tile.BLOCK:
                    num_blocks -= 1

                screen[(x, y)] = tile

                if tile == Tile.BALL:
                    ball_x = x
                elif tile == Tile.PADDLE:
                    paddle_x = x

                #                if tile in (Tile.BALL, Tile.PADDLE):

    except EndProgram:
        # return len([tile for tile in screen.values() if tile == Tile.BLOCK])
        return score
# print(count_blocks(program))

print(play_breakout(program))
