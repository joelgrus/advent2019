from typing import NamedTuple, List
import math

class Amount(NamedTuple):
    chemical: str
    quantity: int

    @staticmethod 
    def from_string(raw: str) -> 'Amount':
        qty, chemical = raw.strip().split(" ")
        return Amount(chemical, int(qty))

class Rule(NamedTuple):
    inputs: List[Amount]
    output: Amount

# 

def parse_rule(raw: str) -> Rule:
    lhs, rhs = raw.split(" => ")
    inputs = lhs.split(", ")
    input_amounts = [Amount.from_string(inp) for inp in inputs]
    output_amount = Amount.from_string(rhs)
    return Rule(input_amounts, output_amount)

assert parse_rule("7 A, 1 D => 1 E") == Rule([Amount("A", 7), Amount("D", 1)], Amount("E", 1))

RAW = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

RULES = [parse_rule(raw) for raw in RAW.split("\n")]


with open('day14.txt') as f:
    raw = f.read()
rules = [parse_rule(line) for line in raw.split("\n")]

def least_ore(rules: List[Rule], fuel_needed: int = 1):
    rules_by_product = {rule.output.chemical: rule for rule in rules}

    requirements = {"FUEL": fuel_needed}
    ore_needed = 0

    def done() -> bool:
        return all(qty <= 0 for qty in requirements.values())


    while not done():
        key = next(iter(chem for chem, qty in requirements.items() if qty > 0))
        qty_needed = requirements[key]

        rule = rules_by_product[key]
        # let's say I need 5 but the rule produces 3, then I need to run the rule twice
        num_times = math.ceil(qty_needed / rule.output.quantity)
        requirements[key] -= num_times * rule.output.quantity

        for amount in rule.inputs:
            if amount.chemical == "ORE":
                ore_needed += amount.quantity * num_times
            else:
                requirements[amount.chemical] = requirements.get(amount.chemical, 0) + num_times * amount.quantity
        
    return ore_needed

RAW2 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

RULES2 = [parse_rule(raw) for raw in RAW2.split("\n")]


print(least_ore(rules))

lo = 1000000
hi = 10000000    
ore_lo = least_ore(rules, lo)
ore_hi = least_ore(rules, hi)

t = 1_000_000_000_000

while lo < hi:
    mid = (lo + hi) // 2
    
    ore_mid = least_ore(rules,mid)

    print(lo, mid, hi)
    print(ore_lo, ore_mid, ore_hi)

    if ore_mid <= t:
        lo, ore_lo = mid, ore_mid
    else:
        hi, ore_hi = mid, ore_mid

