import sys

stacks = []

lines = (l.rstrip("\n") for l in sys.stdin)

for line in lines:
    if line == "":
        break

    values = [w[1:-1] for w in line.split()]

    if len(values) > len(stacks):
        stacks.extend([[]] * (len(values) - len(stacks)))

    for i, value in enumerate(values):
        stacks[i].append(value)

stacks = [list(x for x in reversed(stack) if x != "") for stack in stacks]

# Ok screw it all I'm not writing a parser :)

# Test stacks
stacks = [["Z", "N"], ["M", "C", "D"], ["P"]]
stacks = [
    list(s)
    for s in [
        "QEMRLWCV",
        "DQL",
        "PSRGWCNB",
        "LCDHBOG",
        "VGLEZS",
        "DGNP",
        "DZPVECW",
        "CPDMS",
        "ZNWTVMPC",
    ]
]

for line in lines:
    [count, source, destination] = [int(l) for l in line.split() if l.isnumeric()]
    # Part 1
    # stacks[destination - 1].extend(reversed(stacks[source - 1][-count:]))
    # Part 2
    stacks[destination - 1].extend(stacks[source - 1][-count:])
    del stacks[source - 1][-count:]

print("Part X:", "".join([stack[-1] for stack in stacks]))
