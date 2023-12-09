import sys
from dataclasses import dataclass, field
from itertools import islice
from typing import TypeAlias, Iterable, Union


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
    end_input: int = field(init=False)
    from_output: int
    length: int

    def __post_init__(self):
        self.end_input = self.from_input + self.length

    def should_translate(self, number: int) -> int:
        return number >= self.from_input and number < self.from_input + self.length

    def translate(self, number: int) -> int:
        return self.from_output + (number - self.from_input)

    def should_split(self, split: Split) -> int:
        start, count = split
        return not (self.end_input < start or start + count <= self.from_input)

    def split(
        self, split: Split
    ) -> tuple[Union[None, Split], Split, Union[None, Split]]:
        start, count = split
        below = None
        above = None
        if start < self.from_input:
            below = (start, self.from_input - start)
            start = self.from_input
            count -= self.from_input - start
        inside = (t.translate(start), min(count, self.end_input - start))
        if start + count >= self.end_input:
            above = (self.end_input, start + count - self.end_input)
        return below, inside, above

    def __lt__(self, other: "Translation") -> bool:
        return self.from_input < other.from_input


def parse_map(lines: list[str]) -> list[Translation]:
    translations = []
    for line in lines[1:]:
        # This was the opposite order of what I assumed
        [from_output, from_input, length] = [int(i) for i in line.split()]
        translations.append(Translation(from_input, from_output, length))
    return sorted(translations)


def fst(split: Split) -> int:
    return split[0]


debug = False

if __name__ == "__main__":
    data = sys.stdin.read().strip()
    sections = data.split("\n\n")

    seeds = [int(i) for i in sections[0].split()[1:]]
    ranges = list(batched(seeds, n=2))
    maps = [parse_map(section.split("\n")) for section in sections[1:]]

    locations = []
    for s in seeds:
        if debug:
            print("From", s, end="")
        for map in maps:
            for t in map:
                if t.should_translate(s):
                    s = t.translate(s)
                    if debug:
                        print(" ->", s, end="")
                    break
        if debug:
            print()
        locations.append(s)
    print("Part 1:", min(locations))

    answer = 100000000000000
    splits = sorted(ranges, key=fst)
    if debug:
        print(splits)
    for m in maps:
        isplits = iter(splits)
        itrans = 0
        split = next(isplits)
        new_splits = []
        try:
            while itrans < len(m):
                t = m[itrans]
                if debug:
                    print(t)
                    print(split)

                if t.should_split(split):
                    # inside: should split and keep the last one (if any) as the next split, then continue
                    below, inside, above = t.split(split)
                    if debug:
                        print("Splitting", split, "->", below, inside, above)
                    if below is not None:
                        new_splits.append(below)
                    new_splits.append(inside)
                    if above is not None:
                        # split fully, continue
                        if itrans == len(m) - 1:
                            new_splits.append(above)
                        split = above
                        itrans += 1
                    else:
                        # split not fully, check next split
                        split = next(isplits)

                elif split[0] < t.from_input:
                    if debug:
                        print("Less, skipping")
                    # less: no need to split and should skip this split, try next split with same translation
                    new_splits.append(split)
                    split = next(isplits)

                else:
                    # more: should continue with the current split
                    if debug:
                        print("More, continuing")
                    if itrans == len(m) - 1:
                        new_splits.append(split)
                    itrans += 1
            # Fill in the remaining splits
            new_splits.extend(isplits)
        except StopIteration:
            if debug:
                print("Stopped at translation", itrans)

        splits = sorted(new_splits, key=fst)
        if debug:
            print()
            print("New set:", splits)

    answer = min(answer, *(start for start, _ in splits))
    print("Part 2:", answer)
