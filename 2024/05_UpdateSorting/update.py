from collections import defaultdict
from functools import cmp_to_key

before = defaultdict(set)
after = defaultdict(set)

line = input()
while len(line) > 0:
    [a, b] = line.split("|")
    before[b].add(a)
    after[a].add(b)
    line = input()
import sys

updates = [l.strip().split(",") for l in sys.stdin.readlines()]


def is_sorted(u: list[str]):
    for i, v in enumerate(u):
        if any(b in after[v] for b in u[:i]) or any(a in before[v] for a in u[i + 1 :]):
            return False
    return True


def compare(a, b):
    if a == b:
        return 0
    if a in before[b]:
        return -1
    return 1


def middle(u):
    return int(u[len(u) // 2])


part1 = 0
part2 = 0
for u in updates:
    if is_sorted(u):
        part1 += middle(u)
    else:
        uu = sorted(u, key=cmp_to_key(compare))
        part2 += middle(uu)
print("Part 1:", part1)
print("Part 2:", part2)
