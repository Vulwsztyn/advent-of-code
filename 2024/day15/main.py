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


def parse_input_wide(text):
    hero = (0, 0)
    boxes = set()
    walls = set()
    vertical_wall = len(text[0]) * 2 - 2
    for i, line in enumerate(text):
        if i == 0:
            continue
        if all(x == "#" for x in line):
            break
        for j, char in enumerate(line):
            if char == "O":
                boxes.add((i, j * 2))
            elif char == "#":
                walls.add((i, j * 2))
            elif char == "@":
                hero = (i, j * 2)
    horizontal_wall = i
    moves = ""
    for j in range(i + 2, len(text)):
        moves += text[j]

    def is_wall(pos):
        i, j = pos
        if i == 0 or j < 2 or i == horizontal_wall or j == vertical_wall:
            return True
        return (i, j - j % 2) in walls

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


def apply_move_wide(move, hero, boxes, is_wall):
    move_to_dir = {
        "^": [-1, 0],
        "v": [1, 0],
        "<": [0, -1],
        ">": [0, 1],
    }

    def box_at_position(pos):
        if pos in boxes:
            return pos
        if (pos[0], pos[1] - 1) in boxes:
            return (pos[0], pos[1] - 1)
        return None

    dir = move_to_dir[move]
    new_position = tuple(hero[i] + dir[i] for i in range(2))
    if box_at_position(new_position) is None and not is_wall(new_position):
        return new_position, set(), dir
    if is_wall(new_position):
        return hero, set(), dir
    position_lookup = new_position
    is_horizontal = dir[0] == 0
    result_boxes = set()
    box = box_at_position(position_lookup)
    if is_horizontal:
        while box is not None:
            result_boxes.add(box)
            if move == "<":
                position_lookup = tuple(box[i] + dir[i] for i in range(2))
            else:
                position_lookup = tuple(box[i] + dir[i] + dir[i] for i in range(2))
            box = box_at_position(position_lookup)
        if is_wall(position_lookup):
            return hero, set(), dir
        else:
            return new_position, result_boxes, dir
    unprocessed_boxes = [box]
    while unprocessed_boxes:
        box = unprocessed_boxes.pop()
        if box in result_boxes:
            continue
        result_boxes.add(box)
        box_right_part = (box[0], box[1] + 1)
        for b in (box, box_right_part):
            new_pos = tuple(b[i] + dir[i] for i in range(2))
            if is_wall(new_pos):
                return hero, set(), dir
            box_at_new_pos = box_at_position(new_pos)
            if box_at_new_pos is not None:
                unprocessed_boxes.append(box_at_new_pos)
    return new_position, result_boxes, dir


def print_map(h, w, hero, boxes, is_wall):
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
    print()


def print_map_wide(h, w, hero, boxes, is_wall):
    for i in range(h + 1):
        for j in range(w + 1):
            msg = "."
            if is_wall((i, j)):
                msg = "#"
            elif (i, j) in boxes:
                msg = "["
            elif (i, j - 1) in boxes:
                msg = "]"
            elif (i, j) == hero:
                msg = "@"
            print(msg, end="")
        print("#")
    print()


def boxes_to_result(boxes):
    result = 0
    for box in boxes:
        result += 100 * box[0] + box[1]
    return result


def boxes_to_result_wide(boxes, h, w):
    result = 0
    for i, j in boxes:
        horizontal_diff = i
        vertical_diff = j
        result += 100 * horizontal_diff + vertical_diff
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
hero, boxes, walls, moves, is_wall, h, w = parse_input(text)
print_map(h, w, hero, boxes, is_wall)

for move in moves:
    new_position, box_to_remove, box_to_add = apply_move(move, hero, boxes, is_wall)
    # print(move, new_position, box_to_remove, box_to_add)
    hero = new_position
    if box_to_remove is not None:
        boxes.remove(box_to_remove)
        boxes.add(box_to_add)
    # print_map(h,w,hero,boxes,walls)

print(boxes_to_result(boxes))
hero, boxes, walls, moves, is_wall, h, w = parse_input_wide(text)
print_map_wide(h, w, hero, boxes, is_wall)

for move in moves:
    # print(move)
    new_position, boxes_to_change, dir = apply_move_wide(move, hero, boxes, is_wall)
    hero = new_position
    for box in boxes_to_change:
        boxes.remove(box)
    for box in boxes_to_change:
        boxes.add(tuple(box[i] + dir[i] for i in range(2)))
    # print_map_wide(h, w, hero, boxes, is_wall)
print(boxes_to_result(boxes))
