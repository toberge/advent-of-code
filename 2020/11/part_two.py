"""
Day 11: Game of Seats

Part Two: Ray-casting rules

Original code: 3,12 secs
With incrementing count instead of generator: 2,60 secs
When skipping all floor tiles: 2,06 secs
"""

import copy
import sys
from itertools import chain
from time import sleep

SLOPES = [(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]
assert len(SLOPES) == 8


# def neighbour_indices(chairs, y, x, n, m):
def count_occupied_neighbours(chairs, y, x, n, m):
    count = 0
    for dy, dx in SLOPES:
        cy, cx = y + dy, x + dx
        while 0 <= cy < n and 0 <= cx < m and chairs[cy][cx] == ".":
            cy, cx = cy + dy, cx + dx
        if 0 <= cy < n and 0 <= cx < m and chairs[cy][cx] == "#":
            count += 1
    return count


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
            elif chair == "#" and count >= 5:  # adjusted rule
                nextgen[i][j] = "L"
                changed = True
    return nextgen, changed


def game_loop(state):
    n, m = len(state), len(state[0])
    changed = True
    gens = 0
    while changed:
        state, changed = process_chairs(state, n, m)
        gens += 1
        # print("\n".join("".join(l) for l in state))
        # sleep(1)
    print(f"Stabilized in {gens} generations")
    return state


if __name__ == "__main__":
    lines = [list(l.rstrip()) for l in sys.stdin.readlines()]
    res = game_loop(lines)
    print(sum(1 for chair in chain.from_iterable(res) if chair == "#"))
