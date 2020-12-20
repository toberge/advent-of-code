"""
Day 19: Monster Messages

Part one: The OOP solution I shied away from
          - this does NOT work!
"""

import sys
from itertools import takewhile

from rules import parse_rules

TEXT = 0
COMPOSITE = 1
ALTERNATING = 2


# I went wrong somewhere. Welp.
class Rule:
    def __init__(self, rule: str):
        if rule[0] == rule[2] == '"':
            self.type = TEXT
            self.text = rule[1]
        elif rule.find("|") > 0:
            self.type = ALTERNATING
            idx = rule.find("|")
            self.rules = [
                list(map(int, rule[:idx].split())),
                list(map(int, rule[idx + 1 :].split())),
            ]
        else:
            self.type = COMPOSITE
            self.rules = list(map(int, rule.split()))

    def matches(self, rulebook, msg: str):
        lenm = len(msg)
        print(msg)
        if self.type == TEXT:
            return self.text == msg
        if self.type == COMPOSITE:
            return all(
                rulebook[j].matches(
                    rulebook, msg[i : (i + 1) * lenm // len(self.rules)]
                )
                for i, j in enumerate(self.rules)
            )
        if self.type == ALTERNATING:
            return any(  # 2 3 | 3 2
                all(
                    rulebook[j].matches(rulebook, msg[i : (i + 1) * lenm // len(rule)])
                    for i, j in enumerate(rule)
                )  # 2 3
                for rule in self.rules
            )


def main():
    lines = sys.stdin.readlines()
    rules = parse_rules(line.rstrip() for line in takewhile(lambda l: l != "\n", lines))
    msgs = [
        line.rstrip() for line in lines if not line == "\n" and line.find(":") < 0
    ]  # the rest!

    print(Rule("2 3 | 3 2").rules)
    print(Rule("2 3 3 2").rules)
    rules = [
        Rule("4 1 5"),
        Rule("2 3 | 3 2"),
        Rule("4 4 | 5 5"),
        Rule("4 5 | 5 4"),
        Rule('"a"'),
        Rule('"b"'),
    ]
    print(rules[3].matches(rules, "ab"))
    print(rules[3].matches(rules, "ba"))
    print(rules[0].matches(rules, "ababbb"))
    print(rules[0].matches(rules, "ba"))


if __name__ == "__main__":
    main()
