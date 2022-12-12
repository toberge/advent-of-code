import sys
import heapq
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    index: int
    coord: tuple[int, int]

    height: int
    neighbours: list["Node"] = field(default_factory=list)

    distance: int = 9999
    back: Optional["Node"] = None
    visited: bool = False
    seen: bool = False

    def __gt__(self, other: "Node") -> bool:
        """For heapq sorting"""
        return self.distance > other.distance

    def __lt__(self, other: "Node") -> bool:
        """For heapq sorting"""
        return self.distance < other.distance

    def __eq__(self, other: "Node") -> bool:
        return self.index == other.index

    def can_travel_to(self, other: "Node") -> bool:
        return self.height + 1 >= other.height

    def __repr__(self):
        return f"node({self.coord}, {self.height}) -> {','.join(str(n.coord) for n in self.neighbours)}"


def elevation(c: str) -> int:
    return ord(c) - ord("a")


def forest(lines: list[str]) -> tuple[Node, Node, list[Node], list[Node]]:
    nodes: list[Node] = []
    w = len(lines[0])
    h = len(lines)
    start = Node(-1, (0, 0), 26)
    end = Node(-1, (0, 0), 0)
    other_starts: list[Node] = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            i = y * w + x
            if c == "S":  # We start at highest point to be able to go anywhere
                node = start = Node(i, (x, y), elevation("a"))
                start.distance = 0
            elif c == "E":  # Destination is lowest point
                node = end = Node(i, (x, y), elevation("z"))
            else:
                node = Node(y * w + x, (x, y), elevation(c))
            nodes.append(node)
            if c == "a":
                other_starts.append(node)

    for y in range(h):
        for x in range(w):
            node = nodes[y * w + x]
            if y > 0 and node.can_travel_to(nodes[(y - 1) * w + x]):
                node.neighbours.append(nodes[(y - 1) * w + x])
            if y < h - 1 and node.can_travel_to(nodes[(y + 1) * w + x]):
                node.neighbours.append(nodes[(y + 1) * w + x])
            if x > 0 and node.can_travel_to(nodes[y * w + x - 1]):
                node.neighbours.append(nodes[y * w + x - 1])
            if x < w - 1 and node.can_travel_to(nodes[y * w + x + 1]):
                node.neighbours.append(nodes[y * w + x + 1])

    return start, end, other_starts, nodes


def minimum_steps(start, end, print_path=False) -> int:
    heap = [start]

    while len(heap) > 0:
        node = heapq.heappop(heap)
        node.visited = True

        for neighbour in node.neighbours:
            if node.distance + 1 < neighbour.distance:
                neighbour.distance = node.distance + 1
                neighbour.back = node

            if not neighbour.seen:
                heapq.heappush(heap, neighbour)
                neighbour.seen = True

    if print_path:
        node = end
        while node.back is not None:
            print(node.coord, "<- ", end="")
            node = node.back
        print(start.coord)

    return end.distance


def reset(nodes: list[Node]):
    for node in nodes:
        node.distance = 9999
        node.back = None
        node.seen = False
        node.visited = False


heightmap = list(l.rstrip() for l in sys.stdin)

start, end, other_starts, nodes = forest(heightmap)

minimum = minimum_steps(start, end)
print("Part 1:", minimum)

trails = [minimum]
for other_start in other_starts:
    reset(nodes)
    other_start.distance = 0
    trails.append(minimum_steps(other_start, end))
print("Part 2:", min(trails))
