from copy import copy
import numpy as np


def parse_input(path):
    grid = []
    with open(path) as fh:
        for line in fh.readlines():
            grid.append([ch for ch in line.strip()])
    for row_ix, row in enumerate(grid):
        for col_ix, col in enumerate(row):
            if col == "S":
                start = (row_ix, col_ix)
                grid[row_ix][col_ix] = "a"
            elif col == "E":
                end = (row_ix, col_ix)
                grid[row_ix][col_ix] = "z"
            grid[row_ix][col_ix] = ord(grid[row_ix][col_ix])
    return np.array(grid), start, end


def solution(filepath):
    grid, start, end = parse_input(filepath)
    lengths = np.full(grid.shape, fill_value=-1)
    lengths[*end] = 0
    cursors = [end]
    while cursors:
        # pop
        cur = cursors[-1]
        cursors = cursors[:-1]

        # branches
        proposed = [
            (cur[0] + 1, cur[1]),  # right
            (cur[0], cur[1] - 1),  # up
            (cur[0], cur[1] + 1),  # down
            (cur[0] - 1, cur[1]),  # left
        ]
        for prop in proposed:
            prop_len = lengths[*cur] + 1
            if (
                prop[0] >= 0
                and prop[0] < len(grid)
                and prop[1] >= 0
                and prop[1] < len(grid[0])
                and (lengths[*prop] > prop_len or lengths[*prop] == -1)
                and grid[*prop] - grid[*cur] >= -1
            ):
                lengths[*prop] = prop_len
                cursors.append(prop)

    part1 = lengths[start]
    part2 = min(
        map(
            lambda idx_and_len: idx_and_len[1],
            filter(
                lambda idx_and_len: (grid.reshape(-1)[idx_and_len[0]] == 97 and idx_and_len[1] > 0),
                enumerate(lengths.reshape(-1)),
            ),
        )
    )
    return part1, part2


_t1, _t2 = solution("sample.txt")
assert _t1 == 31, _t1
assert _t2 == 29, _t2
print("Ok")

_a1, _a2 = solution("input.txt")
assert _a1 == 383, _a1

print(f"Part 1 => {_a1}")
print(f"Part 2 => {_a2}")
