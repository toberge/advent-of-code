import sys
from collections import defaultdict
from typing import Iterable

# def floating_bits(number: str) -> Iterable[int]:


def mask(bitmask, number, start=0) -> Iterable[int]:
    """Bitmask with *floating* bits. Takes a BE bitmask."""
    print(start, len(list(zip(range(start, len(bitmask)), bitmask[start:]))))
    for i, msk in zip(range(start, len(bitmask)), bitmask[start:]):
        if msk == "X":  # woop woop
            # use the *current state* of the number!
            # print(f"{number:b}")
            yield from mask(bitmask[:i] + [0] + bitmask[i + 1 :], number, start=i + 1)
            yield from mask(
                bitmask[:i] + [1] + bitmask[i + 1 :], number | (1 << i), start=i + 1
            )
            # number |= 1 << i  # go on with this version
        elif msk == "1":
            number |= 1 << i  # set bit
        # if 0, ignore
    print(f"{number:b}")
    yield number


def iterate(program: [(str, str)]):
    mem = defaultdict(int)
    bitmask = ""
    for lhs, rhs in program:
        if lhs == "mask":
            bitmask = list(reversed(rhs))
        else:
            print(set(mask(bitmask, int(lhs[4:-1]))))
            for i in set(mask(bitmask, int(lhs[4:-1]))):
                mem[i] = int(rhs)
    return sum(mem.values())


def splitit(lines: [str]):  # don't forget the rstrip!
    return [line.rstrip().split(" = ") for line in lines]


def main():
    if len(sys.argv) == 1:
        print(iterate(splitit(sys.stdin.readlines())))


if __name__ == "__main__":
    main()
