from collections import defaultdict
import enum
import sys
import numpy as np


class Mirrors:
    def __init__(self, landscape: list[str]) -> None:
        self.similar_lines = defaultdict(list)
        self.height = len(landscape)
        self.width = len(landscape[0])

        # m = np.array([[c == "#" for c in l] for l in landscape])
        seen = defaultdict(list)
        for y, l in enumerate(landscape):
            if l in seen:
                py = seen[l]
                for yy in py:
                    self.similar_lines[yy].append(y)
                self.similar_lines[y] = py[:]
                py.append(y)
            else:
                seen[l] = [y]
        print(seen, self.similar_lines)
        print(max(len(s) for s in seen.values()))

    def rows_before(self) -> int:
        for i in range(1, self.height):
            similar = self.similar_lines[i]
            for j in similar:
                if abs(j - i) < 2:
                    if j > i:
                        flag = False
                        for (k, l) in zip(range(i, -1, -1), range(j, self.height)):



if __name__ == "__main__":
    lines = [l.split("\n") for l in sys.stdin.read().split("\n\n")]
    print(lines)
    for p in lines:
        Mirrors(p)
