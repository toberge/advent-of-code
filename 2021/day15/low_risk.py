import heapq
import sys
from typing import List, Tuple
from dataclasses import dataclass
from itertools import product


@dataclass
class Tile:
    x: int
    y: int
    risk: int
    distance: int = 1e10
    visited: bool = False
    predecessor = None
    neighbours = None

    def __gt__(self, tile):
        return self.distance > tile.distance

    def __lt__(self, tile):
        return self.distance < tile.distance

    def __eq__(self, tile):
        return self.x == tile.x and self.y == tile.y

    def __hash__(self):
        return self.x + 10000 * self.y


def neighbours(tile: Tile, cave: List[List[Tile]]) -> List[Tile]:
    return [
        cave[y][x]
        for x, y in [
            (tile.x - 1, tile.y),
            (tile.x + 1, tile.y),
            (tile.x, tile.y - 1),
            (tile.x, tile.y + 1),
        ]
        if 0 <= y < len(cave) and 0 <= x < len(cave[0])
    ]


def dijkstra(cave: List[List[Tile]]):
    cave[0][0].distance = 0
    heap = [cave[0][0]]
    goal = cave[-1][-1]
    seen = set()

    while len(heap) > 0:
        tile = heapq.heappop(heap)
        tile.visited = True

        if tile == goal:
            return tile.distance

        update = False
        requeue = False
        for neighbour in tile.neighbours:
            if not neighbour.visited:
                neighbour.predecessor = tile
                # Update distance if smaller
                new_distance = tile.distance + neighbour.risk
                if new_distance < neighbour.distance:
                    neighbour.distance = new_distance
                    update = True
                # Ensure you don't push the same tile again and again
                if neighbour not in seen:
                    heapq.heappush(heap, neighbour)
                    seen.add(neighbour)
                else:
                    requeue = True
        if update and requeue:
            heapq.heapify(heap)  # expensive but necessary

    return -1


def make_cave(lines: List[str]) -> List[List[Tile]]:
    lines = [line.strip() for line in lines]
    return [
        [Tile(x, y, int(lines[y][x])) for x in range(len(lines[0]))]
        for y in range(len(lines))
    ]


def add_neighbours(cave):
    for row in cave:
        for tile in row:
            tile.neighbours = neighbours(tile, cave)


def main():
    cave = make_cave(sys.stdin.readlines())
    add_neighbours(cave)
    lowest_risk = dijkstra(cave)
    print(lowest_risk)


if __name__ == "__main__":
    main()
