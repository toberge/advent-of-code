"""
Day 17: Conway Cubes

Incredibly performant code® (33.45 secs for part one and two)
After caching surrounding points: Less than 5 secs!

Time to implement: Less than two hours
"""

import sys
from functools import lru_cache
from itertools import product


def add(a: tuple, b: tuple):
    return tuple(x + y for x, y in zip(a, b))


def parse_grid(lines: [str], dim=3) -> {tuple}:
    if dim < 2:
        raise ValueError("Dimensions lower than 2D are not supported ({dim} < 2)")

    points = set()
    for y in range(len(lines)):
        for x in range(len(lines[0]) - 1):  # ignore newline
            if lines[y][x] == "#":
                points.add(tuple([x, y, *list(0 for _ in range(dim - 2))]))
    return points


class Life:
    """n-dimensional game of life"""

    def __init__(self, grid, dim=3):
        if dim < 2:
            raise ValueError("Dimensions lower than 2D are not supported ({dim} < 2)")
        self.points = parse_grid(grid, dim=dim)
        self.dim = dim
        self._deltas = list(
            filter(lambda t: any(i != 0 for i in t), product([-1, 0, 1], repeat=dim))
        )

    @lru_cache(maxsize=None)
    def _surrounding(self, point):
        return [add(point, delta) for delta in self._deltas]

    def _neighbours(self, point):
        return filter(lambda p: p in self.points, self._surrounding(point))

    def _disabled_neighbours(self, point):
        return filter(lambda p: p not in self.points, self._surrounding(point))

    def count(self):
        """Return the number of active points in the current generation"""
        return len(self.points)

    def progress(self):
        """Progress the state of life by one cycle"""
        activate = set()
        deactivate = set()

        for point in self.points:
            # First rule: Kill the living!
            count = len(list(self._neighbours(point)))
            if count < 2 or count > 3:
                deactivate.add(point)

            # Second rule: Awaken the dead!
            for disabled in self._disabled_neighbours(point):
                if len(list(self._neighbours(disabled))) == 3:
                    activate.add(disabled)

        # Apply the changes!
        self.points = (self.points - deactivate).union(activate)

    def __repr__(self):
        maxes = tuple(max(self.points, key=lambda p: p[i])[i] for i in range(self.dim))

        mins = tuple(min(self.points, key=lambda p: p[i])[i] for i in range(self.dim))

        if self.dim not in {3, 4}:
            raise ValueError(f"Dimension not implemented: {self.dim}")

        # TODO make this *not* hardcoded
        s = ""
        if self.dim == 3:
            for z in range(mins[2], maxes[2] + 1):
                s += f"z={z}\n"
                for y in range(mins[1], maxes[1] + 1):
                    for x in range(mins[0], maxes[0] + 1):
                        s += "#" if (x, y, z) in self.points else "."
                    s += "\n"
                s += "\n"
        else:
            for z in range(mins[2], maxes[2] + 1):
                for w in range(mins[3], maxes[3] + 1):
                    s += f"z={z}, w={w}\n"
                    for y in range(mins[1], maxes[1] + 1):
                        for x in range(mins[0], maxes[0] + 1):
                            s += "#" if (x, y, z, w) in self.points else "."
                        s += "\n"
                    s += "\n"

        return s


def main():
    lines = sys.stdin.readlines()

    # Part one
    life = Life(lines)
    print(life)
    for _ in range(6):
        life.progress()
    print(life.count())
    print()

    life = Life(lines, dim=4)
    print(life)
    for _ in range(6):
        life.progress()
    print(life.count())


if __name__ == "__main__":
    main()
