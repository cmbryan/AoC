from collections import defaultdict
from dataclasses import dataclass, field
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


CACHE: Dict[Tuple[str, str, int], int] = {}


def best_path(
    nodes: Dict[str, Node],
    cur_nodes: List[str],
    opened: DefaultDict[str, bool] = defaultdict(lambda: False),
    time_remaining=26,
):
    global CACHE
    if time_remaining <= 0:
        return 0
    time_remaining -= 1
    cur_nodes = sorted(cur_nodes)

    # current nodes, time remaining, opened valves
    cache_key = (
        tuple(cur_nodes),
        time_remaining,
        "".join(list(filter(lambda n: opened[n], opened.keys()))),
    )
    if cache_key in CACHE:
        return CACHE[cache_key]

    max_score = 0

    # Option 1: don't open, don't open
    for n1 in nodes[cur_nodes[0]].tunnels:
        for n2 in nodes[cur_nodes[1]].tunnels:
            score = best_path(nodes, [n1, n2], opened, time_remaining)
            max_score = max(max_score, score)

    # Option 2: open, don't open
    if not opened[cur_nodes[0]] and nodes[cur_nodes[0]].rate > 0:
        opened[cur_nodes[0]] = True
        for node in nodes[cur_nodes[1]].tunnels:
            score = best_path(nodes, [cur_nodes[0], node], opened, time_remaining)
            max_score = max(
                max_score, score + nodes[cur_nodes[0]].rate * time_remaining
            )
        opened[cur_nodes[0]] = False

    # Option 3: don't open, open
    if not opened[cur_nodes[1]] and nodes[cur_nodes[1]].rate > 0:
        opened[cur_nodes[1]] = True
        for node in nodes[cur_nodes[0]].tunnels:
            score = best_path(nodes, [node, cur_nodes[1]], opened, time_remaining)
            max_score = max(
                max_score, score + nodes[cur_nodes[1]].rate * time_remaining
            )
        opened[cur_nodes[1]] = False

    # Option 4: open, open
    if (not opened[cur_nodes[0]] and nodes[cur_nodes[0]].rate > 0) and (
        not opened[cur_nodes[1]] and nodes[cur_nodes[1]].rate > 0
    ):
        opened[cur_nodes[0]] = True
        opened[cur_nodes[1]] = True
        score = best_path(nodes, cur_nodes, opened, time_remaining)
        max_score = max(
            max_score,
            score
            + nodes[cur_nodes[0]].rate * time_remaining
            + nodes[cur_nodes[1]].rate * time_remaining
        )
        opened[cur_nodes[0]] = False
        opened[cur_nodes[1]] = False

    CACHE[cache_key] = max_score
    return max_score


nodes = parse_input("../sample.txt")
CACHE = {}
# test_answer = best_path(nodes, ["AA", "AA"], time_remaining=4)
test_answer = best_path(nodes, ["AA", "AA"])
assert test_answer == 1707, test_answer
# print("Ok")
#
# nodes = parse_input("../input.txt")
# CACHE = {}
# part2 = best_path(nodes, ["AA", "AA"])
# print(f"Part 2 => {part2}")
