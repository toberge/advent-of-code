import sys
from collections import defaultdict


def update(count):
    if count > 6:
        return count - 1
    else:
        return (count - 1) % 7


def simulate_naive(initial_fishes, days):
    """Naive solution that works for Part 1"""
    fishes = initial_fishes[:]
    next_spawnage = sum(fish == 0 for fish in fishes)
    for _ in range(days):
        fishes = [update(fish) for fish in fishes]
        if next_spawnage > 0:
            fishes += [8] * next_spawnage
        next_spawnage = sum(fish == 0 for fish in fishes)

    return len(fishes)


def simulate(initial_fishes, days):
    """Efficient solution that only keeps track of the number of fishes per timer value"""
    fishes = defaultdict(int)
    for days_remaining in initial_fishes:
        fishes[days_remaining] += 1

    for _ in range(days):
        # Remember the number of new fishes to spawn
        newborns = fishes[0]
        next_fishes = defaultdict(int)
        # Age the existing fishes
        for i in range(7):
            next_fishes[(i - 1) % 7] = fishes[i]
        next_fishes[6] += fishes[7]
        next_fishes[7] = fishes[8]
        # Spawn new fishes
        next_fishes[8] = newborns
        fishes = next_fishes

    return sum(fishes.values())


def main():
    fishes = [int(x) for x in input().split(",")]
    for days in [18, 80, 256]:
        print(f"After {days} days:", simulate(fishes, days))


if __name__ == "__main__":
    main()
