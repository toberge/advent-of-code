import sys
from itertools import chain


class Droplet:
    def __init__(self, points: set[tuple[int, int, int]]):
        self.points: set[tuple[int, int, int]] = points
        self.max = (
            max(p[0] for p in points),
            max(p[1] for p in points),
            max(p[2] for p in points),
        )
        self.min = (
            min(p[0] for p in points),
            min(p[1] for p in points),
            min(p[2] for p in points),
        )
        self.known_exterior = set()
        self.known_interior = set()

    def sides(self, point: tuple[int, int, int]):
        (x, y, z) = point
        # yield from (
        #    p
        #    for p in product([x - 1, x, x + 1], [y - 1, y, y + 1], [z - 1, z, z + 1])
        #    if p != point and p in self.points
        # )
        yield (x - 1, y, z)
        yield (x + 1, y, z)
        yield (x, y - 1, z)
        yield (x, y + 1, z)
        yield (x, y, z - 1)
        yield (x, y, z + 1)

    def all_sides(self):
        yield from chain.from_iterable(
            (side for side in self.sides(point) if side not in self.points)
            for point in self.points
        )

    def surface_area(self):
        return sum(
            len(list(side for side in self.sides(point) if side not in self.points))
            for point in self.points
        )

    def is_within_limits(self, point: tuple[int, int, int]) -> bool:
        return (
            self.min[0] <= point[0] <= self.max[0]
            and self.min[1] <= point[1] <= self.max[1]
            and self.min[2] <= point[2] <= self.max[2]
        )

    def is_contained(self, seed: tuple[int, int, int]) -> bool:
        stack = [seed]
        inspected = set()  # visited SET for a reason
        while len(stack) > 0:
            point = stack.pop()
            if point in self.known_interior:
                return True
            elif point in self.known_exterior:
                return False
            for side in (
                s
                for s in self.sides(point)
                if s not in self.points and s not in inspected
            ):
                if not self.is_within_limits(side):
                    self.known_exterior.update(inspected)
                    self.known_exterior.add(side)
                    self.known_exterior.add(point)
                    return False  # Found an extremity
                stack.append(side)
            inspected.add(point)
        else:
            self.known_interior.update(inspected)
            return True  # Did not reach the sides

    def exterior_area(self):
        candidates = set(self.all_sides())
        valid = set()
        for seed in candidates:
            if not self.is_contained(seed):
                valid.add(seed)

        return len(list(side for side in self.all_sides() if side in valid))


points = []
for line in (l.rstrip() for l in sys.stdin):
    points.append(tuple(int(i) for i in line.split(",")))

droplet = Droplet(set(points))
print("Part 1:", droplet.surface_area())
print("Part 2:", droplet.exterior_area())
