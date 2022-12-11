# State machine!


import os


class Elt:
    """Directory or file"""

    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.parent_dir = None
        self.child_dirs = []

    def add_or_get_child(self, child_name, size=0):
        for child in self.child_dirs:
            if child.name == child_name:
                assert child.size == size
                return child
        child = Elt(child_name, size=size)
        child.parent_dir = self
        self.child_dirs.append(child)
        self.__propagate(child.size)
        return child

    def get_total_under(self, max_size):
        collection = set()
        for child in self.child_dirs:
            collection = collection.union(child.get_total_under(max_size))
        if self.child_dirs and self.size <= max_size:
            collection.add(self.size)
        return collection


    def __propagate(self, size):
        self.size += size
        if self.parent_dir:
            self.parent_dir.__propagate(size)

    def __repr__(self) -> str:
        if self.parent_dir is None:
            return self.name
        return os.path.join(repr(self.parent_dir), self.name)


def solution(path, max_size):
    with open(path) as fh:
        cur_dir = None
        for line in fh.readlines():
            # print(f"1=> {cur_dir}")
            # print(f"2=> {line.strip()}")
            # print("")
            words = [word.strip() for word in line.split(" ")]
            if words[0] == "$":
                mode = words[1]
                if mode == "cd":
                    if words[2] == "/":
                        if cur_dir is None:
                            cur_dir = Elt("/")
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
    return sum(cur_dir.get_total_under(max_size))


max_size = 100000

_t = solution("sample.txt", max_size)
assert _t == 95437, _t
print("Ok")
print(solution("input.txt", max_size))
