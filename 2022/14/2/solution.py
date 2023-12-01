def parse_input(path):
    rocks = set()
    max_y = 0
    with open(path) as fh:
        for line in fh.readlines():
            coords = line.strip().split(" -> ")
            for idx in range(1, len(coords)):
                coord = list(map(int, coords[idx].split(",")))
                prev_coord = list(map(int, coords[idx - 1].split(",")))
                mn, mx = sorted([prev_coord[0], coord[0]])
                mx_y = max(prev_coord[1], coord[1])
                max_y = mx_y if max_y == 0 else max(max_y, mx_y)
                for x in range(mn, mx + 1):
                    rocks.add((x, coord[1]))
                mn, mx = sorted([prev_coord[1], coord[1]])
                for y in range(mn, mx + 1):
                    rocks.add((coord[0], y))

    return rocks, max_y


def solution(path):
    rocks, max_y = parse_input(path)
    flr = max_y + 2

    units_of_sand = 0
    while True:
        sand = (500, 0)
        while True:
            proposed = [
                (sand[0], sand[1] + 1),
                (sand[0] - 1, sand[1] + 1),
                (sand[0] + 1, sand[1] + 1),
            ]
            for prop in proposed:
                if prop not in rocks and prop[1] < flr:
                    sand = prop
                    break
            else:
                rocks.add(sand)
                units_of_sand += 1
                if sand == (500, 0):
                    return units_of_sand
                break


test_part2 = solution("../sample.txt")
assert test_part2 == 93, test_part2
answer_part2 = solution("../input.txt")
print(f"Part 2 => {answer_part2}")
