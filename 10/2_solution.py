def parse_input(path):
    with open(path) as fh:
        idx = 0
        for line in fh.readlines():
            yield idx, 0
            if "noop" not in line:
                idx += 1
                yield idx, int(line.split()[1])
            idx += 1

def solution(path):
    reg = 1
    result = 0
    for inst in parse_input(path):
        cycle, val = inst
        sprite_vals = range(reg-1, reg+2)
        x_pos = cycle % 40
        print("#" if x_pos in sprite_vals else ".", end="")
        if x_pos == 39:
            print("")
        reg += val

print("Testing")
solution("sample.txt")
print(f"Part 2 =>")
solution('input.txt')
