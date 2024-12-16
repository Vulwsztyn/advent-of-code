from pathlib import Path
import re
from collections import defaultdict
import numpy


def part_1(robots, width, height, i):
    positions = defaultdict(int)
    for r in robots:
        col = (r[0] + r[2] * i) % width
        row = (r[1] + r[3] * i) % height
        # print(col,row)
        positions[(row, col)] += 1
    print(positions)
    for i in range(height):
        for j in range(width):
            msg = "." if (i, j) not in positions else positions[(i, j)]
            print(msg, end="")
        print()
    print()

    results = [0, 0, 0, 0]
    for (row, col), value in positions.items():
        if row == height // 2:
            continue
        if col == width // 2:
            continue
        index = (0 if row < height // 2 else 2) + (0 if col < width // 2 else 1)
        results[index] += value
    print(results)
    result = 1
    for i in results:
        result *= i
    print(result)


file = Path(__file__).parent / "data.txt"
width, height = (11, 7) if str(file).endswith("test.txt") else (101, 103)
text = file.read_text().strip().splitlines()
robots = []
for line in text:
    for m in re.findall(r"(-?\d+),(-?\d+)[^\d-]*(-?\d+),(-?\d+)", line):
        robots.append(tuple((int(x) for x in (m[0], m[1], m[2], m[3]))))
print(robots)
# robots=robots[:1]
# robots=[(2,4,2,-3)]
part_1(robots, width, height, 100)


min_var_rows = 1e9
min_var_cols = 1e9
i_min_var_rows = 0
i_min_var_cols = 0
for i in range(104):
    rows = []
    cols = []
    for r in robots:
        col = (r[0] + r[2] * i) % width
        row = (r[1] + r[3] * i) % height
        rows.append(row)
        cols.append(col)
    var_cols = numpy.var(cols)
    var_rows = numpy.var(rows)
    if min_var_rows > var_rows:
        min_var_rows = var_rows
        i_min_var_rows = i
    if min_var_cols > var_cols:
        min_var_cols = var_cols
        i_min_var_cols = i
print(i_min_var_rows, i_min_var_cols)
my_i = 0
for i in range(103):
    if (i_min_var_rows + height * i) % width == i_min_var_cols:
        my_i = i
part_1(robots, width, height, i_min_var_rows + height * my_i)
print(i_min_var_rows + height * my_i)
