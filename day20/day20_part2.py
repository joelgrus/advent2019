from typing import List, Dict, Set, Iterator, NamedTuple
from collections import defaultdict, deque

deltas1 = [(0, 1), (1, 0)]
deltas2 = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class XY(NamedTuple):
    x: int
    y: int


class Maze(NamedTuple):
    start: XY
    end: XY
    neighbors: Dict[XY, List[XY]]


def parse(raw: str) -> Maze:
    lines = raw.strip("\n").split("\n")
    nr = len(lines)
    nc = len(lines[0])

    def neighbors(loc: XY, deltas) -> Iterator[XY]:
        x, y = loc
        for dx, dy in deltas:
            neighbor = XY(x + dx, y + dy)
            if 0 <= neighbor.x < nr and 0 <= neighbor.y < nc:
                yield neighbor

    # First let's find all the portals
    portals: Dict[str, List[XY]] = defaultdict(list)

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if 'A' <= c <= 'Z':
                for i2, j2 in neighbors(XY(i, j), deltas1):
                    c2 = lines[i2][j2]
                    if 'A' <= c2 <= 'Z':
                        portals[f"{c}{c2}"].extend([XY(i, j), XY(i2, j2)])

    # handle start and end separately    
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                for loc2 in neighbors(loc, deltas2):
                    if loc2 in portals['AA']:
                        start = loc
                    elif loc2 in portals['ZZ']:
                        end = loc

    inside_portal_neighbors = {}
    inside_neighbor_portals = {}
    outside_portal_neighbors = {}
    outside_neighbor_portals = {}


    # find dots that are next to portals
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                outside = i == 2 or i == nr - 3 or j == 2 or j == nc - 3
                for loc2 in neighbors(loc, deltas2):                    
                    for portal, locs in portals.items():
                        if loc2 in locs:
                            if outside:
                                outside_neighbor_portals[loc] = portal
                                outside_portal_neighbors[portal] = loc
                            else:
                                inside_neighbor_portals[loc] = portal
                                inside_portal_neighbors[portal] = loc
    

    # each entry has to have a square, and a change in level
    neighbor_dict = defaultdict(list)

    # find neighbors
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                # get direct neighbors
                for loc2 in neighbors(loc, deltas2):
                    i2, j2 = loc2
                    c2 = lines[i2][j2]
                    if c2 == '.':
                        neighbor_dict[loc].append((loc2, 0))
                # get portal neighbors
                outside_portal = outside_neighbor_portals.get(loc)
                if outside_portal and outside_portal not in ['AA', 'ZZ']:
                    other_loc = inside_portal_neighbors[outside_portal]
                    neighbor_dict[loc].append((other_loc, -1))
                
                inside_portal = inside_neighbor_portals.get(loc)
                if inside_portal:
                    other_loc = outside_portal_neighbors[inside_portal]
                    neighbor_dict[loc].append((other_loc, +1))
                        
    return Maze(start,
                end,
                neighbors=neighbor_dict)

RAW = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """

MAZE = parse(RAW)

def shortest_path(maze: Maze) -> int:
    # (loc, level)
    visited = {(maze.start, 0)}
    # (loc, level, num_steps)
    q = deque([(maze.start, 0, 0)])


    while q:
        loc, level, num_steps = q.popleft()
        print(loc, level, num_steps)

        for nbor, level_delta in maze.neighbors[loc]:
            if nbor == maze.end and level == 0:
                return num_steps + 1

            new_level = level + level_delta

            if new_level >= 0 and (nbor, new_level) not in visited:
                visited.add((nbor, new_level))
                q.append((nbor, new_level, num_steps + 1))

    
with open('day20.txt') as f:
    raw = f.read()

maze = parse(raw)

print(shortest_path(maze))