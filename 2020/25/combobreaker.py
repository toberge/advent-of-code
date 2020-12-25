"""
Looks like a DLP
- we are to find x in 7**x % n = key,
  which is similar to alpha**x % p = beta

Since bruteforce didn't work, it's time for SHANK
(turns out bruteforce was viable with square-and-multiply)

And there IS NO PART TWO
"""

from functools import partial
from itertools import product
from math import floor, sqrt


def encrypt_generic(n, subject, loopsize):
    """Generic version of the puzzle's encryption algorithm"""
    return modpow(subject, loopsize, n)


brutecrypt = partial(encrypt_generic, 20201227, 7)
encrypt = partial(encrypt_generic, 20201227)


def bruteforce(key):
    """
    Stupid bruteforce (written to check if bruteforce actually *works* here)
    Takes several seconds to run, now that the encryption uses square-and-multiply
    """
    res = 0
    loopsize = 1
    while res != key:
        loopsize += 1
        res = brutecrypt(loopsize)
    return loopsize


def modpow(x, e, n):
    """Raises x to e modulo n using the square-and-multiply algorithm"""
    z = 1
    for i in range(e.bit_length() - 1, -1, -1):
        z = z * z % n
        if (e >> i) & 1 == 1:
            z = z * x % n
    return z


def inv(b, n):
    """
    Calculates modular inverse of b modulo n using Euclid's extended algorithm
    Slightly modified but functionally identical version of algorithm 5.3
    in "Cryptography: Theory and Practice"
    """
    a = n
    t = 1
    t0 = 0
    q, r = divmod(a, b)
    while r > 0:
        t, t0 = ((t0 - q * t) % n, t)
        a, b = (b, r)
        q, r = divmod(a, b)
    if b != 1:
        raise ArithmeticError("b has no inverse mod a")
    return t


snd = lambda xs: xs[1]


def shanks(n, a, b):
    """Shanks algorithm for finding log_a(b) mod n"""
    m = floor(sqrt(n))

    lhs = sorted([(j, modpow(a, m * j, n)) for j in range(m)], key=snd)

    rhs = sorted([(i, (b * inv(modpow(a, i, n), n)) % n) for i in range(m)], key=snd)

    j, i = next(  # Raises StopIteration if no such pair exists
        (j, i) for ((j, y1), (i, y2)) in product(lhs, rhs) if y1 == y2
    )

    assert modpow(a, (m * j + i) % n, n) == b
    return (m * j + i) % n


def part_one(cardkey, doorkey):
    """Find the card's loopsize, since that takes the least time of the two"""
    cardsize = shanks(20201227, 7, cardkey)
    # cardsize = bruteforce(cardkey)
    return cardsize, encrypt(doorkey, cardsize)
    # doorsize = shanks(20201227, 7, doorkey)
    # doorsize = bruteforce(doorkey)
    # return doorsize, encrypt(cardkey, doorsize)


def main():
    """Maaaaaaaaaaaaaaaaaain"""
    print(part_one(int(input()), int(input())))


if __name__ == "__main__":
    main()
