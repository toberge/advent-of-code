import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class coord:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return coord(self.x - other.x, self.y - other.y)

    def magnitude(self):
        """Manhattan length"""
        return abs(self.x) + abs(self.y)

    def distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)


@dataclass
class Sensor:
    location: coord
    nearest_beacon: coord

    @property
    def radius(self):
        return self.location.distance(self.nearest_beacon)

    def beacon_not_present(self, position: coord):
        return self.location.distance(position) <= self.location.distance(
            self.nearest_beacon
        )

    def range_on_line(self, y: int) -> Optional[tuple[int, int]]:
        remainder = self.radius - self.location.distance(coord(self.location.x, y))
        # remainder = (
        #     self.location.y + self.radius - y
        #     if self.location.y >= y
        #     else self.location.y - self.radius - y
        # )
        # print(remainder, self.location, self.radius)
        if remainder >= 0:
            return (self.location.x - remainder, self.location.x + remainder)
        return None

    def beacon_on_line(self, y) -> bool:
        return self.nearest_beacon.y == y


sensors: list[Sensor] = []

for line in sys.stdin:
    [sensor_part, beacon_part] = line.rstrip().split(":")
    sensor_tokens = sensor_part.split()[-2:]
    sensor = coord(int(sensor_tokens[0][2:-1]), int(sensor_tokens[1][2:]))
    beacon_tokens = beacon_part.split()[-2:]
    beacon = coord(int(beacon_tokens[0][2:-1]), int(beacon_tokens[1][2:]))
    sensors.append(Sensor(sensor, beacon))

y = 10
y = 2000000

ranges = []

coverage = 0
beacons_on_line = set()


def merge_overlaps(index, xmin, xmax):
    for i, (xmin2, xmax2) in enumerate(ranges):
        if index == i:
            continue
        if xmin2 <= xmin <= xmax2 < xmax:
            # Right side
            ranges[i] = (xmin2, xmax)
            break
        elif xmin < xmin2 <= xmax <= xmax2:
            # Left side
            ranges[i] = (xmin, xmax2)
            break
        elif xmin < xmin2 <= xmax2 < xmax:
            # This new range contains the old!
            ranges[i] = sensor_range
            break
        elif xmin2 <= xmin <= xmax <= xmax2:
            break
    else:
        return
    del ranges[index]


for sensor in sensors:
    sensor_range = sensor.range_on_line(y)
    print(sensor.location, sensor.radius, sensor.nearest_beacon, sep=" \t", end="\t")
    if sensor_range is not None:
        (xmin, xmax) = sensor_range

        # Hypothetical overlap
        area = abs(xmax - xmin) + 1

        # find overlap with existing ranges
        for i, (xmin2, xmax2) in enumerate(ranges):
            if xmin2 <= xmin <= xmax2 < xmax:
                # Right side
                # area = abs(xmax - xmax2)
                ranges[i] = (xmin2, xmax)
                merge_overlaps(i, xmin2, xmax)
                break
            elif xmin < xmin2 <= xmax <= xmax2:
                # Left side
                # area = abs(xmin2 - xmin)
                ranges[i] = (xmin, xmax2)
                merge_overlaps(i, xmin, xmax2)
                break
            elif xmin < xmin2 <= xmax2 < xmax:
                # This new range contains the old!
                # area = abs(xmax - xmax2) + abs(xmin2 - xmin)
                ranges[i] = sensor_range
                merge_overlaps(i, xmin, xmax)
                break
            elif xmin2 <= xmin <= xmax <= xmax2:
                area = 0
                break
        else:
            ranges.append(sensor_range)

        # coverage += area - sensor.beacon_on_line(y)

        if sensor.beacon_on_line(y):
            beacons_on_line.add(sensor.nearest_beacon)

        print(xmin, xmax, sensor.beacon_on_line(y), area - sensor.beacon_on_line(y))
        # ...or maybe we don't need to
        print(ranges)
    else:
        print("no coverage")

for (xmin, xmax) in ranges:
    coverage += xmax - xmin + 1

coverage -= len(beacons_on_line)

print("Part 1:", coverage)
