import sys

def is_valid_password(line):
    [limits, letter, password] = line.split()
    [lower, upper] = [int(i) for i in limits.split('-')]
    letter = letter[0]
    return lower <= password.count(letter) <= upper

if __name__ == "__main__":
    print(sum(
        1 for line in sys.stdin.readlines() if is_valid_password(line)
    ))
