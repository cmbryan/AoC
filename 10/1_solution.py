def parse_input(path):
    with open(path) as fh:
        idx = 0
        for line in fh.readlines():
            idx += 1
            yield idx, 0
            if "noop" not in line:
                idx += 1
                yield idx, int(line.split()[1])

def solution(path):
    reg = 1
    result = 0
    for inst in parse_input(path):
        cycle, val = inst
        if (inst[0] - 20) % 40 == 0:
            score = reg * cycle
            result += score
        reg += val
        if cycle > 220:
            break
    return result

_t = solution("sample.txt")
assert _t == 13140, _t
print("Ok")

print(f"Part 1 => {solution('input.txt')}")
