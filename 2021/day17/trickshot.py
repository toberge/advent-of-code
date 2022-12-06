from itertools import product


def simulate(dx, dy, rect):
    """
    x = dx*t +/- 0.5*t^2 (+/- deps on dx )
    y = dy*t - 0.5*t^2

    Idea: find all ts that let x be within bounds, then find t for y... nah?
    """
    x, y = 0, 0
    maxy = 0
    its = 0
    while x <= rect[0][1] and (y > rect[1][0]) and its < 10:
        if dx == 0: its += 1
        x += dx
        dx += 1 if dx < 0 else (-1 if dx > 0 - 1 else 0)
        y += dy
        dy -= 1
        if y > maxy:
            maxy = y
        # print(x, y)
        if rect[0][0] <= x <= rect[0][1] and rect[1][0] <= y <= rect[1][1]:
            return maxy
    return -1


def main():
    line = input()
    x = [int(i) for i in line.split("=")[1].replace(", y", "").split("..")]
    y = [int(i) for i in line.split("=")[2].split("..")]
    # for dx, dy in product(range(3, max(x[0], 100)), range(1, max(y[0], 100))):
    #    yy = simulate(dx, dy, [x, y])
    #    if yy > 0:
    #        print("Launch probe from", dx, dy)
    #        print("Eye of the universe at", yy)
    maxy = max(
        simulate(dx, dy, [x, y])
        for dx, dy in product(
            range(-1000, max(x[0], 100)), range(-100, max(y[0], 1000))
        )
    )
    print(maxy)


if __name__ == "__main__":
    main()
