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
    num_covered = 0
    for x in range(*x_bounds):
        if (x, tgt_y) in beacons:
            continue
        is_covered = False
        for s in sensors:
            if abs(s.coord[0] - x) + abs(s.coord[1] - tgt_y) <= s.covers:
                is_covered = True
                break
        if is_covered:
            num_covered += 1
    return num_covered


test_answer = solution("sample.txt", 10)
assert test_answer == 26, test_answer
print("Ok")

print(f"Part 1 => {solution('input.txt', 2000000)}")
