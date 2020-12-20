"""
Day 19: Monster Messages

Part one: "maximum recursion depth exceeded"
- nah, it was my fault for not checking that the rule list was sorted!

Part two: 316 is someone else's answer, apparently
          Fixed by looking at what rules 8 and 11 actually mean

Total time: ~216 millis, yay!
"""

import sys
from itertools import takewhile

from rules import parse_rules


def match(rules: [], idx: int, msg: str) -> (bool, int):
    rule = rules[idx]
    if isinstance(rule, str):
        # "x"
        return msg.startswith(rule), len(rule)
    if isinstance(rule[0], list):
        # x y | z w
        for subrule in rule:
            start = 0
            for i in subrule:
                yes, matchlen = match(rules, i, msg[start:])
                start += matchlen
                if not yes:
                    break
            else:
                return True, start
        return False, 0

    # x y z
    start = 0
    for i in rule:
        # print(rulebook[i], msg[start:], end="")
        yes, matchlen = match(rules, i, msg[start:])
        start += matchlen
        # print("match:", matchlen)
        if not yes:
            return False, 0
    return True, start


def rules_match(rulebook, msg_):
    """Doesm msg match the rulebook?"""

    does_match, length = match(rulebook, 0, msg_)
    return does_match and length == len(msg_)


def edited_match(rules, msg):
    """Rule 0: 8 11 = (42)^n(42)^m(31)^m -> n+m > m > 0"""

    msglen = len(msg)
    start = 0
    match_42 = 0
    does_match, matchlen = match(rules, 42, msg)
    # (n + m) matches of rule 42
    while does_match and start < msglen:
        match_42 += 1
        start += matchlen
        does_match, matchlen = match(rules, 42, msg[start:])

    match_31 = 0
    does_match, matchlen = match(rules, 31, msg[start:])
    # m matches of rule 31
    while does_match and start < msglen:
        match_31 += 1
        start += matchlen
        does_match, matchlen = match(rules, 31, msg[start:])

    # Matches rule 0 if the entire message is matched
    # and the match count does not invalidate the rules
    return start == len(msg) and match_42 > match_31 > 0


def main():
    """Day 19"""
    lines = sys.stdin.readlines()
    rules = parse_rules(line.rstrip() for line in takewhile(lambda l: l != "\n", lines))
    msgs = [
        line.rstrip() for line in lines if not line == "\n" and line.find(":") < 0
    ]  # the rest!

    # Part one: Just do it
    print(sum(rules_match(rules, msg) for msg in msgs))

    # Part two: Replace 8 and 11 -> custom code!
    # rules[8] = [[42], [42, 8]]
    # rules[11] = [[42, 31], [42, 11, 31]]
    print(sum(edited_match(rules, msg) for msg in msgs))


if __name__ == "__main__":
    main()
