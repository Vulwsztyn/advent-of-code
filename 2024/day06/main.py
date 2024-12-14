from pathlib import Path


def find_guard(text):
    for i, line in enumerate(text):
        for j, v in enumerate(line):
            if v == "^":
                return (i, j)


def next_direction(dir):
    if dir == (-1, 0):
        return (0, 1)
    elif dir == (0, 1):
        return (1, 0)
    elif dir == (1, 0):
        return (0, -1)
    else:
        return (-1, 0)


def apply_direction(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


def run_algorithm(starting_pos, additional_obstacle, is_legal_position, is_obstacle):
    dir = (-1, 0)
    next_pos = apply_direction(starting_pos, dir)
    visited_with_dir = set([(starting_pos, dir)])
    pos = starting_pos
    is_loop = False
    while is_legal_position(next_pos):
        pos = next_pos
        if (pos, dir) in visited_with_dir:
            is_loop = True
            break
        visited_with_dir.add((pos, dir))
        next_pos = apply_direction(pos, dir)
        # print(pos, next_pos)
        if not is_legal_position(next_pos):
            break
        if is_obstacle(next_pos) or next_pos == additional_obstacle:
            next_pos = pos
            dir = next_direction(dir)
    visited = {x[0] for x in visited_with_dir}
    return is_loop, visited


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().split("\n")
starting_pos = find_guard(text)
is_legal_position = (
    lambda x: x[0] >= 0 and x[0] < len(text) and x[1] >= 0 and x[1] < len(text[0])
)
is_obstacle = lambda x: text[x[0]][x[1]] == "#"

_, visited = run_algorithm(starting_pos, None, is_legal_position, is_obstacle)

print(len(visited))

for i in range(10):
    for j in range(10):
        x = "X" if (i, j) in visited else "."
        if is_obstacle((i, j)):
            x = "#"
        print(x, end="")
    print()

result = 0
for pos in visited:
    if starting_pos == pos:
        continue
    is_loop, _ = run_algorithm(starting_pos, pos, is_legal_position, is_obstacle)
    if is_loop:
        result += 1

print(result)
