import sys

data = [l.strip() for l in sys.stdin.readlines()]


def parse_line(line: str) -> tuple[set[int], set[int]]:
    _, line = line.split(": ")
    winning, numbers = line.split(" | ")
    return (set(int(i) for i in winning.split()), set(int(i) for i in numbers.split()))


def matches(winning: set[int], numbers: set[int]) -> int:
    return len(winning.intersection(numbers))


def worth(matches: int) -> int:
    if matches == 0:
        return 0
    return 2 ** (matches - 1)


cards = map(parse_line, data)

match_counts = list(matches(winning, numbers) for winning, numbers in cards)

points = sum(worth(count) for count in match_counts)

print("Part 1:", points)

card_duplicates = list(0 for _ in range(len(match_counts)))

processed_cards = card_duplicates[:]

duplicates = list(reversed(range(len(match_counts))))

amount = len(match_counts)

# TODO heap
while len(duplicates) > 0:
    card = duplicates.pop()

    duplicate_amount = match_counts[card]
    amount += duplicate_amount

    duplicates.extend(i for i in range(card + 1, card + 1 + duplicate_amount))

print("Part 2:", amount)
