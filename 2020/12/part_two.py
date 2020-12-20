"""
Day 12: Rain Risk
Part Two: Whoops, we're mostly moving a *waypoint* instead
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


def turn_clockwise(pos: (int, int)):
    return (-pos[1], pos[0])


def turn_counterclockwise(pos: (int, int)):
    return (pos[1], -pos[0])


def split_instructions(lst: [str]) -> [(str, int)]:
    for line in lst:
        yield line[0], int(line[1:])


class Ferry:
    def __init__(self, waypoint=(10, -1), pos_=(0, 0), debug=False):
        self.waypoint = waypoint
        self.pos = pos_
        self._debug = debug

    def _turn_waypoint(self, turndir, angle):
        # TODO
        delta = angle // 90 if turndir == "R" else -angle // 90
        if delta > 0:
            while delta > 0:
                self.waypoint = turn_clockwise(self.waypoint)
                delta -= 1
        else:
            while delta < 0:
                self.waypoint = turn_counterclockwise(self.waypoint)
                delta += 1

    def _move_waypoint(self, dist, dir_):
        self.waypoint = add(self.waypoint, mult(SLOPES[dir_], dist))

    def _move_to_waypoint(self, dist):
        self.pos = add(self.pos, mult(self.waypoint, dist))

    def _move_or_turn(self, dir_, dist):
        if dir_ in TURNS:  # L, R
            self._turn_waypoint(dir_, dist)
            if self._debug:
                print(dir_, dist, "->", "Turn waypoint to", self.waypoint)
        elif dir_ in SLOPES:  # N, E, S, W
            self._move_waypoint(dist, dir_)
            if self._debug:
                print(
                    dir_, dist, "->", "Move waypoint", dir_, dist, "to", self.waypoint
                )
        else:
            self._move_to_waypoint(dist)
            if self._debug:
                print(dir_, dist, "->", "Move boat", dist, "to", self.pos)

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
