import sys
from itertools import accumulate, cycle

nums = [int(s.replace("+", "")) for s in open(sys.argv[1] or "example.dat").readlines()]

found = set()

# for n in cycle(accumulate(nums)):
# and then I realized where I went wrong
for n in accumulate(cycle(nums)):
    if n in found:
        print(n)
        break
    found.add(n)
