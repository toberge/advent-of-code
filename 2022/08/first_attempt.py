import sys
from itertools import repeat

trees = []

for line in (l.rstrip("\n") for l in sys.stdin):
    trees.append([int(t) for t in line])

heights = [
    trees[0][:],
    *[[line[0], *[None] * (len(line) - 2), line[-1]] for line in trees[1:-1]],
    trees[-1][:],
]

w = len(trees[0])
halfwidth = w // 2
h = len(trees)
halfheight = h // 2

print(f"Input has dimensions {w}({halfwidth})x{h}({halfheight})")

"""
ok so input is 99x99
which means 50, 50 is center
"""


def height(x, y):
    # TODO it's actually a little more complex than this
    # or rather
    # less complicated
    # so listen
    # what you need to do is ensure that only the diagonals (where the coordinates are the same, or the same when flipped) are able to check in two directions while all the others check their closest side. or something.
    # ...
    # no, actually, uhhhh....
    candidates = [
        (heights[y][x + 1] if x >= halfwidth else None),  # right
        (heights[y][x - 1] if x <= halfwidth + 1 else None),  # left
        (heights[y + 1][x] if y >= halfheight else None),  # below
        (heights[y - 1][x] if y <= halfheight + 1 else None),  # above
    ]
    # print(
    #    x,
    #    y,
    #    trees[y][x],
    #    candidates,
    #    [
    #        heights[y][x + 1],
    #        heights[y][x - 1],
    #        heights[y + 1][x],
    #        heights[y - 1][x],
    #    ],
    # )
    return min(height for height in candidates if height is not None)


"""
1, 99
2, 98
"""


def indices(width, height):
    x = 1
    y = 1
    while width > halfwidth + 1 and height > halfwidth + 1:
        # Upper row
        # print("upper row")
        yield from zip(range(x, width - 1), repeat(y))
        # Bottom row
        # print("bottom row")
        yield from zip(range(x, width - 1), repeat(h - y - 1))
        # Left side
        # print("left side")
        print("lines y:", y, "and", h - y - 1, "x:", x, "to", width - 1)
        print("sides x:", x, "and", w - x - 1, "y:", y + 1, "to", height - 2)
        yield from zip(repeat(x), range(y + 1, height - 2))
        # Right side
        # print("right side")
        yield from zip(repeat(w - x - 1), range(y + 1, height - 2))
        # Next starting point
        x += 1
        y += 1
        width -= 1
        height -= 1
    # yield (x - 1, y - 1)


visible = len(trees[0]) * 2 + (len(trees) - 2) * 2

for (x, y) in indices(len(trees[0]), len(trees)):
    if heights[y][x] is not None:
        continue
    print(
        "\n".join(
            "".join(str(t) if t is not None else "x" for t in row) for row in heights
        ),
        f"\n({x},{y})\n",
    )
    minheight = height(x, y)
    heights[y][x] = max(trees[y][x], minheight)
    if minheight < trees[y][x]:
        # print("visible")
        visible += 1
    # else:
    # print("obscured")

# print(heights)
print("Part 1:", visible)
