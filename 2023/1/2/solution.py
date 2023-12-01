import re

first_digit_re = re.compile(f'(\d)')
last_digit_re = re.compile(f'.*(\d)')
assert first_digit_re.search('1abc2').group(1) == '1'
assert last_digit_re.search('1abc2').group(1) == '2'
assert first_digit_re.search('treb7uchet').group(1) == '7'
assert last_digit_re.search('treb7uchet').group(1) == '7'

replacement_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def translate(s: str) -> str:
    res = ''
    for ix in range(len(s)):
        for k, v in replacement_dict.items():
            if s[ix:].startswith(k):
                res += v
                ix += len(k)
                break
        else:
            res += s[ix]
            ix += 1
    return res

# assert translate('two1nine') == '219'
# assert translate('eightwothree') == '8wo3'
# assert translate('abcone2threexyz') == 'abc123xyz'
# assert translate('xtwone3four') == 'x2ne34'
# assert translate('4nineeightseven2') == '49872'
# assert translate('zoneight234') == 'z1ight234'
# assert translate('7pqrstsixteen') == '7pqrst6teen'


def calc_value(s: str) -> int:
    return int(
        first_digit_re.search(s).group(1) \
        + last_digit_re.search(s).group(1)
    )


assert calc_value(translate('two1nine')) == 29
assert calc_value(translate('eightwothree')) == 83
assert calc_value(translate('abcone2threexyz')) == 13
assert calc_value(translate('xtwone3four')) == 24
assert calc_value(translate('4nineeightseven2')) == 42
assert calc_value(translate('zoneight234')) == 14
assert calc_value(translate('7pqrstsixteen')) == 76


with open('../1/input.txt') as fh:
    total = 0
    for line in fh.readlines():
        total += calc_value(translate(line))
    print(total)
