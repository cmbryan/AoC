import enum


class Dir(enum.Enum):
    L = "L"
    U = "U"
    R = "R"
    D = "D"

def parse_input(path):
    result = []
    with open(path) as fh:
        for line in fh.readlines():
            direction, times = line.split()
            for _ in range(int(times)):
                result.append(Dir[direction])
    return result

result = parse_input("sample.txt")
print(result)

