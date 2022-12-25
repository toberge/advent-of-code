import sys

encrypted = [int(line) for line in sys.stdin]
n = len(encrypted)


def mix(numbers: list[int], times=1, verbose=False) -> list[int]:
    result = list(range(n))
    if verbose:
        print(numbers)
    for _ in range(times):
        for i, number in enumerate(numbers):
            # Yeah, this is horrible practice.
            # This should have been a linked list haha :)
            # -> with references to the nodes in a list or dict
            origin = result.index(i)
            destination = (origin + number) % (n - 1)
            del result[origin]
            result = result[:destination] + [i] + result[destination:]
            if verbose:
                print([numbers[i] for i in result], number, origin, destination)
    return [numbers[i] for i in result]


def grove_sum(numbers: list[int]) -> int:
    zero = numbers.index(0)
    return sum(
        [
            numbers[(zero + 1000) % n],
            numbers[(zero + 2000) % n],
            numbers[(zero + 3000) % n],
        ]
    )


mixed = mix(encrypted[:], verbose=False)

decrypted = mix([i * 811589153 for i in encrypted], times=10, verbose=False)

print("Part 1", grove_sum(mixed))
print("Part 2", grove_sum(decrypted))
