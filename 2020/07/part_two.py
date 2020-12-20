import sys
from itertools import chain

from bags import parse_bags


def _inner_counter(target, bags):
    if target not in bags:
        return 1
    neighbours = bags[target]
    # print(neighbours)
    # print(
    #     list(
    #         chain.from_iterable(
    #             map(lambda x: x * count, _inner_counter(bag, bags, count))
    #             for bag, count in neighbours
    #         )
    #     )
    # )
    # print([(count, "*", _inner_counter(bag, bags)) for bag, count in neighbours])
    return 1 + sum(count * _inner_counter(bag, bags) for bag, count in neighbours)


def count_bags_within(target, bags):
    """Counts the number of bags that must be contained in a bag of the target type"""
    return _inner_counter(target, bags) - 1  # the outer bag does not contain itself


if __name__ == "__main__":
    print(count_bags_within("shiny gold", parse_bags(sys.stdin.readlines())[1]))
