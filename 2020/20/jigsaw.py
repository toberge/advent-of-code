"""
Day 20: Jurassic Jigsaw

Part one: An hour and a half? Really?
          Probably less, since I was working on other things first.
Part two: wrogrwjogjrwgowrjgorwjgorwgutwgwougjrwhgwoughrwoughrwg idk how long

And, finally:
You have enough stars to [Pay the Deposit].

The time in the readme was measured WITHOUT image exports.
"""

import math
import re
import sys
from collections import Counter, defaultdict
from enum import IntEnum
from itertools import chain

import numpy as np
from PIL import Image

SEA_MONSTER = """..................#.
#....##....##....###
.#..#..#..#..#..#...""".split(
    "\n"
)

COLOR = {
    "B": [32, 122, 167],
    "#": [21, 82, 112],
    "O": [164, 69, 61],
    ".": [7, 43, 61],
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
                row[j] = next(
                    t for t in sides if t not in used and t in neighbours[prev]
                )
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
        tile.flip()
    raise Exception("Yo, these tiles can't match up!")


def transform_until_equal3(
    tile1: Tile,
    tile2: Tile,
    tile3: Tile,
    edgefun12=lambda t: t.right_edge(),
    edgefun13=lambda t: t.bottom_edge(),
    edgefun2=lambda t: t.left_edge(),
    edgefun3=lambda t: t.top_edge(),
):
    # Permutations of tile1
    for _ in range(2):
        for _ in range(4):
            # Permutations of tile2
            for _ in range(2):
                for _ in range(4):
                    # Permutations of tile3
                    for _ in range(2):
                        for _ in range(4):
                            if edgefun12(tile1) == edgefun2(tile2) and edgefun13(
                                tile1
                            ) == edgefun3(tile3):
                                return  # and break out
                            tile3.rot()
                        tile3.flip()
                    tile2.rot()
                tile2.flip()
            tile1.rot()
        tile1.flip()
    raise Exception("Yo, these THREE tiles can't match up!")


def orient_grid_properly(grid: [[Tile]], n: int):
    """
    Actually the most self-explanatory part of this
    - me, a few hours ago.
    I did not have to change more than the initial alignment
    to fix the problem, however.
    """
    # Special handling of 1st tile!
    head = grid[0][0]
    transform_until_equal3(head, grid[0][1], grid[1][0])
    assert (
        head.bottom_edge() == grid[1][0].top_edge()
        and head.right_edge() == grid[0][1].left_edge()
    )

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


def merge_with_borders(grid: [[Tile]]) -> Tile:
    lines = []
    size = len(grid[0][0].content)
    for i, row in enumerate(grid):
        for _ in range(size):
            lines.append("B")
        for _, tile in enumerate(row):
            for k in range(size):
                lines[i * (size + 1) + k] += tile.content[k] + "B"
        lines.append("".join("B" * (size * len(grid) + len(grid) + 1)))
    return Tile(0, lines)


def merge(grid: [[Tile]]) -> Tile:
    lines = []
    size = len(grid[0][0].image)
    for i, row in enumerate(grid):
        for _ in range(size):
            lines.append("")
        for _, tile in enumerate(row):
            for k in range(size):
                lines[i * (size) + k] += tile.image[k]
    return Tile(0, lines)


def find_monsters(image: Tile) -> [(int, int)]:
    monsters: [(int, int)] = []
    monsterlen = len(SEA_MONSTER[0])
    imglen = len(image.content)
    for i in range(imglen - len(SEA_MONSTER)):
        for j in range(imglen - monsterlen):
            for k, pattern in enumerate(SEA_MONSTER):
                if not re.fullmatch(pattern, image.content[i + k][j : j + monsterlen]):
                    break  # no match!
            else:
                monsters.append((i, j))
    return monsters


def permute_the_thing(image: Tile):
    """Just used to check that I WAS NOT UTTERLY WRONG"""
    for _ in range(2):
        for _ in range(4):
            yield
            image.rot()
        image.flip()


def find_monsters_in_permutations(image: Tile) -> [(int, int)]:
    """hahahahahahahahahahahahahahaaaa"""
    for _ in range(2):
        for _ in range(4):
            monsters = find_monsters(image)
            if len(monsters) > 0:
                return monsters
            image.rot()
        image.flip()
    raise Exception("Clean waters?")


def mark_monsters(monsters: [(int, int)], image: Tile):
    """Horribly inefficient code, since each tile stores its stuff as a list of immutable strings"""
    for y, x in monsters:
        for dy, pattern in enumerate(SEA_MONSTER):
            for dx, tile in enumerate(pattern):
                if tile == "#":
                    # orig = image.content[y + dy]
                    # image.content[y + dy] = orig[: x + dx] + "O" + orig[x + dx + 1 :]
                    image.content[y + dy] = "".join(
                        c if x + dx != ix else "O"
                        for ix, c in enumerate(image.content[y + dy])
                    )


def part_two(tiles: [Tile], neighbours):
    n = int(math.sqrt(len(tiles)))
    tilemap = {t.id: t for t in tiles}

    # Find correct ordering
    grid = assemble_grid(neighbours, n)
    assert test_solution(grid, neighbours, n)
    realgrid = [[tilemap[i] for i in row] for row in grid]

    # Orient image correctly
    orient_grid_properly(realgrid, n)
    merge_with_borders(realgrid).to_image("borders.png")
    image = merge(realgrid)
    image.to_image("merged.png")

    # eeeeh
    # for i, _ in enumerate(permute_the_thing(image)):
    #     monsters = find_monsters(image)
    #     clone = Tile(0, image.content[:])
    #     mark_monsters(monsters, clone)
    #     print(i, sum(1 for t in chain.from_iterable(clone.content) if t == "#"))

    # Find those monsters
    monsters = find_monsters_in_permutations(image)
    mark_monsters(monsters, image)
    image.to_image("monsters.png")
    return sum(1 for t in chain.from_iterable(image.content) if t == "#")


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
