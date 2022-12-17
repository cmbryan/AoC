from copy import copy


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
    return grid, start, end


def solution(filepath):
    grid, start, end = parse_input(filepath)
    paths = [[start]]
    while True:
        updated_paths = []
        print(f"{len(paths)} paths of length {len(paths[0])}")
        for path in paths:
            cur = path[-1]
            # branches
            proposed = [
                (cur[0], cur[1] - 1),  # up
                (cur[0], cur[1] + 1),  # down
                (cur[0] - 1, cur[1]),  # left
                (cur[0] + 1, cur[1]),  # right
            ]
            for prop in proposed:
                if (
                    prop[0] >= 0
                    and prop[0] < len(grid)
                    and prop[1] >= 0
                    and prop[1] < len(grid[0])
                    and prop not in path
                    and grid[prop[0]][prop[1]] - grid[cur[0]][cur[1]] <= 1
                ):
                    # optimization: check whether this position exists in any path
                    for p2 in paths:
                        try:
                            p2ix = p2.index(prop)
                            if p2ix < len(path):
                                break  # We're already covering this path in a better way
                        except ValueError:
                            continue  # not in list
                    else:
                        updated_paths.append(copy(path) + [prop])

        # Check for winner
        for path in updated_paths:
            if path[-1] == end:
                return len(path) - 1  # Not counting the start
        paths = updated_paths


_t = solution("sample.txt")
assert _t == 31, _t
print("Ok")
print(f"Part 1 => {solution('input.txt')}")
