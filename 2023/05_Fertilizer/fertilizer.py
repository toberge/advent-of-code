import sys
from dataclasses import dataclass
from itertools import islice
from typing import TypeAlias


# batched from 3.12:
def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


Split: TypeAlias = tuple[int, int]


@dataclass
class Translation:
    from_input: int
    from_output: int
    length: int

    @property
    def end_input(self):
        return self.from_input + self.length

    def should_translate(self, number: int) -> int:
        return number >= self.from_input and number < self.from_input + self.length

    def translate(self, number: int) -> int:
        return self.from_output + (number - self.from_input)

    def should_split(self, split: Split) -> int:
        start, count = split
        return not (self.end_input < start or start + count <= self.from_input)

    def split(self, split: Split) -> tuple[Split, Split, Split]:
        # TODO doesn't handle above!
        start, length = split
        count_below = max(self.from_input - start, 0)
        below = (start, count_below)
        count_inside = max(length - count_below, self.length)
        inside = (self.translate(start + count_below), count_inside)
        above = (
            start + count_below + count_inside,
            length - count_inside - count_below,
        )
        return below, inside, above
        # translate start of resulting splits


def parse_map(lines: list[str]) -> list[Translation]:
    print(lines)
    translations = []
    for line in lines[1:]:
        # This was the opposite order of what I assumed
        [from_output, from_input, length] = [int(i) for i in line.split()]
        translations.append(Translation(from_input, from_output, length))
    return translations


if __name__ == "__main__":
    data = sys.stdin.read().strip()
    sections = data.split("\n\n")
    seeds = [int(i) for i in sections[0].split()[1:]]
    ranges = list(batched(seeds, n=2))
    print(ranges)
    # TODO should be possible to just
    maps = [parse_map(section.split("\n")) for section in sections[1:]]
    print(maps)
    locations = []
    for s in seeds:
        print("From", s, end="")
        for m in maps:
            for t in m:
                if t.should_translate(s):
                    s = t.translate(s)
                    print(" ->", s, end="")
                    break
        print()
        locations.append(s)
    print("Part 1:", min(locations))

    # Kinda bruteforce
    answer = 100000000000000
    for r in ranges:
        splits = [r]
        for m in maps:
            for t in m:
                new_splits = []
                for split in splits:
                    # print("From", s, end="")
                    if t.should_split(split):
                        # TODO needs to handle above/below omg
                        below, new_split, above = t.split(split)
                        print(split, t, " - >", below, new_split, above)
                        new_splits.append(below)
                        new_splits.append(new_split)
                        new_splits.append(above)
                        # print(" ->", s, end="")
                    else:
                        new_splits.append(split)
                splits = [s for s in new_splits if s[1] > 0]
            # print()
        answer = min(answer, *(start for start, _ in splits))
    print("Part 2:", answer)
