def parse_input(path):
    rocks = set()
    min_x, max_x = 0, 0
    with open(path) as fh:
        for line in fh.readlines():
            coords = line.strip().split(" -> ")
            for idx in range(1, len(coords)):
                coord = list(map(int, coords[idx].split(",")))
                prev_coord = list(map(int, coords[idx - 1].split(",")))
                mn, mx = sorted([prev_coord[0], coord[0]])
                min_x, max_x = mn if min_x == 0 else min(min_x, mn), max(max_x, mx)
                for x in range(mn, mx+1):
                    rocks.add((x, coord[1]))
                mn, mx = sorted([prev_coord[1], coord[1]])
                for y in range(mn, mx+1):
                    rocks.add((coord[0], y))
    return rocks, min_x, max_x


def solution(path):
    rocks, min_x, max_x = parse_input(path)

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
                if prop not in rocks:
                    sand = prop
                    if prop[0] <= min_x or prop[1] >= max_x:
                        return units_of_sand
                    break
            else:
                rocks.add(sand)
                units_of_sand += 1
                break


test_part1 = solution("../sample.txt")
assert test_part1 == 24, test_part1
answer_part1 = solution("../input.txt")
print(f"Part 1 => {answer_part1}")
