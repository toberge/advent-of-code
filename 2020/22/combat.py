"""
Day 22: Crab Combat

Part one: Play the game!
          Written in half an hour or less

Part two: Play a recursive game!
          Written in less than (half) an hour, perhaps
"""

import sys
from collections import deque
from itertools import islice, takewhile


def score(deck: deque):
    """Sum of card values weighted by position in the deck"""
    return sum(card * weight for card, weight in zip(deck, range(len(deck), 0, -1)))


def combat(deck1, deck2):
    """Play a standard game of Combat"""
    deck1 = deque(deck1)
    deck2 = deque(deck2)

    while len(deck1) > 0 and len(deck2) > 0:
        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if card1 > card2:  # player one won
            deck1.extend([card1, card2])
        elif card2 > card1:  # player two won
            deck2.extend([card2, card1])

    return score(deck1 if len(deck1) > 0 else deck2)


def recursive_combat(deck1, deck2) -> (int, int):
    """Play a recursive game of Combat"""
    deck1 = deque(deck1)
    deck2 = deque(deck2)
    prev_games = set()

    while len(deck1) > 0 and len(deck2) > 0:
        key = (str(deck1), str(deck2))
        if key in prev_games:
            # Prevent infinite loops
            return 1, score(deck1)
        prev_games.add(key)

        # Draw cards
        card1 = deck1.popleft()
        card2 = deck2.popleft()

        # New rules: Compare remaining amount to card value
        if len(deck1) >= card1 and len(deck2) >= card2:
            # Recurse with copies!
            winner, _ = recursive_combat(
                deque(islice(deck1, 0, card1)), deque(islice(deck2, 0, card2))
            )
        else:  # Can't recurse, use higher-val as usual
            winner = 1 if card1 > card2 else 2

        if winner == 1:  # player one won
            deck1.extend([card1, card2])
        else:  # player two won
            deck2.extend([card2, card1])

    return (1, score(deck1)) if len(deck1) > 0 else (2, score(deck2))


def main():
    lines = (line.rstrip() for line in sys.stdin.readlines())
    next(lines)  # Player 1:
    deck1 = [int(line) for line in takewhile(lambda l: l != "", lines)]
    next(lines)  # Player 2:
    deck2 = [int(line) for line in lines]

    # Part one:
    print(combat(deck1, deck2))
    # Part two:
    print(recursive_combat(deck1, deck2))


if __name__ == "__main__":
    main()
