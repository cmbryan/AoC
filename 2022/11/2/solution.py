import re
from typing import List, Set, Tuple


class Item:
    def __init__(self, initial_level):
        self.initial_level = initial_level
        # Keep a separate modulo sum for each monkey
        self.worry_level_mods: Tuple[int] = None

    def __repr__(self):
        return repr(self.worry_level_mods)


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
    monkeys: List[Monkey] = []
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

    # Initialize a separate modulo sum for each monkey
    for monkey in monkeys:
        for item in monkey.items:
            item.worry_level_mods = tuple(item.initial_level % _m.test_div_by for _m in monkeys)
    return monkeys


def solution(path, n_rounds):
    monkeys: List[Monkey] = parse_input(path)
    for _ in range(n_rounds):
        for monkey_ix, monkey in enumerate(monkeys):
            for item in monkey.items:
                # Update the modulo sums for each monkey for each item
                if monkey.operator == "*":
                    if monkey.operand == "old":
                        item.worry_level_mods = \
                           [(worry_level*worry_level) % monkeys[m_ix].test_div_by \
                            for m_ix, worry_level in enumerate(item.worry_level_mods)]
                    else:
                        item.worry_level_mods = \
                           [(worry_level*int(monkey.operand)) % monkeys[m_ix].test_div_by \
                            for m_ix, worry_level in enumerate(item.worry_level_mods)]
                else:
                    assert monkey.operator == "+"
                    item.worry_level_mods = \
                       [(worry_level + int(monkey.operand)) % monkeys[m_ix].test_div_by \
                        for m_ix, worry_level in enumerate(item.worry_level_mods)]

                if item.worry_level_mods[monkey_ix] == 0:
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


n_rounds=10000
_t = solution("../sample.txt", n_rounds)
assert _t == 2713310158, _t
print("Ok")
print(f"Part 2 => {solution('../input.txt', n_rounds)}")
