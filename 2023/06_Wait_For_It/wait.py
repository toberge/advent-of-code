"""
Boils down to:
(budget - wait) * wait > record

Let's say we wanna match it, so:
(b - x) * x = r
-x^2 + bx - r = 0

Quadratic formula gives us:
b/2 +/- sqrt(b^2 + 4r)/2
"""

from math import ceil, floor, sqrt
from functools import reduce
from operator import mul


def beatage(budget, record):
    constant = budget / 2
    plusminus = sqrt(budget**2 - 4 * record) / 2
    lower = ceil(constant - plusminus + 0.1)
    upper = floor(constant + plusminus - 0.1)
    # print(constant, plusminus, constant - plusminus, constant + plusminus)
    # print(lower, upper)
    return upper - lower + 1


budgets = [int(i) for i in input().split()[1:]]
records = [int(i) for i in input().split()[1:]]
single_budget = int("".join(str(i) for i in budgets))
single_record = int("".join(str(i) for i in records))

results = [beatage(b, r) for b, r in zip(budgets, records)]

print(results)
print("Part 1:", reduce(mul, results))
print("Part 2:", beatage(single_budget, single_record))
