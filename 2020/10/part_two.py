import sys
from functools import lru_cache


def possible_arrangements(adapters: [int]) -> int:
    existing = set(adapters)  # for quick lookup
    last = adapters[-1]

    @lru_cache(maxsize=None)
    def arrangements(start):
        if start != 0 and start not in existing:
            return 0
        if start == last:
            return 1
        return sum(arrangements(i) for i in range(start + 1, start + 4))

    return arrangements(0)


def main():
    adapters = sorted([int(i) for i in sys.stdin.readlines()])
    print(possible_arrangements(adapters))


if __name__ == "__main__":
    main()
