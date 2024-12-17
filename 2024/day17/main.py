from pathlib import Path
import re
from itertools import chain


def parse_input(text):
    registers = []
    for i in range(3):
        for m in re.findall(r":\s(\d+)$", text[i]):
            registers.append(int(m))
    program = [int(m[0]) for m in re.findall(r"(\d+)", text[4])]
    return registers, program, []


def part_1(registers, program, output, should_return_self=False, verbose=False):
    i = 0
    while i < len(program):
        opcode = program[i]
        combo = program[i + 1]
        # print(opcode,combo)
        combo_value = combo if combo < 4 or opcode == 4 else registers[combo - 4]
        if opcode == 0:
            registers[0] = registers[0] // 2**combo_value
        elif opcode == 1:
            registers[1] ^= combo_value
        elif opcode == 2:
            registers[1] = combo_value % 8
        elif opcode == 3:
            if registers[0] == 0:
                i += 2
            else:
                i = combo_value
        elif opcode == 4:
            registers[1] ^= registers[2]
        elif opcode == 5:
            new_index = len(output)
            output.append(combo_value % 8)
            print(registers, combo_value % 8)

        elif opcode == 6:
            registers[1] = registers[0] // 2**combo_value
        elif opcode == 7:
            registers[2] = registers[0] // 2**combo_value
        if verbose:
            print(i, opcode, combo, combo_value)
            print(registers, output)
        if opcode != 3:
            i += 2

    print(registers)
    print(",".join(str(i) for i in output))
    return output


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
registers, program, output = parse_input(text)
print(registers, program)
# part_1(registers, program, output)
# exit()
stack = [[0]]
while True:
    current = stack.pop()
    value = 0
    for i in current:
        value += i
        value *= 8
    for i in range(7, -1, -1):
        new_value = value + i
        output = part_1([new_value, 0, 0], program, [])
        print(i, output)
        if ",".join(str(x) for x in program).endswith(",".join(str(x) for x in output)):
            stack.append([*current, i])
            if output == program:
                print(new_value)
                exit()
