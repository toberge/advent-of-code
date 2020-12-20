import sys
from collections import defaultdict


def mask(bitmask, number):
    """Inefficient masking"""
    for i, msk in enumerate(reversed(bitmask)):
        if msk == "X":
            continue
        number &= ~(1 << i)  # unset bit
        if msk == "1":
            number |= 1 << i  # set bit
    return number


def iterate(program: [(str, str)]):
    mem = defaultdict(int)
    bitmask = ""
    for lhs, rhs in program:
        if lhs == "mask":
            bitmask = rhs
        else:
            goal = lhs[4:-1]
            mem[goal] = mask(bitmask, int(rhs))
    return sum(mem.values())


def splitit(lines: [str]):  # don't forget the rstrip!
    return [line.rstrip().split(" = ") for line in lines]


def main():
    # print(mask("1XXXX0X", 11))
    if len(sys.argv) == 1:
        print(iterate(splitit(sys.stdin.readlines())))


if __name__ == "__main__":
    main()
