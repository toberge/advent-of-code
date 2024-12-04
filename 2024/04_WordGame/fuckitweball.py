import sys
from itertools import product

game = [list(line.strip()) for line in sys.stdin.readlines()]
cols = len(game[0])
rows = len(game)

target = "XMAS"
marked = set()


def neighs(x, y):
    yield (x + 0, y + 1)
    yield (x + 0, y - 1)
    yield (x + 1, y + 0)
    yield (x - 1, y + 0)
    yield (x + 1, y + 1)
    yield (x - 1, y + 1)
    yield (x + 1, y - 1)
    yield (x - 1, y - 1)


def search(x, y):
    for x1, y1 in neighs(x, y):
        if x1 < 0 or y1 < 0 or x1 >= rows or y1 >= cols:
            continue
        if "M" == game[x1][y1]:
            yield searchpath(x1, y1, x1 - x, y1 - y)


def searchpath(x, y, dx, dy):
    print(x, y, dx, dy)

    for c in target[2:]:
        x += dx
        y += dy
        if x < 0 or y < 0 or x >= rows or y >= cols:
            return 0
        if c != game[x][y]:
            return 0
    print("yey")
    return 1


def searchmas(x, y, c):
    try:
        if game[x + 1][y + 1] != "A":
            return 0
        if c == "S":
            if game[x + 2][y + 2] != "M":
                return 0
        else:
            if game[x + 2][y + 2] != "S":
                return 0
        if not (
            (game[x + 2][y] == "S" and game[x][y + 2] == "M")
            or (game[x + 2][y] == "M" and game[x][y + 2] == "S")
        ):
            return 0
        return 1
    except:
        return 0


# what part 2 could have beeeeeeen
def search1(x, y, c):
    # if (x, y) in marked:
    #     yield 0
    #     return
    # marked.add((x, y))
    i = target.find(c)
    if i < 0:
        yield 0
        return
    if i >= len(target) - 1:
        yield 1
        return
    nxt = target[i + 1]
    for x1, y1 in neighs(x, y):
        if x1 < 0 or y1 < 0 or x1 >= rows or y1 >= cols:
            continue
        if nxt == game[x1][y1]:
            yield from search1(x1, y1, nxt)
            return


count = 0
for x, y in product(range(rows), range(cols)):
    if game[x][y] == "X":
        count += sum(search(x, y))
        print(x, y, game[x][y], count)

print(count)

count = 0
for x, y in product(range(rows), range(cols)):
    if game[x][y] in {"S", "M"}:
        count += searchmas(x, y, game[x][y])
        print(x, y, game[x][y], count)

print(count)

