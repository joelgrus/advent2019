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

    portal_neighbors = defaultdict(list)
    neighbor_portals = defaultdict(list)

    # find start and end
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                for loc in neighbors(XY(i, j), deltas2):
                    for portal, locs in portals.items():
                        if loc in locs:
                            portal_neighbors[portal].append(XY(i, j))
                            neighbor_portals[XY(i, j)].append(portal)
    
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
                        neighbor_dict[loc].append(loc2)
                # get portal neighbors
                for portal in neighbor_portals.get(loc, []):
                    for nbor in portal_neighbors[portal]:
                        if nbor != loc:
                            neighbor_dict[loc].append(nbor)

    return Maze(start=portal_neighbors['AA'][0],
                end=portal_neighbors['ZZ'][0],
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
    visited = {maze.start}
    q = deque([(maze.start, 0)])



    while q:
        loc, num_steps = q.popleft()

        for nbor in maze.neighbors[loc]:
            if nbor == maze.end:
                return num_steps + 1

            if nbor not in visited:
                visited.add(nbor)
                q.append((nbor, num_steps + 1))

    
with open('day20.txt') as f:
    raw = f.read()

maze = parse(raw)

print(shortest_path(maze))