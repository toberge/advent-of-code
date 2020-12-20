import sys


def is_valid_password(line):
    [positions, letter, pw] = line.split()
    [one, other] = [int(i) for i in positions.split("-")]
    letter = letter[0]
    return (pw[one - 1] == letter or pw[other - 1] == letter) and not (
        pw[one - 1] == letter and pw[other - 1] == letter
    )


if __name__ == "__main__":
    print(sum(1 for line in sys.stdin.readlines() if is_valid_password(line)))
