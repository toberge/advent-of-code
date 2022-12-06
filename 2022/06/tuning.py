def marker_position(buffer, characters_in_marker):
    for i in range(len(buffer) - characters_in_marker):
        candidate = buffer[i : i + characters_in_marker]
        if len(set(candidate)) == characters_in_marker:
            return i + characters_in_marker


buffer = input()

print("Part 1:", marker_position(buffer, 4))
print("Part 2:", marker_position(buffer, 14))

# Note to self:
# I didn't spend 7 minutes from part 1 to part 2,
# but was delayed when inputting my answer since we were making porridge :)
