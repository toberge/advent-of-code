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

    def is_real(self) -> bool:
        return self.x % 2 == 0 and self.y % 2 == 0


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

right_extension_of = {
    "|": ".",
    "-": "-",
    "7": ".",
    "J": ".",
    "L": "-",
    "F": "-",
    "S": "-",
    ".": ".",
}


down_extension_of = {
    "|": "|",
    "-": ".",
    "7": "|",
    "J": ".",
    "L": ".",
    "F": "|",
    "S": "|",
    ".": ".",
}


@dataclass
class Node:
    char: str
    position: coord
    left: coord
    right: coord

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
            return Node(pipe, position, neighbors[0], neighbors[1])

        deltas = pipe_to_deltas[pipe]
        return Node(pipe, position, position + deltas[0], position + deltas[1])

    def opposite(self, position: coord) -> coord:
        if position == self.left:
            return self.right
        if position == self.right:
            return self.left
        raise Exception("Invalid connection!")


class Loop:
    island: list[str]
    nodes: dict[coord, Node]
    start: Node
    in_loop: set[coord]
    inside: set[coord]
    outside: set[coord]
    height: int
    width: int
    verbose: bool

    def __init__(self, island: list[str], verbose=False):
        self.verbose = verbose
        self.nodes = {}
        self.island = island
        self.inside = set()
        self.outside = set()
        self.in_loop = set()
        self.height = len(island)
        self.width = len(island[0])
        for y in range(self.height):
            for x in range(self.width):
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

        self.in_loop.add(self.start.position)

        while left.position not in visited and right.position not in visited:
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
        # Since we're doing this on the upscaled island, there are half as many steps
        return steps // 2

    def is_valid(self, position: coord) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def neighbors(self, position: coord) -> Iterable[coord]:
        return (position + d for d in cardinal_deltas if self.is_valid(position + d))

    def bfs(self, start: coord, already_visited: set[coord]) -> tuple[set[coord], bool]:
        stack = [start]
        visited = set()
        is_in_loop = True
        while len(stack) > 0:
            pos = stack.pop()
            if pos in self.outside:
                is_in_loop = False
            if pos in visited or pos in already_visited:
                continue
            visited.add(pos)
            # TODO limit how far it reaches so we don't add visited nodes multiple times?
            stack.extend(self.neighbors(pos))
        return visited, is_in_loop

    def positions_inside_loop(self) -> int:
        # TODO do this elsewhere?
        # Outer rim is always outside!
        self.outside.update(
            coord(x, 0) for x in range(self.width) if not coord(x, 0) in self.in_loop
        )
        self.outside.update(
            coord(x, self.height - 1)
            for x in range(self.width)
            if not coord(x, self.height - 1) in self.in_loop
        )
        self.outside.update(
            coord(0, y) for y in range(self.height) if not coord(0, y) in self.in_loop
        )
        self.outside.update(
            coord(self.width - 1, y)
            for y in range(self.height)
            if not coord(self.width - 1, y) in self.in_loop
        )

        visited = set(self.in_loop)
        visited.update(self.outside)

        for pos in (
            coord(x, y)
            for x in range(1, self.height - 1)
            for y in range(1, self.width - 1)
        ):
            if pos in visited:
                continue
            visits, is_in_loop = self.bfs(pos, visited)
            if is_in_loop:
                self.inside.update(visits.difference(visited))
            else:
                self.outside.update(visits.difference(visited))
            visited.update(visits)

        if self.verbose:
            for y, line in enumerate(self.island):
                for x, c in enumerate(line):
                    if not coord(x, y).is_real():
                        continue
                    p = (
                        "\x1b[1;33mI\x1b[37m"
                        if coord(x, y) in self.inside and coord(x, y).is_real()
                        else c
                    )
                    print(p, end="")
                if coord(0, y).is_real():
                    print()
        return len([pos for pos in self.inside if pos.is_real() and self.is_valid(pos)])


def upscaled(island: list[str]) -> list[str]:
    upscaled = []
    for line in island:
        upper = []
        for c in line:
            upper.append(c)
            upper.append(right_extension_of[c])
        upscaled.append("".join(upper))
        lower = []
        for c in line:
            lower.append(down_extension_of[c])
            lower.append(".")
        upscaled.append("".join(lower))
    # TODO fix area around S!
    return upscaled


if __name__ == "__main__":
    island = [l.strip() for l in sys.stdin.readlines()]
    island = upscaled(island)
    loop = Loop(island)
    # loop.verbose = True
    steps = loop.steps_along_loop()
    print("Part 1:", steps)
    positions_inside = loop.positions_inside_loop()
    print("Part 2:", positions_inside)
