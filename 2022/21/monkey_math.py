import sys
from typing import Union, Optional
from dataclasses import dataclass


Operation = Union[int, tuple[str, str, str]]


OP = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
}

# If left monkey is unknown, what must it be equal to?
# Params: known branch and what it must equal
INV_OP_LEFT = {
    "+": lambda a, b: b - a,
    "-": lambda a, b: b + a,
    "*": lambda a, b: b // a,
    "/": lambda a, b: b * a,
}

# If right monkey is unknown, what must it be equal to?
INV_OP_RIGHT = {
    "+": lambda a, b: b - a,
    "-": lambda a, b: a - b,
    "*": lambda a, b: b // a,
    "/": lambda a, b: a // b,
}


@dataclass
class Monkey:
    name: str
    value: Union[str, int]
    parent: Optional["Monkey"] = None
    left: Optional["Monkey"] = None
    right: Optional["Monkey"] = None

    is_unknown = False

    def eval(self) -> int:
        if isinstance(self.value, str):
            return OP[self.value](self.left.eval(), self.right.eval())
        return self.value

    def find(self, name="humn") -> Optional["Monkey"]:
        if self.name == name:
            return self
        if isinstance(self.value, str):
            left = self.left.find()
            right = self.right.find()
            return left if left is not None else right
        return None

    def mark_as_unknown(self):
        self.is_unknown = True
        if self.parent is not None:
            self.parent.mark_as_unknown()

    def inner_solve(self, rhs: int) -> int:
        if self.name == "humn":
            return rhs
        elif self.left.is_unknown:
            return self.left.inner_solve(
                INV_OP_LEFT[self.value](self.right.eval(), rhs)
            )
        elif self.right.is_unknown:
            return self.right.inner_solve(
                INV_OP_RIGHT[self.value](self.left.eval(), rhs)
            )
        raise Exception("wtf is going on")

    def solve(self) -> int:
        left = self.left.find()
        right = self.right.find()
        if left is not None:
            left.mark_as_unknown()
            unknown = self.left
            known = self.right.eval()
        else:
            right.mark_as_unknown()
            unknown = self.right
            known = self.left.eval()
        return unknown.inner_solve(known)


class MonkeyTree:
    def __init__(self, monkeys: list[tuple[str, Operation]]):
        self.monkeys = {name: operation for name, operation in monkeys}

    def eval(self, monkey="root") -> int:
        match self.monkeys[monkey]:
            case (left, op, right):
                return OP[op](self.eval(left), self.eval(right))
            case value:
                return value

    def tree(self, monkey="root", parent: Optional[Monkey] = None) -> Monkey:
        match self.monkeys[monkey]:
            case (left, op, right):
                node = Monkey(monkey, op, parent)
                node.left = self.tree(left, node)
                node.right = self.tree(right, node)
                return node
            case value:
                return Monkey(monkey, value, parent)


the_input_ffs = [
    (name, int(operation) if not " " in operation else tuple(operation.split()))
    for [name, operation] in (line.split(": ") for line in sys.stdin)
]

tree = MonkeyTree(the_input_ffs).tree()
print("Part 1:", tree.eval())
print("Part 2:", tree.solve())
