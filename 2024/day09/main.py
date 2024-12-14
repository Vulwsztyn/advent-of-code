from pathlib import Path
from itertools import chain


def get_files_and_blanks(text):
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
    # print(files)
    # print(blanks)
    return files, blanks


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip()

files, blanks = get_files_and_blanks(text)

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

result = 0
for start, length, value in chain(files, moved):
    # print(start, length, value)
    to_add = start * length + (length * (length - 1)) // 2
    # print(to_add)
    result += to_add * value
print(result)

files, blanks = get_files_and_blanks(text)

moved = []
unmoved = []
index_to_be_moved = len(files) - 1
for start, length, value in files[::-1]:
    should_break = False
    did_move = False
    for i, (blank_start, blank_length) in enumerate(blanks):
        if blank_start > start:
            should_break = i == 0
            break
        if blank_length >= length:
            did_move = True
            moved.append((blank_start, length, value))
            blanks[i] = (blank_start + length, blank_length - length)
            break
    if not did_move:
        unmoved.append((start, length, value))
    if should_break:
        break
print(unmoved)
print(moved)
result = 0
for start, length, value in chain(unmoved, moved):
    # print(start, length, value)
    to_add = start * length + (length * (length - 1)) // 2
    # print(to_add)
    result += to_add * value
print(result)
