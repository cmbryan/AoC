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

                for _ in range(amt):
                    saved = stack_base_fr.next
                    stack_base_fr.next = stack_base_fr.next.next
                    saved.next = stack_base_to.next
                    stack_base_to.next = saved

    # print('-')
    # for ix in range(len(stacks)):
    #     print(f'{ix+1}: {stacks[ix]}')

    for ix in range(len(stacks)):
        result += stacks[ix].next.data
    return result

assert solution('sample.txt') == 'CMZ'

print(solution('input.txt'))
