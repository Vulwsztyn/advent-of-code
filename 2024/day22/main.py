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


def find_sequence(changes, sequence):
    for i, v in enumerate(changes):
        if v != sequence[0]:
            continue
        if i + len(sequence) > len(changes):
            break
        for j in range(1, len(sequence)):
            if changes[i + j] != sequence[j]:
                break
        else:
            return i + j
    return None


file = Path(__file__).parent / "test.txt"
text = [int(x) for x in file.read_text().strip().splitlines()]
print(text)
result = 0
prices = []
changes = []
for i, num in enumerate(text):
    # for i,num in enumerate([123]):
    prices.append([])
    changes.append([])
    for j in range(2000):
        # print(num,i)
        m = next_num(num)
        price = m % 10
        prices[i].append(price)
        change = price - (num % 10)
        changes[i].append(change)
        num = m
    result += num
print(result)
result = 0
for i, change_seq in enumerate(changes):
    index = find_sequence(change_seq, [-2, 1, -1, 3])
    if index is None:
        continue
    to_add = prices[i][index]
    print(i, text[i], to_add)
    result += to_add
print(result)
