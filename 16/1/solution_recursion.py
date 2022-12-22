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
    cur_node: str,
    opened: DefaultDict[str, bool] = defaultdict(lambda: False),
    time_remaining=30,
):
    global CACHE
    if time_remaining <= 0:
        return 0
    time_remaining -= 1  # time remaining after the *next* action

    # current node, time remaining, opened valves
    cache_key = (
        cur_node,
        time_remaining,
        "".join(list(filter(lambda n: opened[n], opened.keys()))),
    )
    if cache_key in CACHE:
        return CACHE[cache_key]

    max_score = 0

    # Option A: move without opening
    for node in nodes[cur_node].tunnels:
        score = best_path(nodes, node, opened, time_remaining)
        max_score = max(max_score, score)

    # Option B: open before moving
    if not opened[cur_node] and nodes[cur_node].rate > 0:
        opened[cur_node] = True
        score = best_path(nodes, cur_node, opened, time_remaining)
        max_score = max(max_score, score + nodes[cur_node].rate * time_remaining)
        opened[cur_node] = False

    CACHE[cache_key] = max_score
    return max_score


nodes = parse_input("../sample.txt")
CACHE = {}
test_answer = best_path(nodes, "AA", time_remaining=30)
assert test_answer == 1651, test_answer
print("Ok")

nodes = parse_input("../input.txt")
CACHE = {}
part1 = best_path(nodes, "AA", time_remaining=30)
print(f"Part 1 => {part1}")
assert part1 == 1820, part1
