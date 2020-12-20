import re
import sys
from collections import defaultdict


# Python does not like -> ({[]}, {[(str, int)]})
def parse_bags(lines: [str]):
    """Returns a reverse lookup table for 'bags that can contain this one'"""
    lookup: {[]} = defaultdict(list)
    rules: {[(str, int)]} = defaultdict(list)

    for line in lines:
        [source, rest] = line.rstrip().split(" bags contain ")
        if rest != "no other bags.":
            rest = re.sub(r" bags?\.", "", rest)
            rule = []
            for bag in re.split(r" bags?, ", rest):
                [count, bag] = bag.split(" ", 1)
                lookup[bag].append(source)
                rule.append((bag, int(count)))
            rules[source] = rule

    return (lookup, rules)


if __name__ == "__main__":
    print(parse_bags(sys.stdin.readlines()))
