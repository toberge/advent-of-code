import numpy as np
import sys
from itertools import takewhile, product

lines = sys.stdin.readlines()
dots = [
    tuple(map(int, line[:-1].split(",")))
    for line in list(takewhile(lambda l: l != "\n", lines))
]

shape = (max(dots, key=lambda x: x[1])[1] + 1, max(dots, key=lambda x: x[0])[0] + 1)
paper = np.ndarray(shape, dtype=bool)
paper[:, :] = 0
for x, y in dots:
    paper[y, x] = True


print(shape)


def show(paper: np.ndarray):
    yy, xx = paper.shape
    for y in range(yy):
        for x in range(xx):
            print("#" if paper[y, x] else ".", end="")
        print()


def flip(paper, index, axis=0):
    size = index
    end = max(paper.shape[axis] - 1, 2 * size)
    padding = 2 * size - (paper.shape[axis] - (paper.shape[axis] % 2))
    print(size, end, padding)

    if axis == 0:
        if size < 30:
            show(paper[:size, :])
            print("------")
            show(
                np.pad(
                    np.flip(paper[size:, :], axis)[: end - size, :],
                    ((0, padding), (0, 0)),
                )
            )
            print("aaa")
        return paper[:size, :] | np.pad(
            np.flip(paper[size:, :], axis)[: end - size, :], ((0, padding), (0, 0))
        )
    if size < 30:
        show(paper[:, :size])
        print("------")
        show(
            np.pad(
                np.flip(paper[:, size:], axis)[:, : end - size],
                ((0, 0), (0, padding)),
            )
        )
        print("aaa")
    return paper[:, :size] | np.pad(
        np.flip(paper[:, size:], axis)[:, : end - size], ((0, 0), (0, padding))
    )


it = iter(lines)
line = next(it)
while line != "\n":
    line = next(it)
line = next(it)
command = line.replace("fold along ", "")[:-1].split("=")
paper = flip(paper, int(command[1]), axis=int(command[0] == "x"))
if max(shape) < 30:
    show(paper)
print(np.count_nonzero(paper))
