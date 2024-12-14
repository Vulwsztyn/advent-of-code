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


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
is_legal_position = (
    lambda x: x[0] >= 0 and x[0] < len(text) and x[1] >= 0 and x[1] < len(text[0])
)
visited = create_visited(text)
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
print(result)
