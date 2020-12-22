def floating_chars(arr: str):
    """Simpler example for testing my idea"""
    res = ""
    for i, c in enumerate(arr):
        if c == "X":
            yield from (res + "A" + extra for extra in floating_chars(arr[i + 1 :]))
            res += "B"
        else:
            res += c
    yield res


if __name__ == "__main__":
    print(list(floating_chars("EEXEXEE")))
