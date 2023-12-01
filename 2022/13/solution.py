from functools import cmp_to_key


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
            return -1 if len(a) <= len(b) else 1
        return cmp(a, [b])
    elif isinstance(b, list):
        return cmp([a], b)
    assert a!=b
    return -1 if a < b else 1


def solution(path):
    part1 = 0
    all_packets = []
    for idx, inpt in enumerate(parse_input(path)):
        all_packets.append(inpt[0])
        all_packets.append(inpt[1])
        if cmp(*inpt) == -1:
            part1 += idx + 1

    all_packets = sorted(all_packets, key=cmp_to_key(cmp))

    save_idx1 = 0
    save_idx2 = 0
    for idx, inpt in enumerate(all_packets):
        if not save_idx1 and cmp([[2]], inpt) == -1:
            save_idx1 = idx + 1
        if not save_idx2 and cmp([[6]], inpt) == -1:
            save_idx2 = idx + 1 + 1
            break

    return part1, save_idx1 * save_idx2


test_p1, test_p2 = solution("sample.txt")
assert test_p1 == 13, test_p1
assert test_p2 == 140, test_p2
print("Ok")

part1, part2 = solution("input.txt")
print(f"Part 1 => {part1}")
assert part1 == 5390, part1
print(f"Part 2 => {part2}")
