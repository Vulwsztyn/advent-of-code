from pathlib import Path
import re
from collections import defaultdict


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


def generate_sequences(changes):
    sequences = set()
    for change_list in changes:
        for i in range(len(change_list) - 3):
            sequences.add(tuple(change_list[i : i + 4]))
    return sequences


def generate_values(changes, prices):
    values = defaultdict(int)
    for list_i, change_list in enumerate(changes):
        sequences = set()
        for i in range(len(change_list) - 3):
            key = tuple(change_list[i : i + 4])
            if key in sequences:
                continue
            sequences.add(key)
            values[key] += prices[list_i][i + 3]
    return values


file = Path(__file__).parent / "data.txt"
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
sequences = generate_sequences(changes)
print(len(sequences))
values = generate_values(changes, prices)
print(values)
print(max(values.values()))
