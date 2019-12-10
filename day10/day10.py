from typing import List, Dict, NamedTuple, Tuple, Iterator
import math
from collections import defaultdict

class Asteroid(NamedTuple):
    x: int
    y: int

Asteroids = List[Asteroid]

def parse(raw: str) -> Asteroids:
    return [
        Asteroid(x, y)
        for y, line in enumerate(raw.strip().split("\n"))
        for x, c in enumerate(line)
        if c == '#'
    ]


def count_visible(asteroids: Asteroids, station: Asteroid) -> int:
    # recenter
    slopes = set()
    for x, y in asteroids:
        dx = x - station.x
        dy = y - station.y

        gcd = math.gcd(dx, dy)

        if dx == dy == 0:
            pass
        else:
            slopes.add((dx / gcd, dy / gcd))
    return len(slopes)

def best_station(asteroids: Asteroids) -> Tuple[Asteroid, int]:
    results = [(a, count_visible(asteroids, a)) for a in asteroids]
    return max(results, key=lambda pair: pair[1])

RAW = """.#..#
.....
#####
....#
...##"""

ASTEROIDS = parse(RAW)

assert best_station(ASTEROIDS) == (Asteroid(3, 4), 8)

A2 = parse("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""")

assert best_station(A2) == (Asteroid(5, 8), 33)

A3 = parse(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""")

assert best_station(A3) == (Asteroid(11, 13), 210)


asteroids = parse("""##.###.#.......#.#....#....#..........#.
....#..#..#.....#.##.............#......
...#.#..###..#..#.....#........#......#.
#......#.....#.##.#.##.##...#...#......#
.............#....#.....#.#......#.#....
..##.....#..#..#.#.#....##.......#.....#
.#........#...#...#.#.....#.....#.#..#.#
...#...........#....#..#.#..#...##.#.#..
#.##.#.#...#..#...........#..........#..
........#.#..#..##.#.##......##.........
................#.##.#....##.......#....
#............#.........###...#...#.....#
#....#..#....##.#....#...#.....#......#.
.........#...#.#....#.#.....#...#...#...
.............###.....#.#...##...........
...#...#.......#....#.#...#....#...#....
.....#..#...#.#.........##....#...#.....
....##.........#......#...#...#....#..#.
#...#..#..#.#...##.#..#.............#.##
.....#...##..#....#.#.##..##.....#....#.
..#....#..#........#.#.......#.##..###..
...#....#..#.#.#........##..#..#..##....
.......#.##.....#.#.....#...#...........
........#.......#.#...........#..###..##
...#.....#..#.#.......##.###.###...#....
...............#..#....#.#....#....#.#..
#......#...#.....#.#........##.##.#.....
###.......#............#....#..#.#......
..###.#.#....##..#.......#.............#
##.#.#...#.#..........##.#..#...##......
..#......#..........#.#..#....##........
......##.##.#....#....#..........#...#..
#.#..#..#.#...........#..#.......#..#.#.
#.....#.#.........#............#.#..##.#
.....##....#.##....#.....#..##....#..#..
.#.......#......#.......#....#....#..#..
...#........#.#.##..#.#..#..#........#..
#........#.#......#..###....##..#......#
...#....#...#.....#.....#.##.#..#...#...
#.#.....##....#...........#.....#...#...""")

# print(best_station(asteroids))

def faux_angle(asteroid):
    dx, dy = asteroid
    if dx == 0 and dy < 0:
        # e.g. (0, -1), straight up
        return (0, 0)
    elif dx > 0 and dy < 0:
        # e.g. (0.1, -0.9) or (0.9, -0.1)
        return (1, dx / abs(dy))
    elif dx > 0 and dy == 0:
        return (2, 0)
    elif dx > 0 and dy > 0:
        # e.g. (0.9, 0.1) or (0.1, 0.9)
        return (3, dy / dx)
    elif dx == 0 and dy > 0:
        return (4, 0)
    elif dx < 0 and dy > 0:
        # e.g. (-0.1, 0.9) or (-0.9, 0.1)
        return (5, abs(dx) / dy)
    elif dx < 0 and dy == 0:
        return (6, 0)
    elif dx < 0 and dy < 0:
        # e.g. (-0.9, -0.1) or (-0.1, -0.9)
        return (7, dy / dx)

def iterate(asteroids: Asteroids, station: Asteroid) -> Iterator[Asteroid]:
    asteroids_by_angle = defaultdict(list)

    for x, y in asteroids:
        dx = x - station.x
        dy = y - station.y

        gcd = math.gcd(dx, dy)

        if dx == dy == 0:
            pass
        else:
            angle = (dx / gcd, dy / gcd)
            asteroids_by_angle[angle].append(Asteroid(x, y))

    # sort by length descending for each angle
    for angle_asteroids in asteroids_by_angle.values():
        angle_asteroids.sort(key=lambda a: abs(a.x - station.x) + abs(a.y - station.y), reverse=True)

    while asteroids_by_angle:
        keys = asteroids_by_angle.keys()  # (dx, dy)
        keys = sorted(keys, key=faux_angle)

        for key in keys:
            angle_asteroids = asteroids_by_angle[key]
            yield angle_asteroids.pop()
            if not angle_asteroids:
                del asteroids_by_angle[key]

NEW_ASTEROIDS = parse(""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""")

NEW_STATION = Asteroid(8, 3)

station = best_station(asteroids)[0]
vaporizations = list(iterate(asteroids, station))

print(vaporizations[199])
