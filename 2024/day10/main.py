from pathlib import Path
import re


def find_trails(pos, text, value):
    if 0 > pos[0] or pos[0] >= len(text) or 0 > pos[1] or pos[1] >= len(text[0]):
        return set()
    if text[pos[0]][pos[1]] != str(value):
        return set()
    print(f"({pos[0]}, {pos[1]}): {value}")
    if value == 9:
        return set([pos])
    result = set()
    result |= find_trails((pos[0] - 1, pos[1]), text, value + 1)
    result |= find_trails((pos[0] + 1, pos[1]), text, value + 1)
    result |= find_trails((pos[0], pos[1] - 1), text, value + 1)
    result |= find_trails((pos[0], pos[1] + 1), text, value + 1)
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text().splitlines()
result = 0
for i, line in enumerate(text):
    for j, v in enumerate(line):
        to_add = len(find_trails((i, j), text, 0))
        # if v == "0":
        #     print(f"({i}, {j}): {to_add}")
        result += to_add
print(result)
