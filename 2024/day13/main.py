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


def solve(input, addendum=0):
    result = 0
    for button_a, button_b, prize in input:
        x1, y1 = button_a
        x2, y2 = button_b
        xt, yt = prize
        xt += addendum
        yt += addendum
        # xt=a*x1+b*x2
        # yt=a*y1+b*y2
        # solving the equations we get A=(xt*y2-yt*x2)/(x1*y2-y1*x2)
        q = xt * y2 - yt * x2
        w = x1 * y2 - y1 * x2
        if w == 0:
            print((button_a, button_b, prize))
            raise "aaa"
        if q % w != 0:
            continue
        a = q // w
        # b=(yt-a*y1)//y2
        if y2 == 0:
            print((button_a, button_b, prize))
            raise "aaa"
        e = yt - a * y1
        if e % y2 != 0:
            continue
        b = e // y2
        result += a * 3 + b
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
input = parse_input(text)
print(input)

r1 = solve(input)
r2 = solve(input, 10000000000000)
print(r1)
print(r2)
