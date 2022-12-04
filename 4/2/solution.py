import re
from typing import List

def parse_input(line: str) -> List[List[int]]:
    splt = list(map(lambda x: int(x), re.split(r'[,-]', line)))
    assert len(splt) == 4
    return [splt[:2], splt[2:]]
assert parse_input("11-22,33-44") == [[11, 22], [33, 44]]

def solution(path: str) -> int:
    sum = 0
    with open(path, 'r') as fh:
        for line in fh.readlines():
            rngs = parse_input(line)
            if (rngs[0][0] >= rngs[1][0] and rngs[0][0] <= rngs[1][1]) \
            or (rngs[0][1] >= rngs[1][0] and rngs[0][1] <= rngs[1][1]) \
            or (rngs[0][0] <= rngs[1][0] and rngs[0][1] >= rngs[1][1]):
                sum += 1
    return sum

_t = solution('../1/sample.txt')
assert _t == 4, _t

print(solution('../1/input.txt'))
