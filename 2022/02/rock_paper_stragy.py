import sys

moves = []
move_scores = []
outcome_scores = []

move_score = {
    "A": {
        "X": 3,  # Rock
        "Y": 6,  # Paper
        "Z": 0,  # Scissors
    },
    "B": {
        "X": 0,  # Rock
        "Y": 3,  # Paper
        "Z": 6,  # Scissors
    },
    "C": {
        "X": 6,  # Rock
        "Y": 0,  # Paper
        "Z": 3,  # Scissors
    },
}

# Yeah, this is a ridiculous way to do it :)
outcome_score = {
    "A": {
        "X": 3,  # Lose
        "Y": 4,  # Draw
        "Z": 8,  # Win
    },
    "B": {
        "X": 1,  # Lose
        "Y": 5,  # Draw
        "Z": 9,  # Win
    },
    "C": {
        "X": 2,  # Lose
        "Y": 6,  # Draw
        "Z": 7,  # Win
    },
}

for line in sys.stdin.readlines():
    [elf, you] = line.split()
    moves.append((elf, you))
    move_scores.append(ord(you) - ord("W") + move_score[elf][you])
    outcome_scores.append(outcome_score[elf][you])

print("Part 1:", sum(move_scores))
print("Part 1:", sum(outcome_scores))
