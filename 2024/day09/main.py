from pathlib import Path
from itertools import chain

file = Path(__file__).parent / "data.txt"
text = file.read_text().strip()

is_file = True
current_id = 0
file_id = 0
files = []
blanks = []
for i in (int(x) for x in text):
    if is_file:
        files.append((current_id, i, file_id))
        file_id += 1
    else:
        blanks.append((current_id, i))
    current_id += i
    is_file = not is_file
print(files)
print(blanks)

moved = []
for start, length in blanks:
    should_break = False
    while length > 0:
        last = files.pop()
        if start > last[0]:
            files.append(last)
            should_break = True
            break
        moved.append((start, min(length, last[1]), last[2]))
        if last[1] > length:
            files.append((last[0], last[1] - length, last[2]))
        start += last[1]
        length -= last[1]
    if should_break:
        break
print(moved)
print(files)

result = 0
for start, length, value in chain(files, moved):
    print(start, length, value)
    to_add = start * length + (length * (length - 1)) / 2
    print(to_add)
    result += to_add * value
print(result)
