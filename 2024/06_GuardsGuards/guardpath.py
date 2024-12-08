import sys
from collections import defaultdict
from bisect import bisect_left

field = [list(l.strip()) for l in sys.stdin.readlines()]
ylen = len(field)
xlen = len(field[0])

# x -> y
xs = defaultdict(list)
# y -> x
ys = defaultdict(list)

start = (0, 0)
visited = set()
delta = (0, -1)

for y in range(ylen):
    for x in range(xlen):
        if field[y][x] == "#":
            xs[x].append(y)
            ys[y].append(x)
        elif field[y][x] == "^":
            start = (x, y)

for x, y in xs.items():
    xs[x] = sorted(y)

for y, x in ys.items():
    ys[y] = sorted(x)

print(xs, ys)


def within_bounds(p):
    return 0 <= p[0] < xlen and 0 <= p[1] < xlen


def next(delta):
    match delta:
        case (0, 1):
            return (-1, 0)
        case (-1, 0):
            return (0, -1)
        case (0, -1):
            return (1, 0)
        case (1, 0):
            return (0, 1)


done = False
while not done:
    print(start)
    px, py = start
    match delta:
        case (0, dy):
            # check if obstruction in y dir
            # if not, we're done
            if px in xs:
                # if yes, continue on from there - 1
                cands = xs[px] if dy > 0 else reversed(xs[px])
                # print(list(cands), py, dy)
                for y in cands:
                    if y > py if dy > 0 else y < py:
                        start = (px, y - dy)
                        break
                else:
                    print("hey", py, dy, xs[px][0])
                    done = True
        case (dx, 0):
            if px in xs:
                cands = ys[py] if dx > 0 else reversed(ys[py])
                for x in cands:
                    if x > px if dx > 0 else x < px:
                        start = (x - dx, py)
                        break
                else:
                    done = True
    # TODO count positions along line pain....
    if px == start[0] and py == start[1]:

        while within_bounds((px, py)):
            visited.add((px, py))
            print(px, py)
            px += delta[0]
            py += delta[1]
        break
    print(px, py, start)
    while not (px == start[0] and py == start[1]) and within_bounds((px, py)):
        visited.add((px, py))
        print(px, py)
        px += delta[0]
        py += delta[1]
    visited.add(start)
    delta = next(delta)

print(len(visited))
