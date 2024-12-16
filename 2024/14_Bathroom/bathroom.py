import sys
from dataclasses import dataclass
from typing import Iterable


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

    def __mod__(self, other) -> "coord":
        if type(other) in (int, float):
            return coord(self.x % other, self.y % other)
        return coord(self.x % other.x, self.y % other.y)
    
    def __repr__(self):
        return f"(x={self.x},y={self.y})"

dim = coord(101, 103)
halfdim = coord(dim.x // 2, dim.y // 2)

def parse(line) -> tuple[coord, coord]:
    [ps, vs] = line.split()
    [px, py] = ps[2:].split(",")
    [vx, vy] = vs[2:].split(",")
    return (coord(int(px), int(py)), coord(int(vx), int(vy)))

def safety_factor(points: Iterable[coord]) -> int:
    ne = 0
    se = 0
    nw = 0
    sw = 0
    for p in points:
        if p.x < halfdim.x:
            if p.y < halfdim.y:
                nw += 1
            elif p.y > halfdim.y:
                sw += 1
        elif p.x > halfdim.x:
            if p.y < halfdim.y:
                ne += 1
            elif p.y > halfdim.y:
                se += 1
    print(nw, ne, sw, se)
    return ne*se*nw*sw

def debug(points: set[coord]) -> str:
    return "\r".join(
        "".join(
            "*" if coord(x, y) in points else " " for x in range(dim.x)
        )
        for y in range(dim.y)
    )

if __name__ == '__main__':
    data = [parse(line) for line in sys.stdin.readlines()]
    if (len(data) < 100):
        dim = coord(11, 7)
        halfdim = coord(dim.x // 2, dim.y // 2)
    part1 = [(p + v * 100) % dim for p, v in data]
    print(debug(part1))
    print("Part 1:", safety_factor(part1))