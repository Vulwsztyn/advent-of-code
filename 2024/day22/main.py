from pathlib import Path
import re


def mix(x, y):
    return x ^ y


def prune(x):
    return x % 16777216


def next_num(x):
    y = x * 64
    x = mix(x, y)
    x = prune(x)
    y = x // 32
    x = mix(x, y)
    x = prune(x)
    y = x * 2048
    x = mix(x, y)
    x = prune(x)
    return x


file = Path(__file__).parent / "data.txt"
text = [int(x) for x in file.read_text().strip().splitlines()]
print(text)
result = 0
for num in text:
    for i in range(2000):
        # print(num,i)
        num = next_num(num)
    result += num
print(result)
