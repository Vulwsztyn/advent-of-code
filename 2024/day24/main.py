from pathlib import Path
import re
from collections import defaultdict
from collections.abc import Mapping


def parse_input(text):
    initial_values = {}
    i = 0
    while text[i]:
        var, value = text[i].split(": ")
        initial_values[var] = value == "1"
        i += 1
    gates = []
    i += 1
    j = i
    indices_affected = defaultdict(set)
    while i < len(text) and text[i]:
        inputs_merged, output = text[i].split(" -> ")
        inputs = inputs_merged.split(" ")
        gates.append([*inputs, output])
        for ind in (inputs[0], inputs[2]):
            indices_affected[ind].add(i - j)
        i += 1
    return initial_values, gates, indices_affected


def abc(v1, v2, op):
    if op == "OR":
        return v1 or v2
    if op == "AND":
        return v1 and v2
    return v1 != v2


def from_binary(values):
    print(values)
    result = 0
    for i in values:
        if i:
            result += 1
        result *= 2
    return result // 2


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
values, gates, indices_affected = parse_input(text)
print(values, gates, indices_affected)
stack = list(values.keys())
gates_solved = set()
while stack and len(gates_solved) < len(gates):
    current = stack.pop()
    for i in indices_affected[current]:
        if i in gates_solved:
            continue
        value0, op, value1, output = gates[i]
        if value0 in values and value1 in values:
            v = abc(values[value0], values[value1], op)
            values[output] = v
            stack.append(output)
            gates_solved.add(i)
print(values)
result = from_binary(
    list(
        values[y]
        for y in sorted((x for x in values.keys() if x.startswith("z")), reverse=True)
    )
)
print(result)
