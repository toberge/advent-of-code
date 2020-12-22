import sys
from collections import defaultdict
from typing import Iterable


def bitmasks(floatmask) -> Iterable[int]:
    """All possible bitmasks from a bitmask with floating bits"""
    bitmask = ""
    for i, msk in enumerate(floatmask):
        if msk == "X":
            yield from (
                bitmask + "Z" + restmask for restmask in bitmasks(floatmask[i + 1 :])
            )
            bitmask += "1"
        else:
            bitmask += msk
    yield bitmask


def mask(bitmask, number):
    """Mask a number with a concrete bitmask"""
    for i, msk in zip(range(len(bitmask)), reversed(bitmask)):
        if msk == "1":  # Forcibly one
            number |= 1 << i
        elif msk == "Z":  # Forcibly zero
            number = ~((~number) | (1 << i))
        # Unchanged otherwise
    return number


def iterate(program: [(str, str)]):
    """Emulate initialization of the docking program"""
    mem = defaultdict(int)
    floatmask = ""
    for lhs, rhs in program:
        if lhs == "mask":
            floatmask = rhs
        else:
            addr = int(lhs[4:-1])
            val = int(rhs)
            for bitmask in bitmasks(floatmask):
                mem[mask(bitmask, addr)] = val
    return sum(mem.values())


def splitit(lines: [str]):  # don't forget the rstrip!
    return [line.rstrip().split(" = ") for line in lines]


def main():
    if len(sys.argv) == 1:
        print(iterate(splitit(sys.stdin.readlines())))


if __name__ == "__main__":
    main()
