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
            self.y += max(min(other.y - self.y, 1), -1)
        elif abs(other.y - self.y) > 1:
            self.y += (other.y - self.y) // 2
            self.x += max(min(other.x - self.x, 1), -1)

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


def solution_part1(path):
    head = Knot()
    tail = Knot()
    tail_visited = set()
    for head_command in parse_input(path):
        head.move(head_command)
        tail.follow(head)
        tail_visited.add(copy(tail))
    return len(tail_visited)


def solution_part2(path, debug_view=False):
    knots = [Knot() for _ in range(10)]
    rng_x = [0, 0]
    rng_y = [0, 0]
    tail_visited = set()
    for cmd_ix, head_command in enumerate(parse_input(path)):
        knots[0].move(head_command)
        for ix, knot in list(enumerate(knots))[1:]:
            knot.follow(knots[ix - 1])
        tail_visited.add(copy(knots[-1]))

        if debug_view:
            # Debug view
            rng_x[0] = min(rng_x[0], knots[0].x)
            rng_y[0] = min(rng_y[0], knots[0].y)
            rng_x[1] = max(rng_x[1], knots[0].x)
            rng_y[1] = max(rng_y[1], knots[0].y)
            print("=" * 10 + str(cmd_ix + 1))
            for y in reversed(range(rng_y[0], rng_y[1] + 1)):
                for x in range(rng_x[0], rng_x[1] + 1):
                    ch = "."
                    for k_ix, knot in enumerate(knots):
                        if knot.x == x and knot.y == y:
                            ch = k_ix
                    print(ch, end="")
                print("")
            pass

    return len(tail_visited)


_t = solution_part1("sample.txt")
assert _t == 13, _t
print("Ok")
print(f"Part 1 => {solution_part1('input.txt')}")

_t = solution_part2("sample2.txt")
assert _t == 36, _t
print("Ok")
print(f"Part 2 => {solution_part2('input.txt', True)}")
