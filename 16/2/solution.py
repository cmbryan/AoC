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
HITS = MISSES = 0


def best_path(
    nodes: Dict[str, Node],
    cur_nodes: List[str],
    opened: List[str] = [],
    time_remaining=26
):
    if time_remaining <= 0:
        return 0
    global CACHE#, HITS, MISSES

    time_remaining -= 1
    cur_nodes = sorted(cur_nodes)

    # current nodes, time remaining, opened valves
    cache_key = (
        tuple(cur_nodes),
        time_remaining,
        tuple(opened),
    )
    # if MISSES%1000000==0:
    #     print(f"{HITS}/{MISSES}")
    if cache_key in CACHE:
        # HITS += 1
        return CACHE[cache_key]
    # MISSES += 1

    max_score = 0

    # Option 1: move, move
    for n1 in nodes[cur_nodes[0]].tunnels:
        for n2 in nodes[cur_nodes[1]].tunnels:
            score = best_path(nodes, [n1, n2], opened, time_remaining)
            max_score = max(max_score, score)

    # Option 2: open, move
    if not cur_nodes[0] in opened and nodes[cur_nodes[0]].rate > 0:
        for node in nodes[cur_nodes[1]].tunnels:
            score = best_path(
                nodes,
                [cur_nodes[0], node],
                sorted(opened + [cur_nodes[0]]),
                time_remaining,
            )
            max_score = max(
                max_score, score + nodes[cur_nodes[0]].rate * time_remaining
            )

    # Option 3: move, open
    if not cur_nodes[1] in opened and nodes[cur_nodes[1]].rate > 0:
        for node in nodes[cur_nodes[0]].tunnels:
            score = best_path(
                nodes,
                [node, cur_nodes[1]],
                sorted(opened + [cur_nodes[1]]),
                time_remaining,
            )
            max_score = max(
                max_score, score + nodes[cur_nodes[1]].rate * time_remaining
            )

    # Option 4: open, open
    if (not cur_nodes[0] in opened and nodes[cur_nodes[0]].rate > 0) and (
        not cur_nodes[1] in opened and nodes[cur_nodes[1]].rate > 0
    ):
        both_opened = sorted(opened + cur_nodes)
        score = best_path(nodes, cur_nodes, both_opened, time_remaining)
        score += nodes[cur_nodes[0]].rate * time_remaining
        if cur_nodes[0] != cur_nodes[1]:
            score += nodes[cur_nodes[1]].rate * time_remaining
        max_score = max(max_score, score)

    CACHE[cache_key] = max_score
    return max_score


nodes = parse_input("../sample.txt")
CACHE = {}
test_answer = best_path(nodes, ["AA", "AA"])
assert test_answer == 1707, test_answer
print("Ok")

nodes = parse_input("../input.txt")
CACHE = {}
part2 = best_path(nodes, ["AA", "AA"])
print(f"Part 2 => {part2}")
