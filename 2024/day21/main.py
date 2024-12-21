from pathlib import Path
import re

numeric_keyboard = [
    "789",
    "456",
    "123",
    " 0A",
]
arrow_keyboard = [" ^A", "<v>"]

arrow_to_dir = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}

dir_to_arrow = {
    (0, 1): ">",
    (0, -1): "<",
    (-1, 0): "^",
    (1, 0): "v",
}

dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))


def apply_dir(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])


def position_of_char(keyboard, char):
    for i, line in enumerate(keyboard):
        for j, c in enumerate(line):
            if c == char:
                return (i, j)
    raise ValueError("WTF")


def char_at_pos(keyboard, pos):
    if pos[0] >= len(keyboard):
        return ""
    if pos[1] >= len(keyboard[0]):
        return ""
    return keyboard[pos[0]][pos[1]]


def pos_diff(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos2[1] - pos1[1])


def all_ways_from_pos_to_pos(start, end, hole_pos, ways_memo):
    if (start, end) in ways_memo:
        return ways_memo[(start, end)]
    if end == start:
        return {""}
    if end[0] == start[0]:
        result = (
            {"<" * (start[1] - end[1])}
            if start[1] > end[1]
            else {">" * (-start[1] + end[1])}
        )
        ways_memo[start, end] = result
        return result
    if end[1] == start[1]:
        result = (
            {"^" * (start[0] - end[0])}
            if start[0] > end[0]
            else {"v" * (-start[0] + end[0])}
        )
        ways_memo[start, end] = result
        return result
    result = set()
    diff = pos_diff(start, end)
    for dir in dirs:
        new_pos = apply_dir(start, dir)
        if pos_diff(end, new_pos) >= diff or new_pos == hole_pos:
            continue
        result = result | {
            dir_to_arrow[dir] + x
            for x in all_ways_from_pos_to_pos(new_pos, end, hole_pos, ways_memo)
        }
    ways_memo[start, end] = result
    return result


def add_at_end(ways, suffixes):
    results = set()
    for way in ways:
        for suffix in suffixes:
            results.add(way + suffix + "A")
    return results


def add_at_front(ways, prefixes):
    results = set()
    for way in ways:
        for prefix in prefixes:
            results.add(prefix + "A" + way)
    return results


def all_ways_to_enter_code(pos, code, keyboard, memo, hole_pos, ways_memo):
    key = (pos, code)
    if key in memo:
        return memo[key]
    if not code:
        return {""}
    next_char = code[0]
    char_pos = position_of_char(keyboard, next_char)
    all_ways_to_next_char = all_ways_from_pos_to_pos(pos, char_pos, hole_pos, ways_memo)
    all_ways_to_enter_rest_of_the_code = all_ways_to_enter_code(
        char_pos, code[1:], keyboard, memo, hole_pos, ways_memo
    )
    result = add_at_front(all_ways_to_enter_rest_of_the_code, all_ways_to_next_char)
    memo[key] = result
    return result


def ways_to_achieve(
    set_of_goals, keyboard=arrow_keyboard, memo={}, hole_pos=(0, 0), ways_memo={}
):
    ways = set()
    for i, code in enumerate(set_of_goals):
        current_pos = position_of_char(keyboard, "A")
        current_ways = all_ways_to_enter_code(
            current_pos, code, keyboard, memo, hole_pos, ways_memo
        )
        ways = ways | current_ways
    return ways


def split_into_ending_with_A(string):
    return re.findall("[^A]*A", string)


def ways_to_write(sequence, level, memo):
    key = (sequence, level)
    if key in memo:
        return memo[key]
    if level == 0:
        return len(sequence)
    ways = ways_to_achieve({sequence})
    result: int = -1
    for way in ways:
        current = 0
        for sequence in split_into_ending_with_A(way):
            to_add = ways_to_write(sequence, level - 1, memo)
            print("-", way, sequence, current, to_add)
            current += to_add
        if result < 0 or current < result:
            result = current
    memo[key] = result
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
result = 0
memo = {}
for code in text:
    code = code.strip()
    print(code)
    current_pos = position_of_char(numeric_keyboard, "A")
    ways1 = ways_to_achieve(set([code]), numeric_keyboard, {}, (3, 0), {})
    print(ways1)
    min_len = -1
    for way in ways1:
        print(way)
        current = 0
        for sequence in split_into_ending_with_A(way):
            x = ways_to_write(sequence, 25, memo)
            print(sequence, x)
            current += x
        if min_len < 0 or current < min_len:
            min_len = current
    number = int(code[:-1])
    print(number, min_len, number * min_len)
    result += number * min_len
print(result)
