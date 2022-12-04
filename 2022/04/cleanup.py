import sys

contained = 0
overlap = 0

for line in (l.rstrip("\n") for l in sys.stdin):
    first, second = [tuple(int(x) for x in pair.split("-")) for pair in line.split(",")]

    # Fully contained
    if first[0] >= second[0] and first[1] <= second[1]:
        contained += 1
    elif second[0] >= first[0] and second[1] <= first[1]:
        contained += 1
    # One extra condition for overlap
    elif first[0] <= second[1] <= first[1] or second[0] <= first[1] <= second[1]:
        overlap += 1

print("Part 1:", contained)
print("Part 2:", contained + overlap)
