import sys
from functools import reduce


SYNTAX_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

COMPLETION_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


OPENER_OF = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

CLOSER_OF = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


OPENERS = set("([{<")
CLOSERS = set("}])>")


def syntax_score(line: str) -> int:
    stack = []
    for bracket in line:
        if bracket in OPENERS:
            stack.append(bracket)
        elif OPENER_OF[bracket] != stack.pop():
            return SYNTAX_SCORE[bracket]
    return 0


def completion_string(line: str) -> int:
    stack = []
    for bracket in line:
        if bracket in OPENERS:
            stack.append(bracket)
        else:
            stack.pop()
    # Complete the string by appending brackets in order of recency
    return "".join(CLOSER_OF[bracket] for bracket in reversed(stack))


def completion_score(string: str) -> int:
    return reduce(lambda total, c: 5 * total + COMPLETION_SCORE[c], string, 0)


def main():
    lines = [line.strip() for line in sys.stdin.readlines()]
    # Find the total error score of all lines:
    print("Part 1:", sum(syntax_score(line) for line in lines))
    # Go forth with only incomplete lines:
    lines = [line for line in lines if syntax_score(line) == 0]
    # Find middle completion score
    sorted_scores = sorted(completion_score(completion_string(line)) for line in lines)
    print("Part 2:", sorted_scores[len(sorted_scores) // 2])


if __name__ == "__main__":
    main()
