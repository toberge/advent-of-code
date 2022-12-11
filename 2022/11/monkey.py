import sys
from itertools import takewhile
from math import floor
from functools import reduce


class Monkey:
    def __init__(self, lines: list[str]) -> None:
        self.index = int(lines[0].split()[1][:-1])
        self.items = [int(item) for item in lines[1][18:].split(", ")]
        self.operation = " ".join(lines[2].split()[3:])
        self.divisible_by = int(lines[3].split()[-1])
        self.throw_if_true = int(lines[4].split()[-1])
        self.throw_if_false = int(lines[5].split()[-1])
        self.items_inspected = 0
        # Set this outside __init__
        self.common_divisor = -1

    def perform_operation(self, old) -> int:
        """Part 1: As simple as it says on the tin. Abuse eval()."""
        return floor(eval(self.operation) // 3)

    def inspect(self) -> None:
        self.items = [self.perform_operation(item) for item in self.items]
        self.items_inspected += len(self.items)

    def perform_operation_while_worried(self, old) -> int:
        """Part 2: The relevant aspect of worry level is divisibility by the monkeys' divisors.
        Therefore, we should keep worry levels within the common divisor of all the monkeys.
        """
        return eval(self.operation) % self.common_divisor

    def inspect_while_worried(self) -> None:
        self.items = [self.perform_operation_while_worried(item) for item in self.items]
        self.items_inspected += len(self.items)

    def prepare_throw(self) -> tuple[list[int], list[int]]:
        true = [item for item in self.items if item % self.divisible_by == 0]
        false = [item for item in self.items if item % self.divisible_by != 0]
        self.items = []
        return true, false

    def __repr__(self) -> str:
        return (
            f"Monkey [{self.index}]\n"
            f"items: {self.items}, new = {self.operation}\n"
            f"div by {self.divisible_by}: true -> {self.throw_if_true}, false -> {self.throw_if_false}"
        )


part_two = True

lines = (l.rstrip() for l in sys.stdin)
monkeys = []

try:
    while True:
        monkeys.append(Monkey(list(takewhile(lambda l: l != "", lines))))
        print(monkeys[-1], end="\n\n")
except StopIteration:
    pass
except IndexError:
    pass

common_divisor = reduce(
    lambda a, b: a * b, (monke.divisible_by for monke in monkeys), 1
)

for monke in monkeys:
    monke.common_divisor = common_divisor

for round_ in range(10_000 if part_two else 20):
    for monke in monkeys:
        if part_two:
            monke.inspect_while_worried()
        else:
            monke.inspect()
        [true, false] = monke.prepare_throw()
        monkeys[monke.throw_if_true].items.extend(true)
        monkeys[monke.throw_if_false].items.extend(false)

most_active_monkeys = sorted(monkeys, key=lambda m: m.items_inspected)[-2:]

print(
    "Part",
    "2" if part_two else "1",
    most_active_monkeys[0].items_inspected * most_active_monkeys[1].items_inspected,
)
