import re
from typing import List, Set


class Item:
    def __init__(self, worry_level):
        self.worry_level: int = worry_level
        self.factors: Set[int] = set()

    def __repr__(self):
        return f"{self.worry_level} - {self.factors}"


class Monkey:
    def __init__(self):
        self.items: List[Item] = []
        self.num_inspected = 0
        self.operator: str = None
        self.operand: str = None
        self.test_div_by: int = None
        self.throw_true: int = None
        self.throw_false: int = None

    def __gt__(self, other):
        return self.num_inspected > other.num_inspected

    def __lt__(self, other):
        return self.num_inspected < other.num_inspected

    def __ge__(self, other):
        return self.num_inspected >= other.num_inspected

    def __le__(self, other):
        return self.num_inspected <= other.num_inspected

    def __repr__(self):
        return f"Monkey with {len(self.items)}, inspected {self.num_inspected} items"


def parse_input(path):
    monkeys = []
    with open(path) as fh:
        items_re = re.compile(r"\W+Starting items: (.*)")
        op_re = re.compile(r"\W+Operation: new = old (.) (.*)")
        test_re = re.compile(r"\W+Test: divisible by (\d+)")
        throw_true_re = re.compile(r"\W+If true: throw to monkey (\d+)")
        throw_false_re = re.compile(r"\W+If false: throw to monkey (\d+)")
        for line_num, line in enumerate(fh.readlines()):
            mode = line_num % 7
            if mode == 0:
                monkey = Monkey()
                monkeys.append(monkey)
            elif mode == 1:
                monkey.items = list(
                    Item(int(item)) for item in items_re.match(line)[1].split(", ")
                )
            elif mode == 2:
                monkey.operator = op_re.match(line)[1]
                monkey.operand = op_re.match(line)[2]
            elif mode == 3:
                monkey.test_div_by = int(test_re.match(line)[1])
            elif mode == 4:
                monkey.throw_true = int(throw_true_re.match(line)[1])
            elif mode == 5:
                monkey.throw_false = int(throw_false_re.match(line)[1])
    return monkeys


def solution(path, n_rounds):
    monkeys: List[Monkey] = parse_input(path)
    for _ in range(n_rounds):
        pass
        for monkey in monkeys:
            for item in monkey.items:
                if monkey.operator == "*":
                    item.factors.add(monkey.operand)
                    item.worry_level = 0
                else:
                    assert monkey.operator == "+"
                    item.worry_level += int(monkey.operand)

                if (
                    monkey.test_div_by in item.factors
                    and item.worry_level % monkey.test_div_by == 0
                ):
                    monkeys[monkey.throw_true].items.append(item)
                else:
                    monkeys[monkey.throw_false].items.append(item)
            monkey.num_inspected += len(monkey.items)
            monkey.items = []
        pass

    monkeys = sorted(monkeys)
    for monkey in monkeys:
        print(monkey)
    return monkeys[-1].num_inspected * monkeys[-2].num_inspected


_t = solution("../sample.txt", 10000)
assert _t == 2713310158, _t
print("Ok")
print(f"Part 2 => {solution('../input.txt')}")
