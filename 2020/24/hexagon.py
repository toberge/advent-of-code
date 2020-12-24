"""
Day 24: Lobby Layout

Part one: Written in 10 mins or so, after looking up hexagonal coordinate systems
Part two: Start 15:16, end 15:32 -> 16 mins to write!
"""

import re
import sys
from functools import lru_cache, reduce


def add(tup1, tup2):
    """Add two points together"""
    return (tup1[0] + tup2[0], tup1[1] + tup2[1])


DIRS = {
    "e": (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
}


class Tiling:
    """Hexagonal tiling"""

    def __init__(self):
        self.flipped: set = set()

    def flip(self, directions):
        """Flip a tile identified by the given directions"""
        point = reduce(
            add,
            (DIRS[direction] for direction in re.findall(r"[ns]?[ew]", directions)),
        )
        if point in self.flipped:
            self.flipped.remove(point)
        else:
            self.flipped.add(point)

    @lru_cache(maxsize=None)
    def _neighbours(self, tile):
        return [add(tile, delta) for delta in DIRS.values()]

    def _flipped_neighbours(self, tile):
        return self.flipped.intersection(self._neighbours(tile))

    def _unflipped_neighbours(self, tile):
        return set(self._neighbours(tile)).difference(self.flipped)

    def process(self):
        """Perform one generation of hexagonal game of life"""
        flips = []
        unflips = []

        for tile in self.flipped:
            # Rule 1: Flipped with {0, 3..6} adjacent get unflipped
            count = len(self._flipped_neighbours(tile))
            if count == 0 or count > 2:
                unflips.append(tile)

            # Rule 2: Unflipped with 2 adjacent get flipped
            for unflipped in self._unflipped_neighbours(tile):
                if len(self._flipped_neighbours(unflipped)) == 2:
                    flips.append(unflipped)

        self.flipped.difference_update(unflips)
        self.flipped.update(flips)


def main():
    """Main."""
    tiles = Tiling()
    for line in sys.stdin.readlines():
        tiles.flip(line.rstrip())
    # Part one:
    print(len(tiles.flipped))
    # Part two:
    for _ in range(1, 101):
        tiles.process()
        # print(f"Day {i}:", len(tiles.flipped))
    print(len(tiles.flipped))


if __name__ == "__main__":
    main()
