"""
Day 19: Monster Messages

This version does NOT work!
"""

import sys
from itertools import takewhile

from rules import parse_rules

allstr = lambda xs: all(isinstance(x, str) for x in xs)


def lookup(rules: [], indices: []):
    looks = [rules[i] if isinstance(i, int) else i for i in indices]
    # print(looks)
    if allstr(looks):
        return "".join(looks)
    return indices


def bloody_regex(rules: []) -> str:

    while not isinstance(rules[0], str):
        for i, rule in enumerate(reversed(rules)):
            i = len(rules) - 1 - i
            if isinstance(rule, str):
                pass  # it's done
            elif isinstance(rule[0], list):
                lhs = lookup(rules, rule[0])
                rhs = lookup(rules, rule[1])
                if allstr([lhs, rhs]):
                    rules[i] = "(" + lhs + "|" + rhs + ")"
                else:
                    rules[i] = [lhs, rhs]
                # print("->", rules[i])
            else:
                rules[i] = lookup(rules, rule)

    # print(rules)

    return rules[42]


def main():
    lines = sys.stdin.readlines()
    rules = parse_rules(line.rstrip() for line in takewhile(lambda l: l != "\n", lines))
    msgs = [
        line.rstrip() for line in lines if not line == "\n" and line.find(":") < 0
    ]  # the rest!
    print(rules)
    regex = bloody_regex(rules)
    print(regex)
    # for msg in msgs:
    #     print(msg, (rules, msg))


if __name__ == "__main__":
    main()
