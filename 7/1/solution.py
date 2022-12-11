# State machine!


import os


class Elt:
    """Directory or file"""

    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.parent_dir = None
        self.child_dirs = []

    def add_child(self, child):
        child.parent_dir = self
        self.child_dirs.append(child)
        self.__propagate(child.size)

    def get_total_under(self, max_size):
        result = 0 if self.size > max_size else self.size
        for child in self.child_dirs:
            result += child.get_total_under(max_size)
        return result

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
            print(f"2=> {line.strip()}")
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
                        new_dir = Elt(words[2])
                        cur_dir.add_child(new_dir)
                        cur_dir = new_dir
                    mode = None  # defensive
                continue

            elif mode == "ls":
                if words[0] == "dir":
                    pass  # don't need this information
                else:
                    new_file = Elt(words[1], size=int(words[0]))
                    cur_dir.add_child(new_file)  # don't need the filename
            else:
                assert False  # defensive

    # get to /
    while cur_dir.parent_dir:
        cur_dir = cur_dir.parent_dir
    breakpoint()
    return cur_dir.get_total_under(max_size)


max_size = 100000

_t = solution("sample.txt", max_size)
assert _t == 95437, _t
print("Ok")
print(solution("input.txt"), max_size)
