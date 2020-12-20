import sys
from itertools import combinations


def not_sum_of_those_before(nums: [int], m: int):
    """Part one: A number that is *not* a sum of a pair in the m previous numbers"""
    # O(n * (m choose 2))
    for i in range(m, len(nums)):
        for j, k in combinations(range(1, m + 1), 2):
            if nums[i - j] + nums[i - k] == nums[i]:
                break
        else:
            return nums[i]  # this is it
    return -1


def contiguous_set_equal_to(nums: [int], num: int):
    """Part two: """
    for i, j in combinations(range(len(nums)), 2):
        cand = nums[i : j + 1]
        if sum(cand) == num:
            return min(cand) + max(cand)
    return -1


if __name__ == "__main__":
    nums_ = [int(s) for s in sys.stdin.readlines()]
    weakness = not_sum_of_those_before(nums_, 25)
    print(weakness)
    print(contiguous_set_equal_to(nums_, weakness))
