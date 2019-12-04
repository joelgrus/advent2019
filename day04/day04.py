"""
It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
"""
from typing import List
from collections import Counter

def digits(n: int, num_digits: int = 6) -> List[int]:
    d = []
    for _ in range(num_digits):
        d.append(n % 10)
        n = n // 10
    return list(reversed(d))

assert digits(123) == [0, 0, 0, 1, 2, 3]
assert digits(594383) == [5, 9, 4, 3, 8, 3]

def is_increasing(ds: List[int]) -> bool:
    return all(x <= y for x, y in zip(ds, ds[1:]))

def adjacent_same(ds: List[int]) -> bool:
    return any(x == y for x, y in zip(ds, ds[1:]))

def is_valid(n: int) -> bool:
    d = digits(n)
    return is_increasing(d) and adjacent_same(d)

def has_group_of_two(ds: List[int]) -> bool:
    counts = Counter(ds)
    return any(v == 2 for v in counts.values())

def is_valid2(n: int) -> bool:
    d = digits(n)
    return is_increasing(d) and has_group_of_two(d)

assert is_valid(111111)
assert not is_valid(223450)
assert is_valid(223459)
assert not is_valid(123789)

LO = 372304
HI = 847060

# print(sum(is_valid(d) for d in range(LO, HI+1)))

def is_valid2(n: int) -> bool:
    d = digits(n)
    return is_increasing(d) and has_group_of_two(d)

assert is_valid2(112233)
assert not is_valid2(123444)
assert is_valid2(111122)

print(sum(is_valid2(d) for d in range(LO, HI+1)))