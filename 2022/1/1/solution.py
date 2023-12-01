#!/usr/bin/env python3

with open('input.py', 'r') as fh:
    top = 0
    cur = 0
    for line in fh.readlines():
        if line.strip():
            cur += int(line.strip())
            top = max(top, cur)
        else:
            cur = 0

print(top)
