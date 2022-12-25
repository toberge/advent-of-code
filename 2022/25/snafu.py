import sys


def digit(c: str):
    if c.isnumeric():
        return int(c)
    else:
        return -1 if c == "-" else -2


def snafu2decimal(snafu: str):
    return sum(digit(d) * 5**i for i, d in enumerate(reversed(snafu)))


def decimal2pental(decimal: int):
    pental = []
    base = 5
    while decimal // base > 0:
        base *= 5
    base //= 5
    while base > 1:
        pental.append(str(decimal // base))
        decimal %= base
        base //= 5
    pental.append(str(decimal))
    return "".join(pental)


def pental2snafu(pental: str):
    carry = 0
    snafu = []
    for digit in reversed([int(c) for c in pental]):
        digit += carry
        if digit < 3:
            snafu.append(str(digit))
            carry = 0
        elif digit < 5:
            snafu.append("=" if digit == 3 else "-")
            carry = 1
        else:
            snafu.append("0")
            carry = 1
    return "".join(reversed(snafu))


lines = (l.rstrip() for l in sys.stdin)

decimal = sum(snafu2decimal(number) for number in lines)
pental = decimal2pental(decimal)
snafu = pental2snafu(pental)

print(
    f"Part 1: {decimal} \n"
    f"\t= {pental} ({int(pental, base=5)}) in quinary\n"
    f"\t= {snafu } ({snafu2decimal(snafu)}) in balanced quinary (SNAFU)"
)
