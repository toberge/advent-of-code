import sys

from groups import split_groups


def count_yeses(groups):
    """Count all questions that were answered with a 'yes', per group."""
    return sum(
        len(questions) for questions in (set("".join(group)) for group in groups)
    )


if __name__ == "__main__":
    print(count_yeses(split_groups(sys.stdin.readlines())))
