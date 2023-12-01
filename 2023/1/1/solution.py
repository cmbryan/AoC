import re

first_digit_re = re.compile(f'(\d)')
last_digit_re = re.compile(f'.*(\d)')
assert first_digit_re.search('1abc2').group(1) == '1'
assert last_digit_re.search('1abc2').group(1) == '2'
assert first_digit_re.search('treb7uchet').group(1) == '7'
assert last_digit_re.search('treb7uchet').group(1) == '7'


def calc_value(s: str) -> int:
    return int(
        first_digit_re.search(s).group(1) \
        + last_digit_re.search(s).group(1)
    )


with open('input.txt') as fh:
    total = 0
    for line in fh.readlines():
        total += calc_value(line)
    print(total)
