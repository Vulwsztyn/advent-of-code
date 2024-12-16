from pathlib import Path
import re
from collections import defaultdict

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
for i in range(100, 101):
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
