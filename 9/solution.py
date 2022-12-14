from copy import copy
import enum


class Direction(enum.Enum):
    L = "L"
    U = "U"
    R = "R"
    D = "D"


class Knot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction):
        if direction == Direction.L:
            self.x -= 1
        elif direction == Direction.U:
            self.y += 1
        elif direction == Direction.R:
            self.x += 1
        elif direction == Direction.D:
            self.y -= 1

    def follow(self, other):
        if abs(other.x - self.x) > 1:
            self.x += (other.x - self.x) // 2
            self.y += other.y - self.y
        elif abs(other.y - self.y) > 1:
            self.y += (other.y - self.y) // 2
            self.x += other.x - self.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x},{self.y})"


def parse_input(path):
    with open(path) as fh:
        for line in fh.readlines():
            direction, times = line.split()
            for _ in range(int(times)):
                yield (Direction[direction])


def solution(path):
    head = Knot()
    tail = Knot()
    tail_visited = set()
    for head_command in parse_input(path):
        head.move(head_command)
        tail.follow(head)
        tail_visited.add(copy(tail))
    return len(tail_visited)


_t = solution('sample.txt')
assert _t == 13, _t
print("Ok")
print(f"Part 1 => {solution('input.txt')}")
