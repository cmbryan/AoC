import numpy as np


def solution(path):
    trees = []
    with open(path) as fh:
        for line in fh.readlines():
            trees.append([int(t) for t in line.strip()])
    trees = np.array(trees)

    visible_trees = set()

    def collect_visible(trees, is_rotated):
        for r_ix, r in enumerate(trees):
            # Left -> Right
            max = -1
            for t_ix, t in enumerate(r[:-1]):
                if t > max:
                    # we can see this tree
                    max = t
                    coords = (r_ix, t_ix) if not is_rotated else (t_ix, r_ix)
                    visible_trees.add(coords)

            # Right -> Left
            max = -1
            for t_ix, t in reversed(list(enumerate(r))):
                if t > max:
                    # we can see this tree
                    max = t
                    coords = (r_ix, t_ix) if not is_rotated else (t_ix, r_ix)
                    visible_trees.add(coords)

    collect_visible(trees, is_rotated=False)
    collect_visible(trees.T, is_rotated=True)

    return len(visible_trees)


_t = solution("sample.txt")
assert _t == 21, _t
print("Ok")
print(f"Part 1: {solution('input.txt')}")
