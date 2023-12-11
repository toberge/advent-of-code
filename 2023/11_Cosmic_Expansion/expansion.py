import sys
from dataclasses import dataclass
from itertools import combinations


@dataclass
class coord:
    x: int
    y: int

    def __add__(self, other: "coord") -> "coord":
        return coord(self.x + other.x, self.y + other.y)

    def distance(self, other: "coord") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def move(self, delta: "coord"):
        self.x += delta.x
        self.y += delta.y


class GalaxyHeap:
    def __init__(self, lines: list[str]):
        self.galaxies = []
        self.empty_lines = set(range(len(lines)))
        self.empty_cols = set(range(len(lines)))
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self.galaxies.append(coord(x, y))
                    if y in self.empty_lines:
                        self.empty_lines.remove(y)
                    if x in self.empty_cols:
                        self.empty_cols.remove(x)

    def expand(self, amount: int):
        delta = coord(0, amount)
        for i, y in enumerate(sorted(self.empty_lines)):
            actual_y = y + i * amount
            for g in self.galaxies:
                if g.y >= actual_y:
                    g.move(delta)

        delta = coord(amount, 0)
        for i, x in enumerate(sorted(self.empty_cols)):
            actual_x = x + i * amount
            for g in self.galaxies:
                if g.x >= actual_x:
                    g.move(delta)

    def all_distances(self) -> int:
        return sum(a.distance(b) for a, b in combinations(self.galaxies, 2))


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin.readlines()]

    galaxy_heap = GalaxyHeap(lines)
    galaxy_heap.expand(1)
    distances = galaxy_heap.all_distances()
    print("Part 1:", distances)

    galaxy_heap = GalaxyHeap(lines)
    galaxy_heap.expand(1000000 - 1)
    distances = galaxy_heap.all_distances()
    print("Part 2:", distances)
