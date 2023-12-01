from collections import defaultdict
import re
from typing import Dict


class Node:
    def __init__(self, data) -> None:
        self.data: str = data
        self.next = None

    def append(self, node) -> None:
        if self.next:
            self.next.append(node)
        else:
            self.next = node

    def get(self, ix):
        return self if ix == 0 else self.next.get(ix-1)

    def __repr__(self):
        return f"[{self.data}]->{self.next}"

def solution(path):
    stacks = defaultdict(lambda: Node(''))
    result = ''
    with open(path) as fh:
        mode = 0
        for line in fh.readlines():
            if mode == 0:
                if not line.strip():
                    mode = 1
                    continue
                for ix in range(0, len(line), 4):
                    ch = line[ix+1]
                    if ch.isnumeric():
                        break  # stack labels
                    # print('.'+ch)
                    if ch != ' ':
                        stacks[ix//4].append(Node(ch))

            elif mode == 1:
                # print('-')
                # for ix in range(len(stacks)):
                #     print(f'{ix+1}: {stacks[ix]}')

                amt, fr, to = re.match(r'move (\d+) from (\d+) to (\d+)', line).groups()
                amt, fr, to = int(amt), int(fr), int(to)

                stack_base_fr = stacks[fr-1]
                stack_base_to = stacks[to-1]

                saved_st = stack_base_fr.next
                saved_end = stack_base_fr.get(amt)
                stack_base_fr.next = saved_end.next
                saved_end.next = stack_base_to.next
                stack_base_to.next = saved_st

    # print('-')
    # for ix in range(len(stacks)):
    #     print(f'{ix+1}: {stacks[ix]}')

    for ix in range(len(stacks)):
        result += stacks[ix].next.data
    return result

assert solution('../1/sample.txt') == 'MCD'

print(solution('../1/input.txt'))
