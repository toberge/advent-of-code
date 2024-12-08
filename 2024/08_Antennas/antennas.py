import sys
from itertools import combinations
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class coord:
    x: int
    y: int

    def __add__(self, other) -> "coord":
        return coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "coord":
        return coord(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> "coord":
        if type(other) in (int, float):
            return coord(self.x * other, self.y * other)
        return coord(self.x + other.x, self.y + other.y)

    def __rmul__(self, other) -> "coord":
        return self.__mul__()

    def __div__(self, other) -> "coord":
        if type(other) in (int, float):
            return coord(self.x // other, self.y // other)
        raise NotImplementedError()

    def __neg__(self) -> "coord":
        return coord(-self.x, -self.y)


class Map:
    def __init__(self, data: list[list[str]]):
        self.data = data
        self.antennas = defaultdict(set)
        self.antinodes = set()
        self.dim = coord(len(data[0]), len(data))
        for y in range(self.dim.y):
            for x in range(self.dim.x):
                if data[y][x] != ".":
                    self.antennas[data[y][x]].add(coord(x, y))

    def within_bounds(self, p: coord) -> bool:
        return 0 <= p.x < self.dim.x and 0 <= p.y < self.dim.y

    def add_antinode(self, antinode: coord):
        if self.within_bounds(antinode):
            self.antinodes.add(antinode)

    def add_antinode_resonance(self, p, delta: coord):
        while self.within_bounds(p):
            self.antinodes.add(p)
            p += delta

    def simple_antinodes(self):
        for name, positions in self.antennas.items():
            for a, b in combinations(positions, 2):
                delta = a - b
                self.add_antinode(a + delta)
                self.add_antinode(b - delta)
        return len(self.antinodes)

    def resonant_antinodes(self):
        for name, positions in self.antennas.items():
            for a, b in combinations(positions, 2):
                delta = a - b
                self.add_antinode_resonance(a, delta)
                self.add_antinode_resonance(b, -delta)
        return len(self.antinodes)


if __name__ == "__main__":
    m = Map(list(l.strip() for l in sys.stdin.readlines()))
    print("Part 1:", m.simple_antinodes())
    print("Part 2:", m.resonant_antinodes())
