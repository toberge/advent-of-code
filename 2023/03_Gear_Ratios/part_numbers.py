import sys

data = [l.strip() for l in sys.stdin.readlines()]
ny = len(data)
endy = len(data) - 1
nx = len(data[0])
endx = len(data[0]) - 1


def is_symbol(c: str):
    return not (c.isdigit() or c == ".")


def is_part_number(y: int, x: int, data: list[str]):
    coords = [
        data[y - 1][x] if y > 0 else "0",
        data[y - 1][x - 1] if y > 0 and x > 0 else "0",
        data[y - 1][x + 1] if y > 0 and x < endx else "0",
        data[y][x - 1] if x > 0 else "0",
        data[y][x + 1] if x < endx else "0",
        data[y + 1][x - 1] if y < endy and x > 0 else "0",
        data[y + 1][x] if y < endy else "0",
        data[y + 1][x + 1] if y < endy and x < endx else "0",
    ]
    return data[y][x].isdigit() and any(is_symbol(c) for c in coords)


def find_number(x: int, line: str) -> tuple[int, int, int]:
    start = x
    while start > 0 and line[start].isdigit():
        start -= 1
    if not line[start].isdigit():
        start += 1

    end = x
    while end < nx and line[end].isdigit():
        end += 1
    if not line[end - 1].isdigit():
        end -= 1

    value = int(line[start:end])
    return (start, end, value)


part_numbers = []
gears = []

mark = "\x1b[1;33m"
reset = "\x1b[37m"

print(ny, nx)
for y in range(ny):
    parts = []
    line = data[y]
    x = 0
    while x < endx:
        if is_part_number(y, x, data):
            (start, end, value) = find_number(x, line)
            parts.append((start, end))
            part_numbers.append((value, y, start, end))
            x = end
        elif data[y][x] == "*":
            gears.append((y, x))
            x += 1
        else:
            x += 1
    pretty = []
    last = 0
    for start, end in parts:
        if last < start:
            pretty.append(line[last:start])
        pretty.append(mark)
        pretty.append(line[start:end])
        pretty.append(reset)
        last = end
    if last <= endx:
        pretty.append(line[last:])
    pretty = "".join(pretty)
    pretty = pretty.replace("*", "\x1b[1;32m*\x1b[37m")
    print(pretty)


def coords_of(p: tuple[int, int, int, int]):
    (_, y, start, end) = p
    return ((y, i) for i in range(start, end))


print("Found", len(gears), "gears")
actual_gears = []
# Inefficient solution for dev speed omg
for y, x in gears:
    adjacent = {
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y, x - 1),
        (y, x + 1),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
    }
    adjacent_part_numbers = [
        p for p in part_numbers if any(c in adjacent for c in coords_of(p))
    ]
    if len(adjacent_part_numbers) == 2:
        actual_gears.append(adjacent_part_numbers[0][0] * adjacent_part_numbers[1][0])


print("Part 1:", sum(p[0] for p in part_numbers))
print("Part 2:", sum(actual_gears))
