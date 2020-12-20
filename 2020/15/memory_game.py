"""
Day 14: Memory Game
For once, a second part that doesn't change any requirements
Part two takes 12 seconds to run...
"""

import sys

split_nums = lambda s: [int(i) for i in s.split(",")]


def memory_game(nums, target=2020):
    idx = {}  # index of last instance of each number
    for i, num in enumerate(
        nums[:-1]
    ):  # all except the last – it is handled specially!
        idx[num] = i + 1
    num = nums[-1]
    for i in range(len(nums), target):  # i is one less than this numbers' number
        if num in idx:  # not new
            # print(f"{i+1}: {num} in idx, num = {i} - {idx[num]} = {i - idx[num]}")
            oldnum = num
            num = i - idx[num]
            idx[oldnum] = i
        else:
            idx[num] = i
            num = 0
            # print(f"{i+1}: 0")
    return num


def main():
    if len(sys.argv) > 1:
        nums = split_nums(sys.argv[1])
    else:
        nums = split_nums(input())
    print(memory_game(nums, 30000000))


if __name__ == "__main__":
    main()
