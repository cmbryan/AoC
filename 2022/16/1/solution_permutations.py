from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from itertools import permutations
import numpy as np
import re
from typing import DefaultDict, Dict, List, Tuple


@dataclass
class Node:
    rate: int
    tunnels: List[str]


def parse_input(path):
    parser_re = re.compile(
        r"^Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)"
    )
    nodes: Dict[str, Node] = {}
    with open(path) as fh:
        for line in fh.readlines():
            data = parser_re.match(line.strip()).groups()
            nodes[data[0]] = Node(int(data[1]), data[2].split(", "))
    return nodes



def calculate_cost(tbl, nodes, node_keys, frm, to, running_total=0):
    running_total += 1
    for n in nodes[to].tunnels:
        cur = tbl[node_keys.index(frm)][node_keys.index(n)]
        if running_total < cur or cur == -1:
            tbl[node_keys.index(frm)][node_keys.index(n)] = running_total
            calculate_cost(tbl, nodes, node_keys, frm, n, running_total)


def solution(path):
    nodes: Dict[str, Node] = parse_input(path)
    all_node_keys = list(nodes.keys())
    size = len(nodes)

    cost_table = np.full((size, size), fill_value=-1)
    for frm in all_node_keys:
        calculate_cost(cost_table, nodes, all_node_keys, frm, frm)

    # Now we can compute the score for every permution of opening sequences
    # But this is way to slow-- what other kind of heuristic could we use?
    high_score = 0
    node_keys = list(filter(lambda n: nodes[n].rate>0, all_node_keys))
    for proposal in permutations(node_keys):
        score = 0
        time_remaining = 30
        cur = "AA"
        for node in proposal:
            time_remaining -= cost_table[all_node_keys.index(cur)][all_node_keys.index(node)]
            time_remaining -= 1
            if time_remaining == 0:
                continue
            score += nodes[node].rate*time_remaining
            cur = node
        high_score = max(high_score, score)

    return high_score

test_part1 = solution("../sample.txt")
assert test_part1 == 1651, test_part1
print("Ok")

part1 = solution("../input.txt")
print(f"Part 1 => {part1}")
assert part1 == 1820, part1
