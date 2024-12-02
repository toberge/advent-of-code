import sys
import itertools
data = [(int(l[0]), int(l[1])) for l in (line.split() for line in sys.stdin.readlines())]
left = sorted([x for x, _ in data])
right = sorted([x for _, x in data])
part1 = sum(abs(a - b) for a, b in zip(left, right))
print(part1)

from collections import Counter

counts = Counter(right)
part2 = sum(a * counts[a] for a in left)
print(part2)