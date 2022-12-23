# X,Y coords from bottom-left
from copy import deepcopy


shapes = (
    ([0, 0], [1, 0], [2, 0], [3, 0]),
    ([0, 1], [1, 0], [1, 1], [1, 2], [2, 1]),
    ([0, 0], [1, 0], [2, 0], [2, 1], [2, 2]),
    ([0, 0], [0, 1], [0, 2], [0, 3]),
    ([0, 0], [0, 1], [1, 0], [1, 1]),
)

max_x = 7  # fixed


def solution(path):
    with open(path) as fh:
        pattern = fh.readline().strip()
    pattern_ix = 0

    shape_ix = 0  # The next rock to fall
    column_points_fixed = set()
    max_y = -1  # will update as rocks come to rest
    rock = None  # currently falling

    num_settled = 0
    while num_settled < 2022:
        # new rock
        rock = deepcopy(shapes[shape_ix])
        for pix in range(len(rock)):
            rock[pix][0] += 2
            rock[pix][1] += max_y + 4
        shape_ix = (shape_ix + 1) % len(shapes)

        # keep falling until settled
        settled = False
        while True:
            ch = pattern[pattern_ix]
            pattern_ix = (pattern_ix + 1) % len(pattern)

            # horizontal action
            offset = 1 if ch == ">" else -1
            for p in rock:
                if (
                    p[0] + offset < 0
                    or p[0] + offset >= max_x
                    or (p[0] + offset, p[1]) in column_points_fixed
                ):
                    break  # no action
            else:
                for p in rock:
                    p[0] += offset

            # vertical action
            for p in rock:
                if p[1] - 1 < 0 or (p[0], p[1] - 1) in column_points_fixed:
                    settled = True
                    break
            else:
                for p in rock:
                    p[1] -= 1

            if settled:
                # solidify
                for p in rock:
                    column_points_fixed.add(tuple(p))
                    max_y = max(max_y, p[1])
                num_settled += 1
                # start a new rock
                break

    return max_y + 1


test_answer = solution("../sample.txt")
assert test_answer == 3068, test_answer
print("Ok")
print(solution("../input.txt"))
