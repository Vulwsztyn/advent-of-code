from pathlib import Path
import re


def parse_input(text):
    patterns = [x.strip() for x in text[0].strip().split(",")]
    designs = text[2:]
    return patterns, designs


file = Path(__file__).parent / "test.txt"
text = file.read_text().strip().splitlines()
patterns, designs = parse_input(text)
print(patterns, designs)
regex = rf"^({'|'.join(f'({x})' for x in patterns)})+$"
print(regex)
possible_count = 0
all_ways = 0
for design_i, design in enumerate(designs):
    print(design_i, design)
    for m in re.findall(regex, design, re.MULTILINE):
        print(m)
print(possible_count)
print(all_ways)
