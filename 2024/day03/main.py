from pathlib import Path
import re

file = Path("data.txt")
text = file.read_text()
result = 0
for i, v in enumerate(text.split("\n")):
    print(i, v)
    for m in re.findall(r"mul\((\d+),(\d+)\)", v):
        result += int(m[0]) * int(m[1])
print(result)
result = 0
enabled = True
for i, v in enumerate(text.split("\n")):
    print(i, v)
    for m in re.findall(r"(?:(?:mul\((\d+),(\d+)\))|(do\(\))|(don\'t\(\)))", v):
        # print(m)
        if m[3]:
            enabled = False
        elif m[2]:
            enabled = True
        elif enabled:
            result += int(m[0]) * int(m[1])
print(result)
