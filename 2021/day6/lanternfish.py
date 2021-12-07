import sys


def update(count):
    if count > 6:
        return count - 1
    else:
        return (count - 1) % 7


def simulate(initial_fishes, days):
    """Naive solution that works for Part 1"""
    fishes = initial_fishes[:]
    next_spawnage = 0
    for i in range(days):
        if i % 10 == 0:
            print(i, len(fishes))
        fishes = [update(fish) for fish in fishes]
        if next_spawnage > 0:
            fishes += [8] * next_spawnage
        next_spawnage = sum(fish == 0 for fish in fishes)

    return len(fishes)


def main():
    fishes = [int(x) for x in input().split(",")]
    for days in [18, 80, 256]:
        print(f"After {days} days:", simulate(fishes, days))


if __name__ == "__main__":
    main()
