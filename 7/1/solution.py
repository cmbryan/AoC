# State machine!


import itertools
import os

g_max_size: int = 100000


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

    return sum(map(lambda elt: elt.size, filter(lambda elt: elt.is_dir() and elt.size <= g_max_size, cur_dir)))


_t = solution("sample.txt", g_max_size)
assert _t == 95437, _t
print("Ok")
_t = solution("input.txt", g_max_size)
assert _t == 1886043, _t
print(_t)
