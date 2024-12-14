from pathlib import Path


def create_visited(text):
    visited = []
    for i in range(len(text)):
        visited.append([])
        for _ in range(len(text[0])):
            visited[i].append(False)
    return visited


def get_next_to_visit(visited):
    for i, line in enumerate(visited):
        for j, v in enumerate(line):
            if not v:
                return (i, j)
    return None


def undiscounte_price(visited, text, is_legal_position):
    next_to_visit = get_next_to_visit(visited)
    result = 0
    while next_to_visit is not None:
        perimeter = 0
        area = 0
        to_visit = [(next_to_visit)]
        current = text[next_to_visit[0]][next_to_visit[1]]
        while to_visit:
            (i, j) = to_visit.pop()
            if visited[i][j]:
                continue
            visited[i][j] = True
            area += 1
            for dir in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                ni = i + dir[0]
                nj = j + dir[1]
                if not is_legal_position((ni, nj)):
                    perimeter += 1
                elif text[ni][nj] != current:
                    perimeter += 1
                else:
                    to_visit.append((ni, nj))
        print(current, area, perimeter)
        result += area * perimeter
        next_to_visit = get_next_to_visit(visited)
    return result


def discounte_price(visited, text, is_legal_position):
    next_to_visit = get_next_to_visit(visited)
    result = 0
    while next_to_visit is not None:
        perimeter = 4
        area = 0
        to_visit = [(next_to_visit)]
        current = text[next_to_visit[0]][next_to_visit[1]]
        top_sides, bot_sides, left_sides, right_sides = [], [], [], []
        while to_visit:
            (i, j) = to_visit.pop()
            if visited[i][j]:
                continue
            visited[i][j] = True
            area += 1
            for sides, dir, reverse_col_row_for_sides in [
                (top_sides, [-1, 0], False),
                (bot_sides, [1, 0], False),
                (left_sides, [0, -1], True),
                (right_sides, [0, 1], True),
            ]:
                ni = i + dir[0]
                nj = j + dir[1]
                if not is_legal_position((ni, nj)) or text[ni][nj] != current:
                    sides.append((i, j) if not reverse_col_row_for_sides else (j, i))
                else:
                    to_visit.append((ni, nj))
        for sides in (top_sides, bot_sides, right_sides, left_sides):
            sides.sort()
            for i in range(1, len(sides)):
                current = sides[i]
                previous = sides[i - 1]
                is_continuation = (
                    current[0] == previous[0] and current[1] == previous[1] + 1
                )
                if not is_continuation:
                    perimeter += 1
        print(current, area, top_sides, bot_sides, right_sides, left_sides, perimeter)
        result += area * perimeter
        next_to_visit = get_next_to_visit(visited)
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
is_legal_position = (
    lambda x: x[0] >= 0 and x[0] < len(text) and x[1] >= 0 and x[1] < len(text[0])
)
visited = create_visited(text)
result = undiscounte_price(visited, text, is_legal_position)
print(result)

visited = create_visited(text)
result = discounte_price(visited, text, is_legal_position)
print(result)
