# for each input line,
# divide in half
# find the common element
# translate to priority
# sum

def get_common(*args):
    common = set(args[0])
    for arg in args[1:]:
        common = common & set(arg)
    assert len(common) == 1
    return list(common)[0]
assert get_common('abc', 'cab', 'xxc') == 'c'

def priority(ch):
    if ch.islower():
        return(ord(ch)-97+1)
    else:
        return(ord(ch)-65+27)
assert priority('a') == 1
assert priority('z') == 26
assert priority('A') == 27
assert priority('Z') == 52

def solution(path):
    sum = 0
    trio = []
    with open(path, 'r') as fh:
        for line in fh.readlines():
            trio.append(line.strip())
            if len(trio) < 3:
                continue
            common = get_common(*trio)
            assert(common)
            sum += priority(common)
            trio = []
    return sum

assert solution('../1/sample.txt') == 70
print('Ok')

print(solution('../1/input.txt'))
