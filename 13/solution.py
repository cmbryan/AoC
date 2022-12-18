def parse_input(path):
    with open(path) as fh:
        buf = None
        for line in fh.readlines():
            if line.strip():
                if buf is not None:
                    yield (buf, eval(line))
                    buf = None
                else:
                    buf = eval(line)


def cmp(a, b):
    if isinstance(a, list):
        if isinstance(b, list):
            overlap = min(len(a), len(b))
            if a[:overlap] != b[:overlap]:
                for idx in range(overlap):
                    if a[idx] != b[idx]:
                        return cmp(a[idx], b[idx])
            return len(a) < len(b)
        return cmp(a, [b])
    elif isinstance(b, list):
        return cmp([a], b)
    return a < b


def solution(path):
    result = 0
    for idx, inpt in enumerate(parse_input(path)):
        if cmp(*inpt):
            result += idx + 1
    return result


test_p1 = solution("sample.txt")
assert test_p1 == 13, test_p1
print("Ok")

part1 = solution("input.txt")
print(f"Part 1 => {part1}")
