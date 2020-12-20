def split_groups(lines):
    """Split newline-separated groups"""
    # TODO this should be done in a simpler way (Haskell has splitOn)
    #      - then, why didn't I do this in Haskell in the first place?
    groups = []
    group = []
    for line in lines:
        if line == "\n":
            groups.append(group)
            group = []
        else:
            group.append(line.rstrip())
    groups.append(group)
    return groups
