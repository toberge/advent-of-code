import sys


def find_sum_naive(data, sum_):
    """O(n²) of course"""
    for a in data:
        for b in data:
            if a + b == sum_:
                return a * b
    return -1


def find_sum(data, sum_):
    """O(n) with a set"""
    others = set()
    for a in data:
        if sum_ - a in others:
            return a * (sum_ - a)
        others.add(a)
    return -1


if __name__ == "__main__":
    nums = [int(line) for line in sys.stdin.readlines()]
    print(find_sum_naive(nums, 2020))
    print(find_sum(nums, 2020))
