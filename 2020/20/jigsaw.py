"""
Day 20: Jurassic Jigsaw

Part one: An hour and a half? Really?
          Probably less, since I was working on other things first.
"""

import math
import sys
from collections import Counter, defaultdict
from enum import IntEnum
from itertools import chain, product
from pprint import pp

import numpy as np
from PIL import Image

SEA_MONSTER = """__________________#_
#____##____##____###
_#__#__#__#__#__#___ """.split(
    "\n"
)

COLOR = {
    "#": [254, 0, 0],
    ".": [0, 0, 254],
    "O": [254, 254, 0],
}


class Orientation(IntEnum):
    DEFAULT = 0
    ROT90 = 1
    ROT180 = 2
    ROT270 = 3


def rot_orientation(orientation: Orientation, rotation=Orientation.ROT90):
    return Orientation((orientation % 4 + rotation) % 4)


class Tile:
    def __init__(self, id_, content):
        self.id = id_
        self.content = content
        self._update_edges()
        self.size = len(self.content)
        self.orientation = Orientation.DEFAULT
        self.flipped = False

    def _update_edges(self):
        self.edges = [
            self.content[0],
            "".join(row[-1] for row in self.content),
            self.content[-1],
            "".join(row[0] for row in self.content),
        ]
        self.edges.extend(["".join(reversed(edge)) for edge in self.edges])

    def top_edge(self):
        return self.edges[0]

    def right_edge(self):
        return self.edges[1]

    def bottom_edge(self):
        return self.edges[2]

    def left_edge(self):
        return self.edges[3]

    @property
    def image(self):
        """The actual image does not contain the borders!"""
        return [line[1:-1] for line in self.content[1:-1]]

    def __repr__(self):
        return "\n".join(self.content)

    def edgestr(self):
        lst = []
        lst.append(f"Tile {self.id}\n")
        for i, edge in enumerate(self.edges):
            if (i + 1) % 4 == 1:
                lst.append("Top")
            if (i + 1) % 4 == 2:
                lst.append("Right")
            if (i + 1) % 4 == 3:
                lst.append("Bottom")
            if (i + 1) % 4 == 0:
                lst.append("Left")
            if i > 3:
                lst.append(", flipped")
            lst.append(":" + "\n")
            lst.append(edge + "\n")
        return "".join(lst)

    def to_image(self, filename):
        img = Image.fromarray(
            np.uint8([[COLOR[bit] for bit in row] for row in self.content]),
            "RGB",
        )
        img.resize(size=(img.width * 4, img.height * 4), resample=Image.NEAREST).save(
            filename
        )

    def flip(self):
        """Flip around y-axis"""
        self.content = ["".join(reversed(line)) for line in self.content]
        self._update_edges()
        self.flipped = not self.flipped

    def rot(self):
        """Rotate LEFT by 90 degrees"""
        self.content = [
            "".join(line[i] for line in self.content)
            for i in reversed(range(self.size))
        ]
        self._update_edges()
        self.orientation = rot_orientation(self.orientation)


def parse(lines: [str]) -> [Tile]:
    tiles = []
    id_ = -1
    content = []
    for line in lines:
        if line.startswith("Tile"):
            id_ = int(line.removeprefix("Tile ").removesuffix(":"))
        elif line == "":
            tiles.append(Tile(id_, content))
            content = []
        else:
            content.append(line)
    tiles.append(Tile(id_, content))

    return tiles


def create_revmap(tiles: [Tile]):
    revmap = defaultdict(list)
    for id_, edges in {t.id: set(t.edges) for t in tiles}.items():
        for edge in edges:
            revmap[edge].append(id_)
    return revmap


def find_neighbours(revmap: {str: [int]}):
    neighbours = defaultdict(set)
    for ids in revmap.values():
        for id_ in ids:
            neighbours[id_].update(i for i in ids if i != id_)
    return neighbours


def find_corners(revmap: {str: [int]}):
    return [
        id_
        for id_, count in Counter(
            chain.from_iterable(ids for edge, ids in revmap.items() if len(ids) == 2)
        ).items()
        if count == 4
    ]


def print_counts_and_so_on(neighbours: {int: set}):
    print(
        "Corners:",
        sum(1 for i, xs in neighbours.items() if len(xs) == 2),
    )
    print(
        "Sides:",
        sum(1 for i, xs in neighbours.items() if len(xs) == 3),
    )
    print(
        "Insides:",
        sum(1 for i, xs in neighbours.items() if len(xs) == 4),
    )


def analyze_neighbours(neighbours: {int: set}):
    """Count possible corner/side/inside pieces to check assumptions"""
    # remove plz
    return (
        set(i for i, xs in neighbours.items() if len(xs) == 2),
        set(i for i, xs in neighbours.items() if len(xs) == 3),
        set(i for i, xs in neighbours.items() if len(xs) == 4),
    )


def test_solution(grid: [[int]], neighbours: {int: set}, n: int) -> bool:
    for i in range(n):
        for j in range(n):
            tile = grid[i][j]
            if not all(
                (
                    i == 0 or tile in neighbours[grid[i - 1][j]],
                    i == n - 1 or tile in neighbours[grid[i + 1][j]],
                    j == 0 or tile in neighbours[grid[i][j - 1]],
                    j == n - 1 or tile in neighbours[grid[i][j + 1]],
                )
            ):
                return False
    return True


