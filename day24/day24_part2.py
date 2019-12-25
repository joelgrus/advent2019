from typing import List, NamedTuple, Iterable
from collections import defaultdict
import copy

Grid = List[bool]  # 5x5

class Loc(NamedTuple):
    level: int
    x: int
    y: int

deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class RecursiveGrids:
    def __init__(self, top_level_grid: Grid) -> None:
        self.grids = defaultdict(lambda: [False for _ in range(25)])
        self.grids[0] = top_level_grid[:]

    def total_bugs(self) -> int:
        return sum(v for grid in self.grids.values() for v in grid)

    def neighbors(self, loc: Loc) -> Iterable[Loc]:
        level, x, y = loc
        if (x, y) == (2, 1):
            yield Loc(level, 2, 0)
            yield Loc(level, 1, 1)
            yield Loc(level, 3, 1)
            for x in range(5):
                yield Loc(level + 1, x, 0)
        elif (x, y) == (1, 2):
            yield Loc(level, 0, 2)
            yield Loc(level, 1, 1)
            yield Loc(level, 1, 3)
            for y in range(5):
                yield Loc(level + 1, 0, y)
        elif (x, y) == (3, 2):
            yield Loc(level, 4, 2)
            yield Loc(level, 3, 1)
            yield Loc(level, 3, 3)
            for y in range(5):
                yield Loc(level + 1, 4, y)
        elif (x, y) == (2, 3):
            yield Loc(level, 1, 3)
            yield Loc(level, 3, 3)
            yield Loc(level, 2, 4)
            for x in range(5):
                yield Loc(level + 1, x, 4)
        else:
            for dx, dy in deltas:
                newx = x + dx
                newy = y + dy
                if 0 <= newx < 5 and 0 <= newy < 5:
                    yield Loc(level, newx, newy)
            if x == 0:
                yield Loc(level - 1, 1, 2)
            if y == 0:
                yield Loc(level - 1, 2, 1)
            if x == 4:
                yield Loc(level - 1, 3, 2)
            if y == 4:
                yield Loc(level - 1, 2, 3)

    def step(self) -> None:
        num_grids = len(self.grids)
        # add to defaultdict
        maxk = max(self.grids)
        mink = min(self.grids)

        self.grids[maxk+1]
        self.grids[mink-1]

        new_grids = copy.deepcopy(self.grids)
        levels = list(self.grids.keys())
        for level in levels:
            grid = self.grids[level]
            for x in range(5):
                for y in range(5):
                    if x == y == 2:
                        continue
                    
                    loc = Loc(level, x, y)
                    neighbors = list(self.neighbors(loc))
                    #print(neighbors)
                    values = [getxy(self.grids[nlevel], nx, ny)
                              for (nlevel, nx, ny) in neighbors]
                    #print(values)
                    num_adjacent = sum(values)

                    #print(loc, num_adjacent)
                    #print()

                    bug_now = getxy(grid, x, y)
                    bug_next = (bug_now and num_adjacent == 1) or (not bug_now and num_adjacent in (1, 2))
                    new_grids[level][x + 5 * y] = bug_next

        self.grids = new_grids


def getxy(grid: Grid, x: int, y: int) -> bool:
    return grid[x + 5 * y]


RAW = """
....#
#..#.
#..##
..#..
#...."""

def parse(raw: str) -> Grid:
    return [c == '#' for line in raw.strip().split("\n") for c in line.strip()]

def show(grid: Grid):
    for start in range(0, 25, 5):
        line = grid[start:start+5]
        chars = ['#' if bug else '.' for bug in line]
        print("".join(chars))

GRID = parse(RAW)
GRIDS = RecursiveGrids(GRID)

for i in range(10):
    print(i, GRIDS.total_bugs())
    GRIDS.step()
print(GRIDS.total_bugs())

raw = """..###
.####
...#.
.#..#
#.###"""

grid = parse(raw)
grids = RecursiveGrids(grid)

for i in range(200):
    print(i, grids.total_bugs())
    grids.step()
print(grids.total_bugs())
