def read_passports(file):
    dicts = []
    cur = {}

    for line in file.readlines():
        if line == "\n" and cur != {}:
            dicts.append(cur)
            cur = {}
            continue
        for pair in line.split():
            [k, v] = pair.split(":")
            cur[k] = v
    dicts.append(cur)  # whoopsie, I forgot you...

    return dicts
