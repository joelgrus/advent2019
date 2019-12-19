from typing import List, NamedTuple, Dict, Set, Tuple
from collections import deque
import heapq

class XY(NamedTuple):
    x: int
    y: int


class Grid(NamedTuple):
    walls: Set[XY]
    keys: Dict[XY, str]
    doors: Dict[XY, str]
    start: XY

    @staticmethod
    def parse(raw: str) -> 'Grid':
        walls = set()
        keys = {}
        doors = {}

        lines = raw.strip().split("\n")

        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                loc = XY(i, j)
                if c == '#':
                    walls.add(loc)
                elif c == '@':
                    start = loc
                elif 'a' <= c <= 'z':
                    keys[loc] = c
                elif 'A' <= c <= 'Z':
                    doors[loc] = c

        return Grid(walls, keys, doors, start)

deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def one_source_shortest_path(grid: Grid, start: XY):
    # key is key_name, value is pair (distance, doors_passed_through)
    results = {}
    visited = {start}

    frontier = deque([(0, start, [])])

    while frontier:
        num_steps, (x, y), doors = frontier.popleft()
        for dx, dy in deltas:
            new_pos = XY(x + dx, y + dy)
            
            if new_pos in visited or new_pos in grid.walls:
                continue

            visited.add(new_pos)

            if new_pos in grid.keys:
                key = grid.keys[new_pos]
                results[key] = (num_steps + 1, doors)
                frontier.append((num_steps + 1, new_pos, doors))
            elif new_pos in grid.doors:
                new_doors = doors + [grid.doors[new_pos]]
                frontier.append((num_steps + 1, new_pos, new_doors))
            else:
                frontier.append((num_steps + 1, new_pos, doors))

    return results


def all_source_shortest_path(grid: Grid):
    results = {}

    results['@'] = one_source_shortest_path(grid, grid.start)
    for key_loc, key in grid.keys.items():
        results[key] = one_source_shortest_path(grid, key_loc)

    return results



RAW = """#########
#b.A.@.a#
#########"""

GRID = Grid.parse(RAW)

GRID2 = Grid.parse("""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""")

GRID3 = Grid.parse("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""")

def signature(prev_keys: Set[str], loc: str) -> str:
    return f"{loc}:{''.join(sorted(prev_keys))}"

def shortest_path(grid: Grid) -> int:
    assp = all_source_shortest_path(grid)
    seen_signatures = set()

    num_keys = len(grid.keys)
    # maintain priority queue of num_steps, key at, keys had
    pq = [(0, '@', set())]

    while pq:
        num_steps, source_key, keys_had = heapq.heappop(pq)
        sig = signature(keys_had, source_key)
        if sig in seen_signatures:
            continue
        seen_signatures.add(sig)

        print(num_steps, source_key, keys_had)

        if len(keys_had) == num_keys:
            return num_steps

        ossp = assp[source_key]
        for dest_key, (steps_to_key, doors) in ossp.items():
            if dest_key in keys_had:
                continue
            if any(door.lower() not in keys_had for door in doors):
                continue

            new_keys = keys_had | {dest_key}
            heapq.heappush(pq, (num_steps + steps_to_key, dest_key, new_keys))



with open('day18.txt') as f:
    grid = Grid.parse(f.read())

# print(shortest_path(grid))