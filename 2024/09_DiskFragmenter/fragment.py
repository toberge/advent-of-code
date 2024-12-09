from dataclasses import dataclass


@dataclass
class Block:
    id: int
    start: int
    length: int


EMPTY = -1


def parse(disk):
    data = []
    i = 0
    is_file = True
    for block in disk:
        data.extend(([i] if is_file else [EMPTY]) * int(block))
        i += int(is_file)
        is_file = not is_file
    return data


def blockify(disk):
    blocks = []
    id = 0
    pos = 0
    is_file = True
    for block in disk:
        size = int(block)
        blocks.append(Block(id if is_file else EMPTY, pos, size))
        pos += size
    return blocks


def fragment(data):
    data = data[:]
    end = len(data) - 1
    start = 0
    while start < end:
        if data[start] == EMPTY:
            while data[end] == EMPTY:
                end -= 1
            data[start] = data[end]
            data[end] = -1
            end -= 1
        start += 1
    return data


def dontfragment(blocks):
    pass


checksum = lambda data: sum(d * i if d >= 0 else 0 for i, d in enumerate(data))

if __name__ == "__main__":
    disk = input()
    raw_disk = parse(disk)
    blocks = blockify(disk)

    fragmented = fragment(raw_disk)
    print("Part 1:", checksum(fragmented))
