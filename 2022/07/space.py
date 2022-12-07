import sys
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Union


@dataclass
class File:
    name: str
    size: int

    def __repr__(self):
        return f"{self.name} {self.size}"


@dataclass
class Folder:
    name: str
    parent: Optional["Folder"] = None
    children: dict[str, Union[File, "Folder"]] = field(default_factory=dict)

    @cached_property
    def size(self) -> int:
        return sum(child.size for child in self.children.values())

    def __repr__(self) -> str:
        return f"- {self.name} {self.size}\n" + "\n".join(
            "  " + "\n  ".join(repr(child).split("\n"))
            for child in self.children.values()
        )


lines = (l.rstrip("\n") for l in sys.stdin)
line = next(lines)

root = Folder("/")
current: Folder = root

try:
    while True:
        command = line.split()

        if command[1] == "cd":
            if command[2] == "..":
                if current.parent is None:
                    raise Exception("No parent")
                current = current.parent
            elif command[2] == "/":
                pass
            else:
                current = current.children[command[2]]
            line = next(lines)

        elif command[1] == "ls":
            line = next(lines)
            while not line.startswith("$"):
                [token, name] = line.split()
                if token == "dir":
                    current.children[name] = Folder(name, parent=current)
                else:
                    current.children[name] = File(name, int(token))
                line = next(lines)

except StopIteration:
    pass

print(root)

stack = [root]

total_size = 0
minimum_to_free = 30000000 - (70000000 - root.size)
minimum = root

while len(stack) > 0:
    current = stack.pop()
    if current.size <= 100000:
        total_size += current.size
    elif minimum_to_free <= current.size < minimum.size:
        minimum = current
    stack.extend(
        child for child in current.children.values() if isinstance(child, Folder)
    )

print("Part 1:", total_size)
print("Part 2:", minimum.name, minimum.size)
