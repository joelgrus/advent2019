from typing import List

Grid = List[bool]  # 5x5

def getxy(grid: Grid, x: int, y: int) -> bool:
    return grid[x + 5 * y]


deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def step(grid: Grid) -> Grid:
    next_grid = grid[:]

    for x in range(5):
        for y in range(5):
            num_adjacent = sum(getxy(grid, x + dx, y + dy)
                               for dx, dy in deltas
                               if 0 <= x + dx < 5 and 0 <= y + dy < 5)
            """
            A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
            An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
            """
            bug_now = getxy(grid, x, y)
            bug_next = (bug_now and num_adjacent == 1) or (not bug_now and num_adjacent in (1, 2))
            next_grid[x + 5 * y] = bug_next

    return next_grid

RAW = """....#
#..#.
#..##
..#..
#...."""

def parse(raw: str) -> Grid:
    return [c == '#' for line in raw.strip().split("\n") for c in line.strip()]

def biodiversity(grid: Grid) -> int:
    return sum(2 ** i * bug for i, bug in enumerate(grid))

def find_repeat(grid: Grid) -> int:
    seen = set()
    while True:
        bio = biodiversity(grid)
        if bio in seen:
            return bio
        seen.add(bio)
        grid = step(grid)

raw = """..###
.####
...#.
.#..#
#.###"""

grid = parse(raw)

print(find_repeat(grid))