"""
Day 11: Game of Seats

Part One: Standard Conway rules

Original code: 1,39 secs
When skipping all floor tiles: 1,23 secs
"""

import copy
import sys
from itertools import chain


def neighbour_indices(y, x, n, m):
    # this is ugly rn
    if y > 0:
        yield (y - 1, x)
        if x > 0:
            yield (y - 1, x - 1)
        if x < m - 1:
            yield (y - 1, x + 1)
    if x > 0:
        yield (y, x - 1)
    if x < m - 1:
        yield (y, x + 1)
    if y < n - 1:
        yield (y + 1, x)
        if x > 0:
            yield (y + 1, x - 1)
        if x < m - 1:
            yield (y + 1, x + 1)


def count_occupied_neighbours(chairs, y, x, n, m):
    return sum(1 for i, j in neighbour_indices(y, x, n, m) if chairs[i][j] == "#")


def process_chairs(chairs, n, m):
    nextgen = copy.deepcopy(chairs)
    changed = False
    for i, row in enumerate(chairs):
        for j, chair in enumerate(row):
            if chair == ".":
                continue
            # neighbours
            count = count_occupied_neighbours(chairs, i, j, n, m)
            # apply rule
            if chair == "L" and count == 0:
                nextgen[i][j] = "#"
                changed = True
            elif chair == "#" and count >= 4:
                nextgen[i][j] = "L"
                changed = True
    return nextgen, changed


def game_loop(state):
    n, m = len(state), len(state[0])
    changed = True
    while changed:
        state, changed = process_chairs(state, n, m)
    return state


if __name__ == "__main__":
    lines = [list(l.rstrip()) for l in sys.stdin.readlines()]
    res = game_loop(lines)
    print(sum(1 for chair in chain.from_iterable(res) if chair == "#"))
