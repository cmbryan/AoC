#!/usr/bin/env python3

def solution(inpt):
    with open(inpt, 'r') as fh:
        top = [0, 0, 0]
        cur = 0
        for line in fh.readlines():
            if line.strip():
                cur += int(line.strip())
            else:
                top = sorted(top + [cur], reverse=True)[0:3]
                cur = 0
    # final line
    top = sorted(top + [cur], reverse=True)[0:3]
    cur = 0

    return top

assert([24000, 11000, 10000] == solution('ex.txt'))

print(sum(solution('../1/input.txt')))
