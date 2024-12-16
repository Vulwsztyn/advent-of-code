from pathlib import Path
import re
from itertools import chain


def parse_input(text):
    hero = (0, 0)
    boxes = set()
    walls = set()
    vertical_wall = len(text[0]) - 1
    for i, line in enumerate(text):
        if i == 0:
            continue
        if all(x == "#" for x in line):
            break
        for j, char in enumerate(line):
            if char == "O":
                boxes.add((i, j))
            elif char == "#":
                walls.add((i, j))
            elif char == "@":
                hero = (i, j)
    horizontal_wall = i
    moves = ""
    for j in range(i + 2, len(text)):
        moves += text[j]

    def is_wall(pos):
        i, j = pos
        if i == 0 or j == 0 or i == horizontal_wall or j == vertical_wall:
            return True
        return (i, j) in walls

    return hero, boxes, walls, moves, is_wall, horizontal_wall, vertical_wall


def apply_move(move, hero, boxes, is_wall):
    move_to_dir = {
        "^": [-1, 0],
        "v": [1, 0],
        "<": [0, -1],
        ">": [0, 1],
    }
    dir = move_to_dir[move]
    new_position = tuple(hero[i] + dir[i] for i in range(2))
    if new_position not in boxes and not is_wall(new_position):
        return new_position, None, None
    position_lookup = new_position
    while position_lookup in boxes:
        position_lookup = tuple(position_lookup[i] + dir[i] for i in range(2))
    if is_wall(position_lookup):
        return hero, None, None
    else:
        return new_position, new_position, position_lookup


def print_map(h, w, hero, boxes, walls):
    for i in range(h + 1):
        for j in range(w + 1):
            msg = "."
            if is_wall((i, j)):
                msg = "#"
            elif (i, j) in boxes:
                msg = "O"
            elif (i, j) == hero:
                msg = "@"
            print(msg, end="")
        print()


def boxes_to_result(boxes):
    result = 0
    for box in boxes:
        result += 100 * box[0] + box[1]
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
hero, boxes, walls, moves, is_wall, h, w = parse_input(text)
print_map(h, w, hero, boxes, walls)
print()
for move in moves:
    new_position, box_to_remove, box_to_add = apply_move(move, hero, boxes, is_wall)
    # print(move, new_position, box_to_remove, box_to_add)
    hero = new_position
    if box_to_remove is not None:
        boxes.remove(box_to_remove)
        boxes.add(box_to_add)
    # print_map(h,w,hero,boxes,walls)
    # print()
print(boxes_to_result(boxes))
