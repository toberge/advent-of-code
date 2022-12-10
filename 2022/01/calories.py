import sys

elves = [0]

for line in sys.stdin.readlines():
    if len(line) > 1:
        elves[-1] += int(line)
    else:
        elves.append(0)

print("Part 1:", max(elves))
print("Part 2:", sum(sorted(elves)[-3:]))
