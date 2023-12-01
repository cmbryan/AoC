def translate(ch):
    if ch in ['A', 'X']:
        return 1
    elif ch in ['B', 'Y']:
        return 2
    elif ch in ['C', 'Z']:
        return 3
    else:
        assert False

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
            opponent, mine = translate(a), translate(b)
            score += judge(opponent, mine) + mine
    return score

assert solution('sample.txt') == 15
print(solution('input.txt'))
