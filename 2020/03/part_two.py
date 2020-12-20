import sys
from functools import reduce


def count_trees(grid: [[str]], slope: (int, int)) -> int:
    x, y = 0, 0
    dx, dy = slope
    lenx, leny = len(grid[0]), len(grid)
    count = 0

    while y < leny:
        if grid[y][x % (lenx - 1)] == "#":
            count += 1
        x, y = x + dx, y + dy

    return count


if __name__ == "__main__":
    grid = sys.stdin.readlines()
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    print(reduce(lambda a, b: a * b, (count_trees(grid, slope) for slope in slopes)))
