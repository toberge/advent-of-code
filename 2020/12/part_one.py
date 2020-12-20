"""
Day 12: Rain Risk
Part One: Moving the boat
"""

import sys
from typing import Iterable

DIRS = ["N", "E", "S", "W"]

SLOPES = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

TURNS = {"L": -1, "R": 1}


def add(a: tuple, b: tuple):
    return tuple(x + y for x, y in zip(a, b))


def mult(tup: tuple, num: int):
    return tuple(x * num for x in tup)


def split_instructions(lst: [str]) -> [(str, int)]:
    for line in lst:
        yield line[0], int(line[1:])


class Ferry:
    def __init__(self, dir_="E", pos_=(0, 0), debug=False):
        self.dir = dir_
        self.pos = pos_
        self._debug = debug

    def _turn(self, turndir, angle):
        delta = angle // 90 if turndir == "R" else -angle // 90
        self.dir = DIRS[(DIRS.index(self.dir) + delta) % 4]

    def _move(self, dist, dir_=""):
        self.pos = add(self.pos, mult(SLOPES[dir_ if dir_ else self.dir], dist))

    def _move_or_turn(self, dir_, dist):
        if dir_ in TURNS:  # L, R
            self._turn(dir_, dist)
            if self._debug:
                print(dir_, dist, "->", "Turn to", self.dir)
        elif dir_ in SLOPES:  # N, E, S, W
            self._move(dist, dir_=dir_)  # move w/o turning
            if self._debug:
                print(dir_, dist, "->", "Move", dir_, dist, "->", self.pos)
        else:
            self._move(dist)
            if self._debug:
                print(dir_, dist, "->", "Move", self.dir, dist, "->", self.pos)

    def maneuver(self, instructions: [(str, int)]):
        for dir_, dist in instructions:
            self._move_or_turn(dir_, dist)

    def manhattan_dist(self):
        return sum(abs(i) for i in self.pos)


def main():
    instructions = split_instructions(sys.stdin.readlines())
    ferry = Ferry(debug=False)
    ferry.maneuver(instructions)
    print(ferry.pos, ferry.manhattan_dist())


if __name__ == "__main__":
    main()
