"""
overcomplicated orientation and direction handling
"""

from collections import Counter, defaultdict
from enum import IntEnum

from jigsaw import Tile


class Orientation(IntEnum):
    DEFAULT = 0
    ROT90 = 1
    ROT180 = 2
    ROT270 = 3
    FLIPPED = 4
    FLIPROT90 = 5
    FLIPROT180 = 6
    FLIPROT270 = 7


class Dir(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
    FLIPTOP = 4
    FLIPRIGHT = 5
    FLIPBOTTOM = 6
    FLIPLEFT = 7


DIR_EDGES = [Dir(i % 4) for i in range(8)]


def flip_orientation(orientation: Orientation):
    if orientation < 4:
        return Orientation(orientation + 4)
    else:
        return Orientation(orientation - 4)


def rot_orientation(orientation: Orientation, rotation=Orientation.ROT90):
    if rotation > 3:
        raise ValueError(f"we don't accept flips: {rotation}")
    return Orientation((orientation % 4 + rotation) % 4 + (orientation // 4 * 4))


def dir_of(tile: Tile, edge):
    return Dir(tile.edges.index(edge))


def orientation_of(fixed: Dir, mallable: Dir):
    return Orientation(((mallable % 4) - (fixed % 4) + 2) % 4 + (mallable // 4 * 4))


def find_neighbours_extra(tilemap: {int: Tile}, revmap: {str: [int]}):
    neighbours = defaultdict(list)
    # for id_, edges in {t.id: t.edges for t in tiles}.items():
    for edge, ids in revmap.items():
        for id_ in ids:
            tile = tilemap[id_]
            neighbours[id_].extend(
                (
                    i,
                    orientation_of(dir_of(tile, edge), dir_of(tilemap[i], edge)),
                    dir_of(tile, edge),
                )
                for i in ids
                if i != id_
            )
    return {i: set(stuff) for i, stuff in neighbours.items()}


def part_two_maybe(tiles: [Tile], revmap: {str: [int]}, corners: [int]) -> int:
    tilemap = {t.id: t for t in tiles}
    neighbours = find_neighbours_extra(tilemap, revmap)
    for tile, neighbours in filter(lambda x: len(x[1]) == 4, neighbours.items()):
        print(f"{tile} maps to ", end="")
        for neighbour, orientation, direction in neighbours:
            print(
                f"{neighbour} by {str(orientation).removeprefix('Orientation.')} to the {str(direction).removeprefix('Dir.')}, ",
                end="",
            )
        print()
    return -1


def test_orientation():
    print(flip_orientation(Orientation.DEFAULT))
    print(flip_orientation(Orientation.FLIPROT270))
    print(rot_orientation(Orientation.DEFAULT))
    print(rot_orientation(Orientation.FLIPROT270))
