import sys

encrypted = [int(line) for line in sys.stdin]
n = len(encrypted)


def mix(numbers: list[int], verbose=False) -> list[int]:
    result = list(range(n))
    if verbose:
        print(numbers)
    for i, number in enumerate(numbers):
        origin = result.index(i)
        destination = (origin + number) % n
        if number < 0 and destination > origin:
            destination -= 1
        # if index + number > n or index + number < 0:
        # destination += int(number > 0) - int(number < 0)
        del result[origin]
        result = result[:destination] + [i] + result[destination:]
        if verbose:
            print([numbers[i] for i in result], number, origin, destination)
    return [numbers[i] for i in result]


def grove_sum(numbers: list[int]) -> int:
    zero = numbers.index(0)
    print(
        numbers[(zero + 1000) % n],
        numbers[(zero + 2000) % n],
        numbers[(zero + 3000) % n],
    )
    return sum(
        [
            numbers[(zero + 1000) % n],
            numbers[(zero + 2000) % n],
            numbers[(zero + 3000) % n],
        ]
    )


mixed = mix(encrypted[:], verbose=True)


print("Part 1", grove_sum(mixed))
