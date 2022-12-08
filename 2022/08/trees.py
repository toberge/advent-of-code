import sys
from itertools import product

trees = []

for line in (l.rstrip("\n") for l in sys.stdin):
    trees.append([int(t) for t in line])


w = len(trees[0])
halfwidth = w // 2
h = len(trees)
halfheight = h // 2


def matrix_str(matrix):
    return (
        "\n".join(
            "".join(str(t) if t is not None else "x" for t in row) for row in matrix
        )
        + f"\n"
    )


def clone(matrix):
    return [
        matrix[0][:],
        *[[line[0], *[None] * (len(line) - 2), line[-1]] for line in matrix[1:-1]],
        matrix[-1][:],
    ]


# First create one matrix for each axis
lefts = clone(trees)
rights = clone(trees)
ups = clone(trees)
downs = clone(trees)
for x, y in product(range(1, w - 1), range(1, h - 1)):
    lefts[y][x] = max(lefts[y][x - 1], trees[y][x - 1])
    ups[y][x] = max(ups[y - 1][x], trees[y - 1][x])
for x, y in product(range(w - 2, 0, -1), range(1, h - 1)):
    rights[y][x] = max(rights[y][x + 1], trees[y][x + 1])
for x, y in product(range(1, w - 1), range(h - 2, 0, -1)):
    downs[y][x] = max(downs[y + 1][x], trees[y + 1][x])

visible = w * 2 + (h - 2) * 2

# Then use the matrices, min() < this tree's height
for x, y in product(range(1, w - 1), range(1, h - 1)):
    if trees[y][x] > min(lefts[y][x], rights[y][x], ups[y][x], downs[y][x]):
        visible += 1

print("Part 1:", visible)

# HELLO. THE FOLLOWING DID NOT WORK :)
# First create one matrix for each axis
# This time, we find the viewing distance!
lefts = [[0, *([None] * (w - 1))] for _ in range(h)]
rights = [[*([None] * (w - 1)), 0] for _ in range(h)]
ups = [[0] * w, *([None] * w for _ in range(h - 1))]
downs = [*([None] * w for _ in range(h - 1)), [0] * w]
for x, y in product(range(1, w), range(0, h)):
    lefts[y][x] = lefts[y][x - 1] + 1 if trees[y][x] > trees[y][x - 1] else 0
for x, y in product(range(0, w), range(1, h)):
    ups[y][x] = ups[y - 1][x] + 1 if trees[y][x] > trees[y - 1][x] else 0
for x, y in product(range(w - 2, -1, -1), range(0, h)):
    rights[y][x] = rights[y][x + 1] + 1 if trees[y][x] > trees[y][x + 1] else 0
for x, y in product(range(0, w), range(h - 2, -1, -1)):
    downs[y][x] = downs[y + 1][x] + 1 if trees[y][x] > trees[y + 1][x] else 0

# Then use the matrices :)
best_view = max(
    lefts[y][x] * rights[y][x] * ups[y][x] * downs[y][x]
    for x, y in product(range(w), range(h))
)

# new idea: lefts[height][y][x] for each of the 10 heights...
# Will be less expensive than the O(n^2) that follows :))))
# THIS IS THE IDEA THAT I USED THOUGH


def view_distance(this_tree, line):
    distance = 0
    for tree in line:
        if this_tree > tree:
            distance += 1
        else:
            return distance + 1
    return distance


views = [*([None] * w for _ in range(h))]

for x, y in product(range(w), range(h)):
    height = trees[y][x]
    lefts[y][x] = view_distance(height, reversed(trees[y][:x]))
    rights[y][x] = view_distance(height, trees[y][x + 1 :])
    ups[y][x] = view_distance(height, reversed(list(line[x] for line in trees[:y])))
    downs[y][x] = view_distance(height, (line[x] for line in trees[y + 1 :]))
    views[y][x] = lefts[y][x] * rights[y][x] * ups[y][x] * downs[y][x]

print(matrix_str(trees))
print("lefts")
print(matrix_str(lefts))
print("rights")
print(matrix_str(rights))
print("ups")
print(matrix_str(ups))
print("downs")
print(matrix_str(downs))
print("views")
print(matrix_str(views))

# Then use the matrices :)
best_view = max(
    lefts[y][x] * rights[y][x] * ups[y][x] * downs[y][x]
    for x, y in product(range(w), range(h))
)

print("Part 2:", best_view)
