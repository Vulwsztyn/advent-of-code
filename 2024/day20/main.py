from pathlib import Path
import re
from itertools import chain
from collections import defaultdict


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
        if i <= 0 or j <= 0 or i >= horizontal_wall or j >= vertical_wall:
            return True
        return (i, j) in walls

    return raindeer, end, is_wall, horizontal_wall, vertical_wall


def print_colored(color, text, end=""):
    print(f"\033[{30+color}m{text}\033[00m", end=end)


def print_map(r, e, is_wall, h, w, distances=None):
    for i in range(h + 1):
        for j in range(w + 1):
            msg = "."
            color = 0
            if is_wall((i, j)):
                msg = "#"
            elif (i, j) == r:
                msg = "S"
            elif (i, j) == e:
                msg = "E"
            elif distances is not None:
                v = distances[i][j]
                msg = str(v).zfill(2)
                color = v % 7 + 1
            if len(msg) < 2:
                msg = 2 * msg
            print_colored(color, msg, end="")
        print()
    print()


def empty_distances(h, w):
    result = []
    for i in range(w):
        result.append([])
        for _ in range(h):
            result[i].append(None)
    return result


def get_distances(end, is_wall, h, w):
    distances = empty_distances(h, w)
    stack = [(end, 0)]
    while stack:
        pos, dist = stack.pop()
        if is_wall(pos):
            continue
        if distances[pos[0]][pos[1]] is not None:
            continue
        distances[pos[0]][pos[1]] = dist
        for dir in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            stack.append(((pos[0] + dir[0], pos[1] + dir[1]), dist + 1))
    return distances


def get_positions_x_from(from_pos, x, include_less_than_x=False):
    positions = set()
    stack = [(from_pos, 0)]
    visited = set()
    while stack:
        pos, dist = stack.pop(0)
        if pos in visited:
            continue
        if dist > x:
            continue
        visited.add(pos)
        if dist == x:
            # print(pos,dist)
            positions.add(pos)
            continue
        if dist > 1 and include_less_than_x:
            # print(pos,dist)
            positions.add(pos)
        for dir in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            stack.append(((pos[0] + dir[0], pos[1] + dir[1]), dist + 1))
    return positions


def get_2_step_skips(distances_from_start, distances_from_end, l, is_wall):
    skips = defaultdict(set)
    for i, line in enumerate(distances_from_start):
        for j, v in enumerate(line):
            if v is None:
                continue
            possible_skips = get_positions_x_from((i, j), 2)
            for possible_skip in possible_skips:
                if is_wall(possible_skip):
                    continue
                to_end_at_skip = distances_from_end[possible_skip[0]][possible_skip[1]]
                from_start_to_end = v + 2 + to_end_at_skip
                if from_start_to_end < l:
                    skips[l - from_start_to_end].add(((i, j), possible_skip))
    return skips


def get_20_or_less_steps_skips(distances_from_start, distances_from_end, l, is_wall):
    skips = defaultdict(set)
    for i, line in enumerate(distances_from_start):
        for j, v in enumerate(line):
            if v is None:
                continue
            possible_skips = get_positions_x_from((i, j), 20, include_less_than_x=True)
            for possible_skip in possible_skips:
                if is_wall(possible_skip):
                    continue
                to_end_at_skip = distances_from_end[possible_skip[0]][possible_skip[1]]
                skip_len = abs(possible_skip[0] - i) + abs(possible_skip[1] - j)
                from_start_to_end = v + skip_len + to_end_at_skip
                if from_start_to_end < l:
                    skips[l - from_start_to_end].add(((i, j), possible_skip))
    return skips


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
start, end, is_wall, h, w = parse_input(text)
print_map(start, end, is_wall, h, w)
distances_from_end = get_distances(end, is_wall, h, w)
distances_from_start = get_distances(start, is_wall, h, w)

# print_map(start, end, is_wall, h, w,distances_from_end)
# print_map(start, end, is_wall, h, w,distances_from_start)
from_start_to_end = distances_from_end[start[0]][start[1]]
skips = get_2_step_skips(
    distances_from_start, distances_from_end, from_start_to_end, is_wall
)
# print(skips)
# for k in sorted(skips.keys()):
#     print(k,len(skips[k]))
at_least_100_skips_count = 0
for k in sorted(skips.keys()):
    if k >= 100:
        at_least_100_skips_count += len(skips[k])
print(at_least_100_skips_count)

skips2 = get_20_or_less_steps_skips(
    distances_from_start, distances_from_end, from_start_to_end, is_wall
)
at_least_100_skips_count = 0
for k in sorted(skips2.keys()):
    if k < 50:
        continue
    print(k, len(skips2[k]))
    if k >= 100:
        at_least_100_skips_count += len(skips2[k])
print(at_least_100_skips_count)
