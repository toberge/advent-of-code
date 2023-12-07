import sys
from dataclasses import dataclass, field
from collections import Counter
from typing import Union


@dataclass
class OfAKind:
    n: int
    v: str


@dataclass
class FullHouse:
    triplet: str
    pair: str


@dataclass
class TwoPair:
    v: str
    w: str


@dataclass
class OnePair:
    v: str


@dataclass
class HighCard:
    pass


Type = Union[OfAKind, FullHouse, TwoPair, OnePair, HighCard]


def rankof(t: Type):
    match t:
        case OfAKind(5, _):
            return 6
        case OfAKind(4, _):
            return 5
        case FullHouse(_, _):
            return 4
        case OfAKind(3, _):
            return 3
        case TwoPair(_, _):
            return 2
        case OnePair(_):
            return 1
        case HighCard():
            return 0
    return -1


def typeof(cards: str):
    counts = Counter(cards)
    match counts.most_common(2):
        case [(x, 5), *_]:
            return OfAKind(5, x)
        case [(x, 4), *_]:
            return OfAKind(4, x)
        case [(x, 3), (y, 2)]:
            return FullHouse(x, y)
        case [(x, 3), *_]:
            return OfAKind(3, x)
        case [(x, 2), (y, 2)]:
            return TwoPair(x, y)
        case [(x, 2), *_]:
            return OnePair(x)
    return HighCard()


# TODO clean up here -_-
card_values = "123456789TJQKA"
cards_without_joker = "123456789TQKA"
card_strength = dict(zip(card_values, range(0, 14)))
part_2_card_strength = dict(zip("J123456789TQKA", range(0, 14)))
card_strength = part_2_card_strength


def permutationsof(cards: str):
    yield from _permutationsof("", cards)


def _permutationsof(left: str, right: str):
    if len(right) == 0:
        yield left
        return

    if right[0] == "J":
        for j in (
            _permutationsof(left + card, right[1:]) for card in cards_without_joker
        ):
            yield from j
    else:
        yield from _permutationsof(left + right[0], right[1:])


def valueof(v: str):
    return card_strength[v]


@dataclass
class Hand:
    cards: str
    bid: int
    type: Type = field(init=False)
    type_rank: int = field(init=False)
    jokered_type: Type = field(init=False)
    jokered_rank: int = field(init=False)

    @staticmethod
    def parse(line: str):
        [cards, bid] = line.strip().split()
        return Hand(cards, int(bid))

    def __post_init__(self):
        self.type = self._type()
        self.type_rank = self._type_rank()
        self.jokered_type = self._jokered_type()
        self.jokered_rank = self._jokered_rank()

    def _type(self) -> Type:
        return typeof(self.cards)

    def _type_rank(self) -> int:
        return rankof(self.type)

    def _jokered_type(self) -> Type:
        return max(
            (typeof(permutation) for permutation in permutationsof(self.cards)),
            key=lambda x: rankof(x),
        )

    def _jokered_rank(self) -> int:
        return rankof(self.jokered_type)

    def __lt__(self, other: "Hand") -> bool:
        # TODO refactor with type vs joker
        # (maybe use two classes)
        if self.jokered_rank != other.jokered_rank:
            return self.jokered_rank < other.jokered_rank

        for s, o in zip(map(valueof, self.cards), map(valueof, other.cards)):
            if s == o:
                continue
            return s < o
        return False


# TODO fix part 1/2 distinction
if __name__ == "__main__":
    hands = [Hand.parse(line) for line in sys.stdin.readlines()]

    with_rank = list(zip(range(len(hands)), sorted(hands)))
    # print("\n".join(str(h) for h in with_rank))
    total_winnings = sum(h.bid * (i + 1) for i, h in with_rank)

    print("Part 1:", total_winnings)

    # Reorder cards
    card_strength = dict(zip("J123456789TQKA", range(0, 14)))

    with_rank = list(zip(range(len(hands)), sorted(hands)))
    total_winnings = sum(h.bid * (i + 1) for i, h in with_rank)
    print("Part 2:", total_winnings)
