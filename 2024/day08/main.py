from pathlib import Path
from collections import defaultdict
import re

file = Path(__file__).parent / "data.txt"
text = file.read_text().strip()

nodes = defaultdict(list)
for i,line in enumerate(text.split("\n")):
    for j,v in enumerate(line):
        if v != ".":
            nodes[v].append((i,j))
print(nodes)

antinodes = set()
for k, positions in nodes.items():
    print(k, positions)
    for i,p in enumerate(positions):
        for q in positions[i+1:]:
            d_row = q[0] - p[0]
            d_col = q[1] - p[1]
            antinodes.add((p[0] - d_row, p[1] - d_col))
            antinodes.add((q[0] + d_row, q[1] + d_col))
print(antinodes)

correct_antinodes = {x for x in antinodes if 0 <= x[0] < len(text.split("\n")) and 0 <= x[1] < len(text.split("\n")[0])}

print(correct_antinodes)

print(len(correct_antinodes))
print(len(text.split("\n")))
