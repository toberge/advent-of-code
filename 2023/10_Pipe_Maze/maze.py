import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class coord:
    x: int
    y: int

    def __add__(self, other) -> "coord":
        return coord(self.x + other.x, self.y + other.y)

    def __neg__(self) -> "coord":
        return coord(-self.x, -self.y)


left = coord(-1, 0)
right = coord(1, 0)
up = coord(0, -1)
down = coord(0, 1)

cardinal_deltas = [left, right, up, down]

neighbor_deltas = [
    left,
    left + up,
    left + down,
    right,
    right + up,
    right + down,
    up,
    down,
]

pipe_to_deltas = {
    "|": (up, down),
    "-": (left, right),
    "7": (left, down),
    "J": (left, up),
    "L": (right, up),
    "F": (right, down),
}


@dataclass
class Node:
    char: str
    position: coord
    left: coord
    right: coord
    in_loop: bool = False

    @staticmethod
    def parse(pipe: str, position: coord, island: list[str]) -> "Node":
        if pipe == ".":
            raise NotImplementedError("No . parsing")
        if pipe == "S":
            # TODO own method for this?
            neighbors = []
            for delta in cardinal_deltas:
                neighbor_position = position + delta
                try:
                    neighbor = island[neighbor_position.y][neighbor_position.x]
                    if neighbor == ".":
                        continue
                    if -delta in pipe_to_deltas[neighbor]:
                        neighbors.append(neighbor_position)
                except KeyError:
                    continue
            print("S node leads to", neighbors)
            return Node(pipe, position, neighbors[0], neighbors[1], in_loop=True)

        deltas = pipe_to_deltas[pipe]
        return Node(pipe, position, position + deltas[0], position + deltas[1])

    def opposite(self, position: coord) -> coord:
        if position == self.left:
            return self.right
        if position == self.right:
            return self.left
        raise Exception("Invalid connection!")


class Loop:
    nodes: dict[coord, Node]
    start: Node
    in_loop: set[coord]
    inside: set[coord]
    outside: set[coord]
    height: int
    width: int

    def __init__(self, island: list[str]):
        self.nodes = {}
        self.inside = set()
        self.outside = set()
        height = len(island)
        width = len(island[0])
        for y in range(height):
            for x in range(width):
                pipe = island[y][x]
                if pipe == ".":
                    continue
                pos = coord(x, y)
                node = Node.parse(pipe, pos, island)
                self.nodes[pos] = node
                if pipe == "S":
                    self.start = node

    def steps_along_loop(self) -> int:
        """this also marks loop"""
        left_prev = right_prev = self.start.position
        left = self.nodes[self.start.left]
        right = self.nodes[self.start.right]
        visited = {self.start.position}
        steps = 0

        while left.position not in visited and right.position not in visited:
            left.in_loop = True
            right.in_loop = True
            self.in_loop.add(left.position)
            self.in_loop.add(right.position)

            visited.add(left.position)
            visited.add(right.position)

            left_next = left.opposite(left_prev)
            right_next = right.opposite(right_prev)
            left_prev = left.position
            right_prev = right.position

            left = self.nodes[left_next]
            right = self.nodes[right_next]
            steps += 1
        return steps

    def squeeze_through(self, start: coord) -> coord:
        # TODO go in direction away from inside, check for non-loop along side
        #      then follow whichever direction you end up with, still checking the same side
        # TODO OR JUST MAYBE SCALE UP THE ENTIRE MAP SO YOU DON'T NEED THE SQUEEZE CHECK
        #      (means that only nodes that are at even coords in both dirs are real)
        return coord(-1, -1)

    def is_valid(self, position: coord) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def neighbors(self, position: coord) -> Iterable[coord]:
        return (position + d for d in neighbor_deltas if self.is_valid(position + d))

    def bfs(self, start: coord, already_visited: set[coord]) -> tuple[set[coord], bool]:
        stack = [start]
        visited = set()
        is_in_loop = True
        while len(stack) > 0:
            # TODO in_loop -> call squeeze_through somehow
            pos = stack.pop()
            if pos in visited:
                continue
            if pos in already_visited:
                # TODO this is unnecessary if you extend the thing
                if pos in self.in_loop:
                    # TODO also add squeezed nodes to visited
                    output = self.squeeze_through(pos)
                    if output is not None:
                        stack.append(output)
                continue
            visited.add(pos)
            stack.extend(c for c in self.neighbors(pos) if c not in visited)
        return visited, is_in_loop

    def positions_outside_loop(self) -> int:
        visited = set(self.in_loop)
        for pos in (coord(x, y) for x in range(self.height) for y in range(self.width)):
            if pos in visited:
                continue
            visits, is_in_loop = self.bfs(pos, visited)
            visited = visited.union(visits)
            if is_in_loop:
                self.inside = self.inside.union(visits)
            else:
                self.outside = self.outside.union(visits)

        return len(self.inside)


if __name__ == "__main__":
    island = [l.strip() for l in sys.stdin.readlines()]
    loop = Loop(island)
    steps = loop.steps_along_loop()
    print("Part 1:", steps)
    steps = loop.steps_along_loop()
