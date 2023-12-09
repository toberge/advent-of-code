import sys
from typing import Iterable
from itertools import pairwise


def differences(sequence: Iterable[int]) -> Iterable[int]:
    return (b - a for a, b in pairwise(sequence))


def pyramid(sequence: list[int]) -> list[list[int]]:
    layers = [sequence, list(differences(sequence))]
    while not all(i == 0 for i in layers[-1]):
        layers.append(list(differences(layers[-1])))
    return layers


def next_value(pyramid: list[list[int]]) -> int:
    nxt = 0
    for i in reversed(range(len(pyramid))):
        nxt = pyramid[i][-1] + nxt
    return nxt


def previous_value(pyramid: list[list[int]]) -> int:
    prev = 0
    for i in reversed(range(len(pyramid))):
        prev = pyramid[i][0] - prev
    return prev


if __name__ == "__main__":
    sequences = [[int(i) for i in l.strip().split()] for l in sys.stdin.readlines()]
    pyramids = [pyramid(s) for s in sequences]
    future_sum = sum(next_value(p) for p in pyramids)
    print("Part 1:", future_sum)
    history_sum = sum(previous_value(p) for p in pyramids)
    print("Part 2:", history_sum)
