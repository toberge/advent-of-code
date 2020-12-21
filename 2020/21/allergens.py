"""
Day 21: Allergen Assessment

Rather straightforward.
"""
import sys
from collections import Counter, defaultdict
from itertools import chain

from matplotlib import pyplot as plt


def parse_ingredients(line: str) -> ([str], [str]):
    """Parse an allergen-ingredient pair of lists from an input line"""
    ingredients, allergenes = line.split(" (contains ")
    return ingredients.split(), allergenes[:-1].split(", ")


def parse_input(lines: [str]) -> [([str], [str])]:
    """Eh. Simply map the parse function"""
    return list(map(parse_ingredients, lines))


def count_ingredients(data: [([str], [str])]) -> Counter:
    """Count each ingredient in the input data"""
    return Counter(chain.from_iterable(ingr for ingr, _ in data))


def count_allergens(data: [([str], [str])]) -> Counter:
    """Count each allergen in the input data"""
    return Counter(chain.from_iterable(allerg for _, allerg in data))


def plot_things(data: [([str], [str])], identified: {str: str}):
    """Just plot some things (trigger with 'plot' arg)"""
    allerg_counts = count_allergens(data)
    plt.xkcd()
    plt.title("Dishes with allergens")
    plt.bar(allerg_counts.keys(), allerg_counts.values())
    plt.xlabel("Allergens")
    plt.ylabel("Dishes")
    plt.show()

    rev = {v: k for k, v in identified.items()}
    ingr_counts = count_ingredients(data)
    identified_counts = {
        rev[ingr]: count for ingr, count in ingr_counts.items() if ingr in rev
    }
    plt.title("Instances of allergens in dishes")
    plt.bar(identified_counts.keys(), identified_counts.values())
    plt.xlabel("Allergens")
    plt.ylabel("Instances")
    plt.show()


def map_allergs(data):
    """Map allergens to the counts of ingredients they are listed behind"""
    allerg_map: {str: Counter} = defaultdict(Counter)
    for ingrs, allergs in data:
        for allerg in allergs:
            allerg_map[allerg].update(ingrs)
    return allerg_map


def identify_allergs(data: [([str], [str])]) -> {str: str}:
    """Identify the one-to-one mapping of allergen to ingredient"""
    identified = {}
    allerg_map = map_allergs(data)
    num_allerg = len(allerg_map)

    # This algorithm is similar to the one in day 16
    # - but greater care might've been taken in its implementation.
    # It is slower than it had to be.
    while len(identified) < num_allerg:
        for allerg, counts in allerg_map.items():
            # Skip those that are found
            if allerg in identified:
                continue
            # Find the most common ingredient with this allergene
            ingr, count = counts.most_common(1)[0]
            # Check if there's a conflicting ingredient
            if counts.most_common(2)[1][1] == count:
                continue
            identified[allerg] = ingr
            # Reset counts for this ingredient
            for counts_ in allerg_map.values():
                counts_[ingr] = 0

    return identified


def part_one(identified: {str: str}, data: [([str], [str])]) -> int:
    """Number of appearances of ingredients that *do not* contain allergens"""
    dangerous = set(identified.values())
    return sum(
        count
        for ingr, count in count_ingredients(data).items()
        if ingr not in dangerous
    )


def part_two(identified: {str: str}) -> str:
    """Ingredients in the identified allergen-ingredient pairs, sorted by allergen"""
    return ",".join(
        ingr for allerg, ingr in sorted(identified.items(), key=lambda xs: xs[0])
    )


def main():
    data = parse_input(line.rstrip() for line in sys.stdin.readlines())
    identified = identify_allergs(data)
    if len(sys.argv) > 1 and "plot" in sys.argv:
        plot_things(data, identified)
    print(part_one(identified, data))
    print(part_two(identified))


if __name__ == "__main__":
    main()
