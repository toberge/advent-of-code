import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class coord:
    x: int
    y: int

    def __add__(self, other):
        return coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return coord(self.x - other.x, self.y - other.y)

    def step(self, other):
        return self + (other - self).dir()

    def step_diagonally(self, other):
        return self + coord(
            int(other.x > self.x) - int(other.x < self.x),
            int(other.y > self.y) - int(other.y < self.y),
        )

    def dir(self):
        """Manhattan-style unit distance"""
        return coord(
            int(self.x > 0) - int(self.x < 0), int(self.y > 0) - int(self.y < 0)
        )

    def is_vertical(self):
        return self.x == 0 and self.y != 0

    def is_horizontal(self):
        return self.x != 0 and self.y == 0

    def magnitude(self):
        """Manhattan length"""
        return abs(self.x) + abs(self.y)

    def move_towards(self, head):

        difference = head - self
        cartesian = difference.is_horizontal() or difference.is_vertical()

        # Move horizontally if distance is > 2
        if cartesian and difference.magnitude() > 1:
            return self.step(head)
        # Move diagonally if needed
        elif not cartesian and difference.magnitude() > 2:
            return self.step_diagonally(head)
        return self


DELTA = {
    "U": coord(0, 1),
    "D": coord(0, -1),
    "L": coord(-1, 0),
    "R": coord(1, 0),
}

head = coord(0, 0)
tail = coord(0, 0)
knots = [coord(0, 0)] * 10
visited_by_tail = set([coord(0, 0)])
visited_by_chain = set([coord(0, 0)])

for instruction in sys.stdin:
    [direction, amount] = instruction.split()
    for _ in range(int(amount)):
        knots[0] += DELTA[direction]
        for i in range(9):
            knots[i + 1] = knots[i + 1].move_towards(knots[i])

        visited_by_tail.add(knots[1])
        visited_by_chain.add(knots[-1])

print("Part 1:", len(visited_by_tail))
print("Part 1:", len(visited_by_chain))
