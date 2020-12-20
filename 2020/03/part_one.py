import sys


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
    print(count_trees(sys.stdin.readlines(), (3, 1)))
