"""
Day 23: Crab Cups

Part one: ez.
Part two: Had to reverse __init__ and add lookup table for nodes

Runs for way too long before spitting out the correct answer.
As far as I can see, each part of the move() method
should be an O(3) operation, at most.
However, that is if I entirely forget about the decrementing of the label.
That one *does* have a "higher" complexity, but it should *ultimately* be O(1).
"""

from itertools import chain, tee


class Node:
    """Node in this particular list"""

    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right

    def __iter__(self):  # for testing?
        node = self
        while node is not None:
            yield node
            node = node.right

    def __repr__(self):
        return str(self.label)


class circulist:
    """Circular doubly-linked list"""

    def __init__(self, labels, minlabel=1, maxlabel=None):
        # Cache of nodes by label
        if maxlabel is None:
            temp, labels = tee(labels)
            maxlabel = max(temp)  # don't exhaust iterator!
        self.lookup: [Node] = [None] * maxlabel

        # Create root node
        rootlabel = next(labels)
        tail = Node(rootlabel)
        self.root = tail
        self.lookup[rootlabel - 1] = tail

        # Add nodes to the tail
        for label in labels:
            tail = Node(label, left=tail)  # Connect back
            tail.left.right = tail  # Connect forward
            self.lookup[label - 1] = tail

        # Connect tail back to root
        tail.right = self.root
        self.root.left = tail

        # Game-specific details
        self.current = self.root
        self.minlabel = minlabel
        self.maxlabel = maxlabel

    def __iter__(self):
        # Should this be the default behaviour?
        node = self.root
        yield node.label
        node = node.right
        while node != self.root:
            yield node.label
            node = node.right

    def nodes(self):
        """Iterable of nodes"""
        node = self.root
        yield node
        node = node.right
        while node != self.root:
            yield node
            node = node.right

    def at(self, index):
        """Get element by index"""
        for i, label in enumerate(self):
            if i == index:
                return label
        raise KeyError(f"Index {index} out of bounds")

    def __getitem__(self, label):
        """Find node by label - O(1)"""
        return self.lookup[label - 1]

    def find(self, label):
        """Find node by label - O(n), deprecated"""
        try:
            return next(node for node in self.nodes() if node.label == label)
        except StopIteration as err:
            raise KeyError(f"No such label: {label}") from err

    def take_chain(self, start: Node, length=3) -> Node:
        """Take a range of nodes out of the list, return root of chain - O(length)"""
        end = start
        for _ in range(length - 1):
            end = end.right
        # connect the list
        start.left.right = end.right
        end.right.left = start.left
        after = end.right  # remember this one!
        # disconnect the slice
        start.left = None
        end.right = None
        # replace root if any of these were the root!
        if self.root in start:
            self.root = after
        return start

    def insert_chain(self, insertion_point, root):
        """Insert a chain of nodes *after* the given node - O(length)"""
        after = insertion_point.right
        insertion_point.right = root
        root.left = insertion_point
        *_, tail = iter(root)
        tail.right = after
        after.left = tail

    def swap(self, after, start, length=3):
        """Place elements in start+length after an element"""
        pass

    def wrap_around(self, label):
        """Wrap label around if it's less than minimum"""
        if label - 1 < self.minlabel:
            return self.maxlabel
        return label - 1

    def move(self):
        """Have the crab make a move"""
        cups = self.take_chain(self.current.right)  # O(3)
        labels = set(cup.label for cup in cups)  # O(3)
        label = self.wrap_around(self.current.label)
        while label in labels:  # O(6) I think
            label = self.wrap_around(label)  # O(1)
        # print(
        #     list(cups),
        #     label,
        #     list(self),
        # )
        destination = self[label]  # O(1)
        self.insert_chain(destination, cups)  # O(3)
        self.current = self.current.right  # O(1)


def test():
    lst = circulist(chain([3, 8, 9, 1, 2, 5, 4, 6, 7], range(10, 21)))
    print(list(lst))
    node = lst.take_chain(lst.root.left)
    print(list(node))
    print(list(lst))
    lst.insert_chain(lst.root.left, node)
    print(list(lst))


def part_one(labels):
    """Just 10 cups - this is fine"""
    cups = circulist(iter(labels), maxlabel=9)
    for _ in range(100):
        cups.move()
    # rebase to 1
    cups.root = cups[1]
    print("".join(str(i) for i in list(cups)[1:]))


def part_two(labels):
    """Upping the numbers"""
    # 1 million != 10 million!
    cups = circulist(chain(labels, range(10, 1000_001)), maxlabel=1000_000)
    for _ in range(10_000_000):
        cups.move()
    print(cups[1].right.label * cups[1].right.right.label)


def main():
    """Day 23, yo"""
    labels = [int(i) for i in input()]
    part_one(labels)
    part_two(labels)


if __name__ == "__main__":
    main()
