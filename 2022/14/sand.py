import sys

blocks = set()

sand = set()

for line in sys.stdin:
    line = line.rstrip()

    points = (eval(token) for token in line.split(" -> "))
    start = next(points)
    blocks.add(start)

    for point in points:
        # x same, vertical
        if point[0] == start[0] and point[1] != start[1]:
            diff = point[1] - start[1]
            delta = int(diff / abs(diff))
            for i in range(1, abs(diff)):
                blocks.add((start[0], start[1] + i * delta))
        # y same, horizontal
        elif point[1] == start[1] and point[0] != start[0]:
            diff = point[0] - start[0]
            delta = int(diff / abs(diff))
            for i in range(1, abs(diff)):
                blocks.add((start[0] + i * delta, start[1]))

        blocks.add(point)
        start = point

# y is downwards
abyss = max(block[1] for block in blocks) + 1
spawn = (500, 0)
pos = spawn

while pos[1] < abyss:
    down = (pos[0], pos[1] + 1)
    left = (pos[0] - 1, pos[1] + 1)
    right = (pos[0] + 1, pos[1] + 1)

    if down not in blocks and down not in sand:
        pos = down
    elif left not in blocks and left not in sand:
        pos = left
    elif right not in blocks and right not in sand:
        pos = right
    else:
        sand.add(pos)
        pos = spawn

print("Part 1:", len(sand))

# y is downwards
floor = max(block[1] for block in blocks) + 1
spawn = (500, 0)
pos = spawn
sand = set()

while True:
    down = (pos[0], pos[1] + 1)
    left = (pos[0] - 1, pos[1] + 1)
    right = (pos[0] + 1, pos[1] + 1)

    if pos[1] == floor:
        sand.add(pos)
        pos = spawn
    elif down not in blocks and down not in sand:
        pos = down
    elif left not in blocks and left not in sand:
        pos = left
    elif right not in blocks and right not in sand:
        pos = right
    else:
        sand.add(pos)
        if pos == spawn:
            break
        pos = spawn

print("Part 2:", len(sand))
