from collections import Counter

if __name__ == "__main__":
    lns = sorted([int(i) for i in open("input.dat", "r").readlines()])
    print("Maximal difference:", max(lns[i] - lns[i - 1] for i in range(1, len(lns))))
    diffs = Counter(lns[i] - lns[i - 1] for i in range(1, len(lns)))
    print(diffs[1] * diffs[3])
