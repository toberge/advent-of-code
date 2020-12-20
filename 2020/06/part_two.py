import sys
from collections import Counter

from groups import split_groups


def count_unanimous_votes(groups):
    """Count all questions that were answered unanimously, per group."""
    return sum(
        sum(1 for question, count in questions.items() if count == groupsize)
        for questions, groupsize in (
            (Counter("".join(group)), len(group)) for group in groups
        )
    )


if __name__ == "__main__":
    print(count_unanimous_votes(split_groups(sys.stdin.readlines())))
