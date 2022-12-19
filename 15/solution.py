import re
from typing import List, Tuple


class Sensor:
    def __init__(self, s_coord, b_coord):
        self.coord: Tuple[int, int] = tuple(s_coord)
        self.covers: int = abs(s_coord[0] - b_coord[0]) + abs(s_coord[1] - b_coord[1])

    def __repr__(self):
        return f"{self.coord} covers {self.covers}"


def parse_input(path) -> Tuple[List[Sensor], Tuple[int, int]]:
    sensors = []
    beacons = set()
    x_bounds = [None, None]
    parser = re.compile(
        r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    with open(path) as fh:
        for line in fh.readlines():
            coords = list(map(int, parser.match(line).groups()))
            sensor = Sensor(coords[:2], coords[2:])
            beacons.add(tuple(coords[2:]))
            x_bounds[0] = (
                sensor.coord[0] - sensor.covers
                if x_bounds[0] is None
                else min(x_bounds[0], sensor.coord[0] - sensor.covers)
            )
            x_bounds[1] = (
                sensor.coord[0] + sensor.covers
                if x_bounds[1] is None
                else max(x_bounds[1], sensor.coord[0] + sensor.covers)
            )
            sensors.append(sensor)
    return sensors, beacons, tuple(x_bounds)


def solution(path, tgt_y):
    sensors, beacons, x_bounds = parse_input(path)

    ranges = set()
    for s in sensors:
        covers = s.covers - abs(s.coord[1] - tgt_y)
        if covers < 0:
            continue
        new_range = (s.coord[0] - covers, s.coord[0] + covers + 1)
        ranges.add(new_range)

    while True:
        ranges = sorted(list(ranges))
        idx1, idx2 = 0, 1
        simple_ranges = set()
        updated = False
        while idx1 < len(ranges) - 1:
            idx2 = idx1 + 1
            while idx2 < len(ranges) and ranges[idx1][1] >= ranges[idx2][0]:
                idx2 += 1
                updated = True
            new_range = (
                min(ranges[idx1][0], ranges[idx2 - 1][0]),
                max(ranges[idx1][1], ranges[idx2 - 1][1]),
            )
            simple_ranges.add(new_range)
            idx1 = idx2 + 1
        if updated:
            ranges = simple_ranges
        else:
            break

    num_covered = sum(map(lambda r: r[1] - r[0], ranges))
    num_covered -= len(list(filter(lambda b: b[1] == tgt_y, beacons)))
    return num_covered


test_answer = solution("sample.txt", 10)
assert test_answer == 26, test_answer
print("Ok")

print(f"Part 1 => {solution('input.txt', 2000000)}")
