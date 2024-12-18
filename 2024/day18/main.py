from pathlib import Path
import re
from itertools import chain


def parse_input(text, h, w, how_many):
    raindeer = (0, 0)
    end = (h - 1, w - 1)
    walls = set()
    for i, line in enumerate(text):
        if i >= how_many:
            break
        col, row = [int(x) for x in line.split(",")]
        walls.add((row, col))

    def is_wall(pos):
        i, j = pos
        if i < 0 or j < 0 or i >= h or j >= w:
            return True
        return (i, j) in walls

    return raindeer, end, is_wall


def print_map(r, e, is_wall, h, w, achieved):
    for i in range(h):
        for j in range(w):
            msg = "."
            if is_wall((i, j)):
                msg = "#"
            elif (i, j) == r:
                msg = "S"
            elif (i, j) == e:
                msg = "E"
            elif (i, j) in achieved:
                msg = "O"
            print(msg, end="")
        print()
    print()


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
w, h, how_many = (7, 7, 12) if str(file).endswith("test.txt") else (71, 71, 1024)
raindeer, end, is_wall = parse_input(text, h, w, how_many)
print_map(raindeer, end, is_wall, h, w, {})
achieved = {}
stack: list[tuple[tuple[int, int], int, tuple[int, int], list[tuple[int, int]]]] = [
    (raindeer, 0, (0, 1), [])
]
cheapest_end = 1e9
best_paths = []
iterations = 0
while stack:
    pos, v, current_dir, path_until_now = stack.pop(0)
    new_path = [*path_until_now, pos]
    should_skip = False
    if pos == end:
        print(end, v, new_path)
        if v < cheapest_end:
            cheapest_end = v
            best_paths = [new_path]
            achieved[pos] = v
        elif v == cheapest_end:
            best_paths.append(new_path)
            achieved[pos] = v
        continue
    if pos in achieved and achieved[pos] <= v:
        continue
    if v > cheapest_end:
        continue
    achieved[pos] = v
    for dir in (
        current_dir,
        (current_dir[1], current_dir[0]),
        (-current_dir[1], -current_dir[0]),
    ):
        dir: tuple[int, int] = tuple(dir)
        new_pos: tuple[int, int] = tuple(pos[i] + dir[i] for i in range(2))
        if is_wall(new_pos):
            continue
        stack.append((new_pos, v + 1, dir, new_path))
    # for pos,v,current_dir,path in stack:
    #     print(pos,v,current_dir)
    # print(achieved)
    # print()
    # iterations+=1
    # if iterations%100==0:
    #     print_map(raindeer, end, is_wall, h, w, achieved)
    #     input()

print(cheapest_end)
print_map(None, None, is_wall, h, w, best_paths[0])
print(best_paths)
# print(len(best_paths))
# # in_best = set()
# # for i in best_paths:
# #     in_best |= set(i)
# # print(len(in_best))
# print(list(len(x) for x in best_paths))
