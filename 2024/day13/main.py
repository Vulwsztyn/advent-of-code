from pathlib import Path
import re


def parse_input(text):
    i = 0
    result = []
    while i < len(text):
        subresult = []
        for j in range(3):
            for m in re.findall(r"(\d+)\D*(\d+)", text[i + j]):
                subresult.append((int(m[0]), int(m[1])))
        i += 4
        result.append(subresult)
    return result


def part1(input):
    result = 0
    for button_a, button_b, prize in input:
        best = None
        for button_a_presses in range(101):
            if (prize[0] - button_a[0] * button_a_presses) < 0:
                break
            if (prize[1] - button_a[1] * button_a_presses) < 0:
                break
            if (prize[0] - button_a[0] * button_a_presses) % button_b[0] != 0:
                continue
            if (prize[1] - button_a[1] * button_a_presses) % button_b[1] != 0:
                continue
            button_b_presses_1 = (
                prize[0] - button_a[0] * button_a_presses
            ) // button_b[0]
            button_b_presses_2 = (
                prize[1] - button_a[1] * button_a_presses
            ) // button_b[1]
            if button_b_presses_1 != button_b_presses_2:
                continue
            button_b_presses = button_b_presses_1
            if button_b_presses >= 101:
                continue
            current = button_a_presses * 3 + button_b_presses
            if best is None or current < best:
                best = current
        if best is not None:
            result += best
    return result


def part2(input):
    result = 0
    for button_a, button_b, prize in input:
        print((button_a, button_b, prize))
        best = None
        prize = tuple(x + 10000000000000 for x in prize)
        for button_a_presses in range(button_b[0]):
            if (prize[0] - button_a[0] * button_a_presses) < 0:
                break
            if (prize[0] - button_a[0] * button_a_presses) % button_b[0] != 0:
                continue
            button_b_presses = (prize[0] - button_a[0] * button_a_presses) // button_b[
                0
            ]
            print(button_a_presses, button_b_presses)
        if best is not None:
            result += best
    return result


file = Path(__file__).parent / "test.txt"
text = file.read_text().strip().splitlines()
input = parse_input(text)
print(input)
r1 = part1(input)
r2 = part2(input)
print(r1)
print(r2)
