import sys
from dataclasses import dataclass, field
from operator import itemgetter


# ore, clay, obsidian, geode
Cost = tuple[int, int, int, int]

robot_names = {
    0: "ore",
    1: "clay",
    2: "obsidian",
    3: "geode",
}


@dataclass
class Blueprint:
    recipes: tuple[Cost, Cost, Cost, Cost] = (
        (4, 0, 0, 0),
        (2, 0, 0, 0),
        (3, 14, 0, 0),
        (2, 0, 7, 0),
    )

    def can_build(self, recipe: Cost, inventory: Cost) -> bool:
        return all(stored >= cost for cost, stored in zip(recipe, inventory))

    def build(self, recipe: Cost, inventory: Cost) -> Cost:
        return tuple(stored - cost for cost, stored in zip(recipe, inventory))

    def mine(self, robots: Cost, inventory: Cost) -> Cost:
        return tuple(stored + mined for mined, stored in zip(robots, inventory))

    def evaluate(self) -> int:
        robots = (1, 0, 0, 0)
        resources = (0, 0, 0, 0)
        for i in range(24):
            print(f"Minute {i}")
            for robot, recipe in reversed(list(enumerate(self.recipes))):
                print(robot, recipe)
                if self.can_build(recipe, resources):
                    print(f"built a {robot_names[robot]} collecting robot")
                    resources = self.build(recipe, resources)
                    robots = tuple(
                        count + 1 if i == robot else count
                        for i, count in enumerate(robots)
                    )
            resources = self.mine(robots, resources)
            print(f"Got {resources}")
        return resources[3]


print(Blueprint().evaluate())
