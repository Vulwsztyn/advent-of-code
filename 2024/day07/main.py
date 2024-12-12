from pathlib import Path
import re

file = Path(__file__).parent / "data.txt"
text = file.read_text()
inputs = []
result = 0
for i, v in enumerate(text.split("\n")):
    if not v:
        break
    value, numbers = v.split(":")
    value = int(value)
    numbers = [int(x) for x in numbers.strip().split(" ")]
    inputs.append((value, numbers))
print(inputs)

result = 0
for value, numbers in inputs:
    print(value, numbers)
    possible = [numbers[0]]
    for n in numbers[1:]:
        possible = [x + n for x in possible] + [x * n for x in possible]
    if value in possible:
        result += value
print(result)

result = 0
for value, numbers in inputs:
    print(value, numbers)
    possible = [numbers[0]]
    for n in numbers[1:]:
        possible = (
            [x + n for x in possible]
            + [x * n for x in possible]
            + [int(str(x) + str(n)) for x in possible]
        )
    if value in possible:
        result += value
print(result)
