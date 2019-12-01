"""
Fuel required to launch a given module is based on its mass. 
Specifically, to find the fuel required for a module, take its mass, 
divide by three, round down, and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
"""
def fuel(mass: int) -> int:
    return mass //                                                                                                                                                                                                                                                                                                                                                                           3 - 2

assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756)                                                                                                                                                                                                                                                                                                                                                                             == 33583

with open('input.txt') as f:
    masses = [int(line.strip()) for line in f]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    part1 = sum(fuel(mass) for mass in masses)

print(part1)

# For part2 we want to add fuel for the fuel, etc

def fuel_for_the_fuel(mass: int) -> int:
    """We need fuel for the fuel, fuel for that fuel, etc"""
    total = 0

    next_fuel = fuel(mass)

    while next_fuel > 0:
        total += next_fuel
        next_fuel = fuel(next_fuel)

    return total

assert fuel_for_the_fuel(14) == 2
assert fuel_for_the_fuel(1969) == 966
assert fuel_for_the_fuel(100756) == 50346

part2 = sum(fuel_for_the_fuel(mass) for mass in masses)
print(part2)