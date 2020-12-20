"""
Day V: Binary Boarding
"""

import sys

from boarding_pass import decode_boarding_pass


def some_sort_of_attempt(passes):
    """Brute force is also a solution, but this is not a solution"""
    passes = sorted(id_ for _, _, id_ in passes)
    existing = set(passes)
    for id1 in passes:
        for id2 in passes:
            if abs(id1 - id2) == 2 and (min(id1, id2) + 1) not in existing:
                return min(id1, id2) + 1


def bad_solution(passes):
    """This is also a solution, in the end"""
    passes = sorted(id_ for _, _, id_ in passes)
    existing = set(passes)
    prev = passes[0] - 1
    for id_ in passes:
        if id_ - 1 != prev and id_ - 1 not in existing:
            return id_ - 1
        prev = id_


def find_my_boarding_pass(passes):
    """However, this is a better solution that does not require sorting"""
    passes = [id_ for _, _, id_ in passes]
    existing = set(passes)
    for i in range(min(passes), max(passes)):
        if i not in existing:
            return i


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    print(find_my_boarding_pass(map(decode_boarding_pass, lines)))
    print(bad_solution(map(decode_boarding_pass, lines)))
