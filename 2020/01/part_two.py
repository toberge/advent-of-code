"""
Naive solution
"""

import sys


def find_sum_naive(data, sum_):
    """O(n³), atrocious"""
    for a in data:
        for b in data:
            for c in data:
                if a + b + c == sum_:
                    return a * b * c
    return -1


def find_sum(data, sum_):
    """O(n²), slightly better"""
    others = set()
    for a in data:
        for b in data:
            if sum_ - a - b in others:
                return a * b * (sum_ - a)
            others.add(a)
    return -1


if __name__ == "__main__":
    nums = [int(line) for line in sys.stdin.readlines()]
    print(find_sum_naive(nums, 2020))
    print(find_sum(nums, 2020))
