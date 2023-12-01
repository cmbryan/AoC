def translate(ch):
    if ch in ['A', 'X']:
        return 1
    elif ch in ['B', 'Y']:
        return 2
    elif ch in ['C', 'Z']:
        return 3
    else:
        assert False

def calculate(opp, outcome):
    return (opp+outcome-2-1) % 3 + 1

def judge(opp, mine):
    if opp == mine:
        return 3
    elif opp == 1 and mine == 2:
        return 6
    elif opp == 2 and mine == 3:
        return 6
    elif opp == 3 and mine == 1:
        return 6
    else:
        return 0

def solution(path):
    score = 0
    with open(path, 'r') as fh:
        for line in fh.readlines():
            a, b = line.split()
            opponent, outcome = translate(a), translate(b)
            mine = calculate(opponent, outcome)
            score += judge(opponent, mine) + mine
    return score

assert calculate(1, 1) == 3, calculate(1, 1)
assert calculate(1, 2) == 1, calculate(1, 2)
assert calculate(1, 3) == 2, calculate(1, 3)
assert calculate(3, 1) == 2, calculate(3, 1)
assert calculate(3, 2) == 3, calculate(3, 2)
assert calculate(3, 3) == 1, calculate(3, 3)

assert solution('sample.txt') == 12

print("Ok")
print(solution('input.txt'))
