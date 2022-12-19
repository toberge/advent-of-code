import sys
from dataclasses import dataclass, field
from operator import itemgetter


# ore, clay, obsidian, geode
Cost = tuple[int, int, int, int]


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
        # minutes[minute][orebots][claybots][obsidianbots][geodebots]
        # minutes[minute+1] = all possibilities? that could be expensive
        minutes: list[dict[Cost, Cost]] = [{(1, 0, 0, 0): (0, 0, 0, 0)}]
        for minute in range(24):
            minutes.append(dict())
            for robots, resources in minutes[minute].items():
                minutes[minute + 1][robots] = self.mine(robots, resources)
                for robot, recipe in enumerate(self.recipes):
                    print("can build", robot, "?")
                    if self.can_build(recipe, resources):
                        print("yes")
                        with_robot = tuple(
                            count + 1 if i == robot else count
                            for i, count in enumerate(robots)
                        )
                        # Find max of this and other solution with same robot set
                        proposal = self.mine(robots, self.build(recipe, resources))
                        other = minutes[minute + 1].get(with_robot)
                        if other is not None:
                            minutes[minute + 1][with_robot] = max(proposal, other)
                        else:
                            minutes[minute + 1][with_robot] = proposal
        return max(inventory[3] for inventory in minutes[-1].values())


print(Blueprint().evaluate())
