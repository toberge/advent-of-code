import sys
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class coord:
    x: int
    y: int

    def __add__(self, other) -> "coord":
        return coord(self.x + other.x, self.y + other.y)


directions = {"N": coord(0, -1), "S": coord(0, 1), "W": coord(-1, 0), "E": coord(1, 0)}


class Board:
    def __init__(self, starting_points: list[coord]):
        self.points = set(starting_points)
        self.directions = list(directions.values())

    def step(self) -> bool:
        proposed_steps = defaultdict(list)

        for point in self.points:
            step = self.propose_step(point)
            proposed_steps[step].append(point)

        newpoints = set()
        for step, proposers in proposed_steps.items():
            if len(proposers) > 1:
                newpoints.update(proposers)
            else:
                newpoints.add(step)

        if len(newpoints) != len(self.points):
            raise Exception("wtf")
        if len(newpoints.difference(self.points)) == 0:
            self.points = newpoints
            return False
        self.points = newpoints

        # Shift directions surveyed
        self.directions = self.directions[1:] + [self.directions[0]]
        return True

    def propose_step(self, point: coord) -> coord:
        if self.is_too_clear(point):
            return point
        for direction in self.directions:
            if self.is_clear(point, direction):
                return point + direction
        return point

    def is_too_clear(self, point: coord) -> bool:
        return all(
            neighbour not in self.points
            for neighbour in [
                point + coord(-1, -1),
                point + coord(-1, 0),
                point + coord(-1, 1),
                point + coord(0, -1),
                point + coord(0, 1),
                point + coord(1, -1),
                point + coord(1, 0),
                point + coord(1, 1),
            ]
        )

    def is_clear(self, point: coord, direction: "coord") -> bool:
        deltas = []
        match direction:
            case coord(x, 0):
                deltas = [coord(x, -1), coord(x, 0), coord(x, 1)]
            case coord(0, y):
                deltas = [coord(-1, y), coord(0, y), coord(1, y)]
        return (
            len(self.points.intersection(set(point + delta for delta in deltas))) == 0
        )

    def empty_cells(self) -> int:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        width = abs(max(xs) - min(xs)) + 1
        height = abs(max(ys) - min(ys)) + 1
        area = width * height
        return area - len(self.points)

    def __repr__(self) -> str:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return (
            "\n".join(
                "".join(
                    "#" if coord(x, y) in self.points else "."
                    for x in range(min(xs), max(xs) + 1)
                )
                for y in range(min(ys), max(ys) + 1)
            )
            + "\n"
        )


def starting_points(board: list[str]) -> list[coord]:
    points = []
    for y, line in enumerate(board):
        for x, c in enumerate(line):
            if c == "#":
                points.append(coord(x, y))
    return points


def main():
    points = starting_points([l.rstrip() for l in sys.stdin])
    board = Board(points)
    i = 1
    while board.step():
        i += 1
        if i > 10:
            break
    print("Part 1:", board.empty_cells())
    while board.step():
        i += 1
    print("Part 2:", i)


if __name__ == "__main__":
    main()
