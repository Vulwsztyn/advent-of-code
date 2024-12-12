from pathlib import Path
from collections import defaultdict


def neighbours(i, j, text):
    result = []
    for ii in range(-1, 2):
        if i + ii < 0:
            continue
        if i + ii >= len(text):
            continue
        for jj in range(-1, 2):
            if j + jj < 0:
                continue
            if j + jj >= len(text[0]):
                continue
            if ii == 0 and jj == 0:
                continue
            result.append((i + ii, j + jj))
    return result


def positions(text, value="X"):
    result = []
    for i, line in enumerate(text):
        for j, char in enumerate(line):
            if char == value:
                result.append((i, j))
    return result


def finder(pos, index, word, text):
    if index == len(word):
        return 1
    print(pos, word[index])
    n = neighbours(*pos, text)
    n_ok = [x for x in n if text[x[0]][x[1]] == word[index]]
    print(n_ok)
    sum = 0
    for i in n_ok:
        sum += finder(i, index + 1, word, text)
    return sum


def apply_direction(pos, direction):
    return [pos[0] + direction[0], pos[1] + direction[1]]


def finder_with_direction(pos, index, direction, to_find, text, is_legal_position):
    if text[pos[0]][pos[1]] != to_find[index]:
        return False
    if index == len(to_find) - 1:
        return True
    nex_pos = apply_direction(pos, direction)
    if not is_legal_position(nex_pos):
        return False
    return finder_with_direction(
        nex_pos, index + 1, direction, to_find, text, is_legal_position
    )


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
x_pos = positions(text)
directions = [[x, y] for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0]
is_legal_position = (
    lambda x: x[0] >= 0 and x[0] < len(text) and x[1] >= 0 and x[1] < len(text[0])
)

print(x_pos)
result = 0
for x in x_pos:
    add = 0
    for dir in directions:
        found = finder_with_direction(x, 0, dir, "XMAS", text, is_legal_position)
        add += 1 if found else 0
    result += add
print(result)

a_pos = [
    x
    for x in positions(text, "A")
    if 0 < x[0] < len(text) - 1 and 0 < x[1] < len(text[0]) - 1
]
print(a_pos)
result = 0
for pos in a_pos:
    if text[pos[0] - 1][pos[1] - 1] == text[pos[0] + 1][pos[1] + 1]:
        continue
    values = defaultdict(int)
    for dir in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
        values[text[pos[0] + dir[0]][pos[1] + dir[1]]] += 1
    if values["M"] == 2 and values["S"] == 2:
        result += 1
print(result)
