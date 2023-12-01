import numpy as np


class SimpleStack:
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)

    def pop(self):
        if self._data:
            self._data, val = self._data[:-1], self._data[-1]
            return val
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def __repr__(self):
        return repr(self._data)


def calc_score(trees, scores):
    for r_ix, r in enumerate(trees):
            row_stack = SimpleStack()
            ix_stack = SimpleStack()
            row_stack.push(trees[r_ix][0])
            ix_stack.push(0)
            for t_ix, t in list(enumerate(r))[1:]:
                while row_stack.peek() is not None and t >= row_stack.peek():
                    row_stack.pop()
                    s_ix = ix_stack.pop()
                    scores[r_ix, s_ix] *= t_ix - s_ix
                row_stack.push(t)
                ix_stack.push(t_ix)
            while (s_ix:=ix_stack.pop()) is not None:
                scores[r_ix, s_ix] *= len(r) - s_ix - 1


def solution(path):
    trees = []
    with open(path) as fh:
        for line in fh.readlines():
            trees.append([int(t) for t in line.strip()])
    trees = np.array(trees)
    scores = np.full(trees.shape, 1)

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

    calc_score(trees, scores)  # left->right
    calc_score(np.fliplr(trees), np.fliplr(scores))  # right->left
    calc_score(trees.T, scores.T)  # top->bottom
    calc_score(np.fliplr(trees.T), np.fliplr(scores.T))  # bottom->top

    return len(visible_trees), np.amax(scores)

_t = solution("sample.txt")
assert _t == (21, 8), _t
print("Ok")
print(f"Part 1: {solution('input.txt')}")
