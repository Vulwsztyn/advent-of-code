from pathlib import Path


def find_guard(text):
    for i, line in enumerate(text):
        for j, v in enumerate(line):
            if v == "^":
                return (i, j)


def next_direction(dir):
    if dir == [-1, 0]:
        return [0, 1]
    elif dir == [0, 1]:
        return [1, 0]
    elif dir == [1, 0]:
        return [0, -1]
    else:
        return [-1, 0]


def apply_direction(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


def is_obstacle(pos, text):
    return text[pos[0]][pos[1]] == "#"


file = Path("test.txt")
text = file.read_text().split("\n")
pos = find_guard(text)
dir = [-1, 0]
is_legal_position = (
    lambda x: x[0] >= 0 and x[0] < len(text) and x[1] >= 0 and x[1] < len(text[0])
)
next_pos = apply_direction(pos, dir)
visited = set([pos])
while is_legal_position(next_pos):
    pos = next_pos
    visited.add(pos)
    next_pos = apply_direction(pos, dir)
    print(pos, next_pos)
    if not is_legal_position(next_pos):
        break
    if is_obstacle(next_pos, text):
        next_pos = pos
        dir = next_direction(dir)
print(len(visited))

for i in range(10):
    for j in range(10):
        x = "X" if (i, j) in visited else "."
        if is_obstacle((i, j), text):
            x = "#"
        print(x, end="")
    print()
