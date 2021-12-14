from collections import Counter


def update(pairs: Counter, rules):
    """Update the string (represented by its pairs) according to a set of rules"""
    new_pairs = Counter()
    for pair, insert in rules.items():
        if pair not in pairs:
            continue
        count = pairs[pair]
        new_pairs.update({pair[0] + insert: count, insert + pair[1]: count})
    return new_pairs


def length(pairs):
    return sum(pairs.values()) + 1


def letter_count(pairs: Counter) -> Counter:
    """Find letter counts, use freq of pair as freq of first letter"""
    counts = Counter()
    for pair, count in pairs.items():
        counts.update({pair[0]: count})
    return counts


def result(pairs: Counter, last_letter) -> int:
    """Compute the result"""
    letters = letter_count(pairs)
    # Account for the last letter in the string
    letters.update({last_letter: 1})
    most_common = letters.most_common()
    return most_common[0][1] - most_common[-1][1]


def main():
    base = input()
    last_letter = base[-1]
    input()
    rules = {}
    try:
        while True:
            [pair, insert] = input().split(" -> ")
            rules[pair] = insert
    except EOFError:
        pass

    pairs = Counter([base[i : i + 2] for i in range(len(base) - 1)])
    for i in range(10):
        pairs = update(pairs, rules)
    print("Part 1", result(pairs, last_letter))
    for i in range(30):
        pairs = update(pairs, rules)
    print("Part 2", result(pairs, last_letter))


if __name__ == "__main__":
    main()
