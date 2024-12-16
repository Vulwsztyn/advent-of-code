from pathlib import Path
import re
from itertools import chain


def parse_input(text):
    raindeer = (0, 0)
    end = (0, 0)
    walls = set()
    vertical_wall = len(text[0]) - 1
    for i, line in enumerate(text):
        if i == 0:
            continue
        if all(x == "#" for x in line):
            break
        for j, char in enumerate(line):
            if j == 0 or j == len(line) - 1:
                continue
            if char == "#":
                walls.add((i, j))
            elif char == "S":
                raindeer = (i, j)
            elif char == "E":
                end = (i, j)
    horizontal_wall = i

    def is_wall(pos):
        i, j = pos
        if i == 0 or j == 0 or i == horizontal_wall or j == vertical_wall:
            return True
        return (i, j) in walls

    return raindeer, end, is_wall, horizontal_wall, vertical_wall


def print_map(r, e, is_wall, h, w):
    for i in range(h + 1):
        for j in range(w + 1):
            msg = "."
            if is_wall((i, j)):
                msg = "#"
            elif (i, j) == r:
                msg = "S"
            elif (i, j) == e:
                msg = "E"
            print(msg, end="")
        print()
    print()


file = Path(__file__).parent / "test.txt"
text = file.read_text().strip().splitlines()
raindeer, end, is_wall, h, w = parse_input(text)
print_map(raindeer, end, is_wall, h, w)

achieved = {}
stack = [(raindeer, 0, (0, 1))]
cheapest_end = 1e9
while stack:
    pos, v, current_dir = stack.pop()
    print(pos, v, current_dir)
    if (pos, current_dir) in achieved and achieved[(pos, current_dir)] <= v:
        continue
    if v > cheapest_end:
        continue
    achieved[(pos, current_dir)] = v
    if pos == end:
        if v < cheapest_end:
            cheapest_end = v
        continue
    for dir in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        dir = tuple(dir)
        if dir == tuple(-x for x in current_dir):
            continue
        new_pos = tuple(pos[i] + dir[i] for i in range(2))
        if is_wall(new_pos):
            continue
        stack.append((new_pos, v + 1 + (0 if dir == current_dir else 1000), dir))
    print(stack)
print(cheapest_end)