def assemble_grid(neighbours: {int: set}, n: int) -> [[int]]:
    """Simplified logic by making some hefty assumptions"""
    corners, sides, insides = analyze_neighbours(neighbours)

    grid = []
    for i in range(n):
        grid.append([-1] * n)
    used = set()

    # Go row by row
    for i, row in enumerate(grid):
        if i == 0:
            if 1951 in neighbours:
                row[0] = 1951  # 'tis the example
            else:
                row[0] = next(t for t in corners if t not in used)
        elif i == n - 1:
            row[0] = next(
                t for t in corners if t not in used and t in neighbours[grid[i - 1][0]]
            )
        else:
            row[0] = next(
                t for t in sides if t not in used and t in neighbours[grid[i - 1][0]]
            )
        used.add(row[0])

        # side or inner parts
        prev = row[0]
        for j in range(1, n - 1):
            if i == 0:
                cands = list(
                    t for t in sides if t not in used and t in neighbours[prev]
                )
                row[j] = cands[-1]
            elif i == n - 1:
                row[j] = next(
                    t
                    for t in sides
                    if t not in used
                    and t in neighbours[prev]
                    and t in neighbours[grid[i - 1][j]]
                )
            else:
                row[j] = next(
                    t
                    for t in insides
                    if t not in used
                    and t in neighbours[prev]
                    and t in neighbours[grid[i - 1][j]]
                )
            prev = row[j]
            used.add(row[j])

        # again, corner or side
        if i == 0:
            row[-1] = next(
                t for t in corners if t not in used and t in neighbours[prev]
            )
        elif i == n - 1:
            row[-1] = next(
                t
                for t in corners
                if t not in used
                and t in neighbours[prev]
                and t in neighbours[grid[i - 1][-1]]
            )
        else:
            row[-1] = next(
                t
                for t in sides
                if t not in used
                and t in neighbours[prev]
                and t in neighbours[grid[i - 1][-1]]
            )
        used.add(row[-1])

    return grid


def rotate_until_equal(tile: Tile, edge: str, edgefun=lambda t: t.left_edge()):
    for _ in range(2):
        for _ in range(4):
            if edgefun(tile) == edge:
                return  # and break out
            tile.rot()
        print("aaaaaaaaaaa")
        tile.flip()
    raise Exception("Yo, disse kan ikke matches!")


def rotate_until_both_equal(
    tile: Tile,
    edge1: str,
    edge2: str,
    edgefun1=lambda t: t.right_edge(),
    edgefun2=lambda t: t.bottom_edge(),
):
    for _ in range(2):
        for _ in range(4):
            if edgefun1(tile) == edge1 and edgefun2(tile) == edge2:
                return  # and break out
            tile.rot()
        tile.flip()
    raise Exception("Yo, disse kan ikke matches!")


def orient_grid_properly(grid: [[Tile]], n: int):
    """Actually the most self-explanatory part of this"""
    # Special handling of 1st tile!
    head = grid[0][0]
    right_edge = next(
        e1 for e1, e2 in product(head.edges, grid[0][1].edges) if e1 == e1
    )
    bottom_edge = next(
        e1 for e1, e2 in product(head.edges, grid[1][0].edges) if e1 == e1
    )
    rotate_until_both_equal(head, right_edge, bottom_edge)
    # rotate_until_equal(head, right_edge, lambda t: t.right_edge())
    # rotate_until_equal(head, bottom_edge, lambda t: t.bottom_edge())

    for i, row in enumerate(grid):
        # handle beginning of line
        if i > 0:
            rotate_until_equal(
                row[0], grid[i - 1][0].bottom_edge(), edgefun=lambda t: t.top_edge()
            )

        # each tile must match the previous
        prev = row[0]
        for tile in row[1:]:
            rotate_until_equal(
                tile,
                prev.right_edge(),
            )
            prev = tile


def merge(grid: [[Tile]]) -> Tile:
    lines = []
    size = len(grid[0][0].content)
    for i, row in enumerate(grid):
        for _ in range(size):
            lines.append("")
        for _, tile in enumerate(row):
            for k in range(size):
                lines[i * (size + 1) + k] += tile.content[k] + "O"
        lines.append("".join("O" * (size * len(grid) + 3)))
    return Tile(0, lines)


def part_two(tiles: [Tile], neighbours):
    n = int(math.sqrt(len(tiles)))
    tilemap = {t.id: t for t in tiles}
    grid = assemble_grid(neighbours, n)
    assert test_solution(grid, neighbours, n)
    pp(grid)
    realgrid = [[tilemap[i] for i in row] for row in grid]
    orient_grid_properly(realgrid, n)
    image = merge(realgrid)
    print(image)
    image.to_image("haha.png")


def test_manipulation(tiles: [Tile]):
    print(tiles[0])
    tiles[0].to_image("asdf.png")
    tiles[0].rot()
    print()
    print(tiles[0])
    print(tiles[0].edgestr())
    tiles[0].to_image("asdfrot.png")


def main():
    tiles = parse(line.rstrip() for line in sys.stdin.readlines())
    revmap = create_revmap(tiles)
    corners = find_corners(revmap)
    neighbours = find_neighbours(revmap)
    # Part one
    print(math.prod(corners))
    # Part two
    print(part_two(tiles, neighbours))


if __name__ == "__main__":
    main()
