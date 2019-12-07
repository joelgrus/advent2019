"""
If we build a tree, each thing orbits its ancestors, 
so we need to count the total number of ancestors
"""

from typing import NamedTuple, List, Dict
from collections import defaultdict

RAW = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

class Orbit(NamedTuple):
    parent: str
    child: str

    @staticmethod
    def from_string(s: str) -> 'Orbit':
        parent, child = s.strip().split(")")
        return Orbit(parent, child)

ORBITS = [Orbit.from_string(s) for s in RAW.strip().split("\n")]

def make_tree(orbits: List[Orbit]) -> Dict[str, str]:
    parents = {}
    for parent, child in orbits:
        parents[child] = parent
    return parents

def count_ancestors(child: str, parents: Dict[str, str]) -> int:
    count = 0
    while child != "COM":
        count += 1
        child = parents[child]
    return count

PARENTS = make_tree(ORBITS)

assert count_ancestors('D', PARENTS) == 3
assert count_ancestors('L', PARENTS) == 7
assert count_ancestors('COM', PARENTS) == 0

def total_ancestors(orbits: List[Orbit]) -> int:
    parents = make_tree(orbits)

    return sum(count_ancestors(child, parents) for child in parents)

assert total_ancestors(ORBITS) == 42

with open('input.txt') as f:
    orbits = [Orbit.from_string(line) for line in f]

# print(total_ancestors(orbits))


def path_to_com(child: str, parents: Dict[str, str]) -> List[str]:
    path = [child]

    while child != "COM":
        child = parents[child]
        path.append(child)

    return path

assert path_to_com('I', PARENTS) == ['I', 'D', 'C', 'B', 'COM']

def shortest_path(child1: str, child2: str, parents: Dict[str, str]) -> int:
    path1 = path_to_com(child1, parents)
    path2 = path_to_com(child2, parents)

    # J, E, D, C, B, COM
    #    I, D, C, B, COM

    while path1 and path2 and path1[-1] == path2[-1]:
        path1.pop()
        path2.pop()

    return len(path1) + len(path2)

assert shortest_path('I', 'K', PARENTS) == 4
assert shortest_path('H', 'F', PARENTS) == 6

parents = make_tree(orbits)
print(shortest_path(parents['YOU'], parents['SAN'], parents))