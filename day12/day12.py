from typing import NamedTuple, List
from dataclasses import dataclass
import copy

@dataclass
class XYZ:
    x: int
    y: int
    z: int

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon:
    def __init__(self, position: XYZ, velocity: XYZ = None) -> None:
        self.position = position
        self.velocity = velocity or XYZ(0, 0, 0)

    def __repr__(self) -> str:
        return f"Moon(position={self.position}, velocity={self.velocity})"

    def potential_energy(self) -> int:
        return self.position.energy()

    def kinetic_energy(self) -> int:
        return self.velocity.energy()

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()

    def apply_velocity(self) -> None:
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def sig_x(self):
        return (self.position.x, self.velocity.x)

    def sig_y(self):
        return (self.position.y, self.velocity.y)

    def sig_z(self):
        return (self.position.z, self.velocity.z)


def step(moons: List[Moon]) -> None:
    # first apply acceleration
    n = len(moons)
    for moon1 in moons:
        for moon2 in moons:
            if moon1 != moon2:
                # adjust the velocity of moon1
                if moon1.position.x < moon2.position.x:
                    moon1.velocity.x += 1
                elif moon1.position.x > moon2.position.x:
                    moon1.velocity.x -= 1

                if moon1.position.y < moon2.position.y:
                    moon1.velocity.y += 1
                elif moon1.position.y > moon2.position.y:
                    moon1.velocity.y -= 1

                if moon1.position.z < moon2.position.z:
                    moon1.velocity.z += 1
                elif moon1.position.z > moon2.position.z:
                    moon1.velocity.z -= 1

    # next apply velocity
    for moon in moons:
        moon.apply_velocity()

MOONS = [
    Moon(XYZ(-1, 0, 2)),
    Moon(XYZ(2, -10, -7)),
    Moon(XYZ(4, -8, 8)),
    Moon(XYZ(3, 5, -1))
]


moons = [
    Moon(XYZ(0, 4, 0)),
    Moon(XYZ(-10, -6, -14)),
    Moon(XYZ(9, -16, -3)),
    Moon(XYZ(6, -1, 2))
]

def sig_x(moons: List[Moon]):
    return tuple(moon.sig_x() for moon in moons)

def sig_y(moons: List[Moon]):
    return tuple(moon.sig_y() for moon in moons)

def sig_z(moons: List[Moon]):
    return tuple(moon.sig_z() for moon in moons)


def steps_to_repeat(moons: List[Moon], sig_fn) -> int:
    moons = copy.deepcopy(moons)

    seen = set()
    seen.add(sig_fn(moons))

    num_steps = 0

    while True:
        num_steps += 1
        step(moons)
        sig = sig_fn(moons)
        if sig in seen:
            return num_steps
        else:
            seen.add(sig)

print(steps_to_repeat(moons, sig_x))
print(steps_to_repeat(moons, sig_y))
print(steps_to_repeat(moons, sig_z))
