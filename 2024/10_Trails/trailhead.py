import sys
from functools import cached_property, reduce
from itertools import product
from dataclasses import dataclass

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

DELTAS = (coord(-1, 0), coord(0, -1), coord(1, 0), coord(0, 1))

@dataclass
class Node:
    val: int
    pos: coord

    # TODO cache?
    # @cached_property
    @property
    def ascending_neighbours(self):
        # print(self.val, self.pos)
        for delta in DELTAS:
            npos = self.pos + delta
            if not (0 <= npos.x < xlen and 0 <= npos.y < ylen):
                continue
            cand = map[npos.y][npos.x]
            if cand.val == self.val + 1:
                yield cand

    def rating(self) -> int:
        if self.val == 9:
            # print(9, self.pos, "END")
            return 1
        return sum(n.rating() for n in self.ascending_neighbours)

    def score(self) -> set[coord]:
        if self.val == 9:
            # print(9, self.pos, "END")
            return {self.pos}
        res = set()
        for n in self.ascending_neighbours:
            res.update(n.score())
        return res
        return set().union(n.soccer() for n in self.ascending_neighbours)
        return reduce(set.union, list(self.ascending_neighbours), set())


map = [[Node(-9 if c == "." else int(c), coord(x, y)) for x, c in enumerate(l.rstrip())] for y, l in enumerate(sys.stdin.readlines())]
ylen = len(map)
xlen = len(map[0])

starts = [map[y][x] for y, x in product(range(ylen), range(xlen)) if map[y][x].val == 0]
# res = list((n.pos, len(n.score()), n.score()) for n in starts)
# print("\n".join(str(r) for r in res))
print(sum(len(n.score()) for n in starts))
print(sum(n.rating() for n in starts))
# print(map[6][0].soccer())
# print(map[3][4], list(map[3][4].ascending_neighbours))
# scores = [map[y][x].score for x, y in product(range(xlen), range(ylen))]
# print(scores, sum(scores))
