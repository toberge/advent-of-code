import sys

cycle = 1
x = 1
strength = 0

crt = [40 * ["."] for _ in range(6)]


def signal_strength(cycle_):
    if (cycle_ - 20) % 40 == 0:
        return (cycle_) * x
    return 0


def display():
    print("\n".join("".join(row) for row in crt))


def update_display(cycle_):
    cycle_ -= 1
    if cycle_ % 40 in [x - 1, x, x + 1]:
        crt[cycle_ // 40][cycle_ % 40] = "#"


for line in sys.stdin:
    update_display(cycle)
    if line.startswith("noop"):
        cycle += 1
    else:
        [_, value] = line.split()
        # Since addx-es are 2 cycles long
        update_display(cycle + 1)
        strength += signal_strength(cycle + 1)
        cycle += 2
        x += int(value)
    strength += signal_strength(cycle)

print("Part 1:", strength)

print("Part 2:")
display()
