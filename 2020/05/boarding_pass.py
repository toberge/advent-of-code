def decode_boarding_pass(boarding_pass: str) -> (int, int, int):
    lower, upper = 0, 127
    for code in boarding_pass[:-3]:
        if code == "F":
            upper = (lower + upper) // 2
        elif code == "B":
            lower = round((lower + upper) / 2)
    row = upper
    # if lower < upper:  # THIS WAS MY DOOM
    #     print(lower, upper, boarding_pass[6])
    #     row = upper if boarding_pass[6] == "B" else lower

    lower, upper = 0, 7
    for code in boarding_pass[7:]:
        if code == "L":
            upper = (lower + upper) // 2
        elif code == "R":
            lower = round((lower + upper) / 2)
    col = upper
    # if lower < upper:  # THIS WAS MY DOOM
    #     print(lower, upper, boarding_pass[9])
    #     col = upper if boarding_pass.endswith("R") else lower
    return row, col, row * 8 + col
