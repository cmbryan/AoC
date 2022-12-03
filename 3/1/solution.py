# for each input line,
# divide in half
# find the common element
# translate to priority
# sum

def rucksacks(inpt):
    return inpt[:len(inpt)//2], inpt[len(inpt)//2:]
assert rucksacks('abcd') == ('ab', 'cd')

def get_common(a, b):
    return list(set(a) & set(b))[0]
assert get_common('abc', 'cde') == 'c'

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
    with open(path, 'r') as fh:
        for line in fh.readlines():
            a, b = rucksacks(line.strip())
            common = get_common(a, b)
            sum += priority(common)
    return sum

assert solution('sample.txt') == 157
print('Ok')

print(solution('input.txt'))
