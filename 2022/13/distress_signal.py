from functools import reduce
import sys
from typing import Union


class InRightOrder(Exception):
    pass


class NotInRightOrder(Exception):
    pass


def compare(left: Union[list, int], right: Union[list, int], verbose=False):
    if verbose:
        print("Comparing", left, "to", right)
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            raise InRightOrder("Left int < right int")
        if left > right:
            raise NotInRightOrder("Left int > right int")
    elif isinstance(left, list) and isinstance(right, list):
        compare_lists(left, right)
    elif isinstance(left, int) and isinstance(right, list):
        compare_lists([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        compare_lists(left, [right])


def compare_lists(left: list, right: list):
    for l, r in zip(left, right):
        compare(l, r)

    if len(left) < len(right):
        raise InRightOrder("Left ran out of items")
    if len(left) > len(right):
        raise NotInRightOrder("Right ran out of items")


class Comparable:
    def __init__(self, packet: list):
        self.packet = packet

    def __lt__(self, other: "Comparable"):
        try:
            compare(self.packet, other.packet)
        except InRightOrder:
            return True
        except NotInRightOrder:
            return False

    def __gt__(self, other: "Comparable"):
        try:
            compare(self.packet, other.packet)
        except InRightOrder:
            return False
        except NotInRightOrder:
            return True


def comparable(packet: list):
    return Comparable(packet)


lines = (l.rstrip() for l in sys.stdin)

correct = 0
incorrect = 0
correct_sum = 0
index = 1

verbose = False
dividers = [[[2]], [[6]]]
packets = dividers[:]

for left in lines:
    # Abuse iterators
    if left == "":
        left = next(lines)
    right = next(lines)

    # Abuse eval
    left = eval(left)
    right = eval(right)
    packets.extend([left, right])

    if verbose:
        print(
            left,
            right,
        )

    # Abuse exceptions
    try:
        compare(left, right, verbose)
    except InRightOrder as e:
        if verbose:
            print(e.__class__.__name__, e)
        correct += 1
        correct_sum += index
    except NotInRightOrder as e:
        if verbose:
            print(e.__class__.__name__, e)
        incorrect += 1

    index += 1

print(correct, "correct,", incorrect, "incorrect")
print("Part 1:", correct_sum)

# Abuse sorting
packets = sorted(packets, key=comparable)
if verbose:
    print("\n".join(str(packet) for packet in packets))

decoder_key = reduce(
    lambda a, b: a * b,
    (i + 1 for i, packet in enumerate(packets) if packet in dividers),
)
print("Part 2:", decoder_key)
