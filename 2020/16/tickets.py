import sys
from functools import partial, reduce
from itertools import chain, permutations, takewhile
from math import factorial

nonempty = lambda l: l != ""


print_tickets = lambda tickets: print(
    "\n".join(",".join(str(i) for i in t) for t in tickets)
)


def valid_field(ranges, field):
    return any(lo <= field <= hi for lo, hi in ranges)


def parse_category(category: str):
    return [
        tuple(int(i) for i in xs)
        for xs in (s.split("-") for s in category.split(": ")[1].split(" or "))
    ]


def parse_input(lines):
    itlines = iter(lines)
    categories = list(map(parse_category, takewhile(nonempty, itlines)))
    next(itlines)  # skip "your ticket:"
    my_ticket = list(
        map(
            lambda s: [int(i) for i in s.split(",")],
            takewhile(nonempty, itlines),
        )
    )[0]
    next(itlines)  # skip "nearby tickets:"
    tickets = list(map(lambda s: [int(i) for i in s.split(",")], itlines))
    return categories, my_ticket, tickets


def valid_tickets(categories, tickets):
    ranges = list(chain.from_iterable(categories))
    return [
        ticket for ticket in tickets if all(map(partial(valid_field, ranges), ticket))
    ]


def part_one(lines):
    categories, _, tickets = parse_input(lines)
    ranges = list(chain.from_iterable(categories))
    return sum(
        field
        for field in chain.from_iterable(tickets)
        if not valid_field(ranges, field)
    )


def categorizes(ranges, tickets, i):
    """This field matches this row"""
    return all(valid_field(ranges, row[i]) for row in tickets)


def part_two(lines):
    categories, my_ticket, tickets = parse_input(lines)
    tickets = valid_tickets(categories, tickets)
    # print_tickets(tickets)
    cat_names = [s.split(":")[0] for s in takewhile(nonempty, lines)]

    num_cats = len(categories)
    num_tickets = len(tickets[0])
    identified = {}  # map from category to field index

    # Stupid attempt
    # for i in range(num_cats):
    #     for j, ranges in enumerate(categories):
    #         if j in identified or i in identified.values():
    #             continue
    #         # print(list(valid_field(ranges, row[i]) for row in tickets))
    #         if categorizes(ranges, tickets, i):
    #             identified[j] = i

    # print(f"Number of possible orderings: {factorial(num_cats)}")

    # Stupid attempt no 2:
    # for step, idx in enumerate(permutations(range(num_cats), num_cats)):
    #     # print(step)
    #     identified = {}
    #     if all(categorizes(categories[i], tickets, j) for i, j in enumerate(idx)):
    #         identified = dict(enumerate(idx))
    #         break

    # Proper attempt no 1:
    for its in range(num_cats):
        if len(identified) == num_cats:
            print("Iterations:", its, "of", num_cats)
            break
        # Find the column(s) that only match(es) one category
        for col in range(num_tickets):
            if col in identified.values():
                continue
            match = -1
            for cat in range(num_cats):
                if cat in identified:
                    continue
                if categorizes(categories[cat], tickets, col):
                    if match >= 0:
                        break  # this is NOT the one that just matches here.
                    match = cat
            else:  # no other match: this is the one!
                identified[match] = col

    print("\n".join(f"{cat_names[k]} -> {my_ticket[v]}" for k, v in identified.items()))
    assert len(identified) == num_cats

    # Multiply together all fields in your ticket that start with "departure"
    return reduce(
        lambda x, y: x * y,
        (
            my_ticket[identified[i]]
            for i in range(num_cats)
            if cat_names[i].startswith("departure")
        ),
        1,
    )


def main():
    lines = [line.rstrip() for line in sys.stdin.readlines()]
    print(part_one(lines))
    print(part_two(lines))


if __name__ == "__main__":
    main()
