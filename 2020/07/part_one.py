import sys
from itertools import chain

from bags import parse_bags


def _inner_counter(target, bags, found):
    """Find the bags that can contain this one and are not present in found"""
    if target not in bags:
        return
    neighbours = bags[target]
    yield from neighbours
    yield from chain.from_iterable(
        _inner_counter(nxt, bags, found.union(neighbours))
        for nxt in neighbours
        if nxt not in found
    )


def count_bags_containing(target, bags):
    """Counts the number of bags that *eventually* contain the target type"""
    return len(set(_inner_counter(target, bags, set(target))))


if __name__ == "__main__":
    print(count_bags_containing("shiny gold", parse_bags(sys.stdin.readlines())[0]))
