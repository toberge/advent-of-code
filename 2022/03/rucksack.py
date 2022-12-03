import sys

priorities = 0
badges = 0


def priority(item: str):
    if item.isupper():
        return ord(item) - ord("A") + 27
    return ord(item) - ord("a") + 1


count = 0
group = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

for line in (l.rstrip("\n") for l in sys.stdin):
    first = set(line[: len(line) // 2])
    second = set(line[len(line) // 2 :])
    overlap = first.intersection(second)
    priorities += sum(priority(x) for x in overlap)

    group.intersection_update(set(line))
    if count >= 2:
        count = 0
        badges += priority(next(iter(group)))
        group = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    else:
        count += 1

print("Part 1:", priorities)
print("Part 2:", badges)
