def hash(step: str) -> int:
    current_value = 0
    for c in step:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


# TODO this is a mess
class Lens:
    def __init__(self, step: str):
        if step[-1] == "-":
            self.label = step[:-1]
            self.operation = "-"
            self.focal_length = 0
        else:
            self.label = step[:-2]
            self.operation = step[-2]
            self.focal_length = int(step[-1])
        self.hash = hash(self.label)


class Hashmap:
    def __init__(self) -> None:
        self.dict = [[] for _ in range(256)]

    def focusing_power(self) -> int:
        return sum(
            (1 + box) * (1 + slot) * lens.focal_length
            for box, slot, lens in self.lenses()
        )

    def lenses(self):
        for i, box in enumerate(self.dict):
            for j, lens in enumerate(box):
                yield (i, j, lens)

    def execute_all(self, steps: list[Lens]):
        for step in steps:
            self.execute(step)

    def execute(self, step: Lens):
        box = self.dict[step.hash]
        if step.operation == "-":
            self.dict[step.hash] = [l for l in box if l.label != step.label]
        elif any(l.label == step.label for l in box):
            self.dict[step.hash] = [l if l.label != step.label else step for l in box]
        else:
            box.append(step)


if __name__ == "__main__":
    steps = input().split(",")
    control_value = sum(hash(step) for step in steps)
    print("Part 1:", control_value)
    lenses = [Lens(step) for step in steps]
    hashmap = Hashmap()
    hashmap.execute_all(lenses)
    focusing_power = hashmap.focusing_power()
    print("Part 2:", focusing_power)
