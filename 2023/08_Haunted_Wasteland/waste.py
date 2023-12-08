import sys
from dataclasses import dataclass
from functools import reduce
from itertools import cycle
from math import gcd
from operator import mul
from typing import Iterable


@dataclass
class Node:
    name: str
    left: str
    right: str

    @staticmethod
    def parse(line: str) -> "Node":
        name, rest = line.split(" = ")
        left, right = rest[1:-1].split(", ")
        return Node(name, left, right)


class Map:
    def __init__(self, node_list: Iterable[Node]) -> None:
        self.nodes = {n.name: n for n in node_list}
        self.starts = [n for n in self.nodes.keys() if n[-1] == "A"]

    @staticmethod
    def parse(lines: Iterable[str]) -> "Map":
        return Map(Node.parse(l) for l in lines)

    def follow_instructions(self, instructions: str, start="AAA") -> int:
        node = self.nodes[start]
        for i, direction in enumerate(cycle(instructions)):
            if node.name == "ZZZ":
                return i

            if direction == "L":
                node = self.nodes[node.left]
            else:
                node = self.nodes[node.right]
        return -1

    def follow_ghost_instructions_bruteforce(self, instructions: str) -> int:
        # Don't run the bruteforce for it does not work
        nodes = [self.nodes[start] for start in self.starts]
        for i, direction in enumerate(cycle(instructions)):
            if all(n.name[-1] == "Z" for n in nodes):
                return i

            if direction == "L":
                nodes = [self.nodes[n.left] for n in nodes]
            else:
                nodes = [self.nodes[n.right] for n in nodes]
        return -1

    def find_period(self, instructions: str, start: str) -> int:
        node = self.nodes[start]
        for i, direction in enumerate(cycle(instructions)):
            if node.name[-1] == "Z":
                return i

            if direction == "L":
                node = self.nodes[node.left]
            else:
                node = self.nodes[node.right]
        return -1

    def find_periods(self, instructions: str) -> list[int]:
        return [self.find_period(instructions, start) for start in self.starts]


def common_period(periods: Iterable[int]) -> int:
    gcd_ = reduce(gcd, periods)
    return gcd_ * int(reduce(mul, (p / gcd_ for p in periods)))


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin.readlines()]
    instructions = lines[0]
    wasteland_map = Map.parse(lines[2:])

    try:
        steps = wasteland_map.follow_instructions(instructions)
        print("Part 1:", steps)
    except KeyError:
        print("Part 1 impossible with this input")

    steps = common_period(wasteland_map.find_periods(instructions))
    print("Part 2:", steps)
