# State machine!


import itertools
import os


class FileElt:
    """Directory or file"""

    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.parent_dir = None
        self.children = []

    def add_or_get_child(self, child_name, size=0):
        for child in self.children:
            if child.name == child_name:
                assert child.size == size
                return child
        child = FileElt(child_name, size=size)
        child.parent_dir = self
        self.children.append(child)
        return child

    def is_dir(self):
        return bool(self.children)

    def __iter__(self):
        if self.children:
            self.size = 0
            for child in self.children:
                for gc in child:
                    yield gc
                self.size += child.size
        yield self

    def __repr__(self) -> str:
        name = (
            self.name
            if self.parent_dir is None
            else os.path.join(repr(self.parent_dir), self.name)
        )
        return f"{name} ({self.size})" if self.size else name


def solution(path, max_size):
    with open(path) as fh:
        cur_dir = None
        for line in fh.readlines():
            words = [word.strip() for word in line.split(" ")]
            if words[0] == "$":
                mode = words[1]
                if mode == "cd":
                    if words[2] == "/":
                        if cur_dir is None:
                            cur_dir = FileElt("/")
                        else:
                            assert False  # doesn't happen in the input
                    elif words[2] == "..":
                        cur_dir = cur_dir.parent_dir
                        assert cur_dir
                    else:
                        cur_dir = cur_dir.add_or_get_child(words[2])
                    mode = None  # defensive
                continue

            elif mode == "ls":
                if words[0] == "dir":
                    pass  # don't need this information
                else:
                    cur_dir.add_or_get_child(words[1], size=int(words[0]))
            else:
                assert False  # defensive

    # get to /
    while cur_dir.parent_dir:
        cur_dir = cur_dir.parent_dir

    solution_sum = sum(map(lambda elt: elt.size, filter(lambda elt: elt.is_dir() and elt.size <= max_size, cur_dir)))

    tot_disk_size = 70000000
    tgt_min_unused = 30000000
    current_free = tot_disk_size -cur_dir.size
    free_at_least = tgt_min_unused - current_free
    print(free_at_least)
    # solution_delete_this = min(map(lambda elt: elt.size, filter(lambda elt: elt.is_dir() and elt.size >= free_at_least, cur_dir)))
    solution_delete_this = min(map(lambda elt: elt.size, filter(lambda elt: elt.is_dir() and elt.size >= free_at_least, cur_dir)))

    return solution_sum, solution_delete_this


max_size: int = 100000

_t = solution("sample.txt", max_size)
assert _t[0] == 95437, _t[0]
assert _t[1] == 24933642, _t[1]
print("Ok")

_t = solution("input.txt", max_size)
assert _t[0] == 1886043, _t[0]
print(f"Part 1: {_t[0]}, part 2: {_t[1]}")
