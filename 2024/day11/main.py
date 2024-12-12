from pathlib import Path
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: "Node | None" = None

    def __len__(self):
        current = self
        count = 0
        while current is not None:
            count += 1
            current = current.next
        return count


def print_list(head: Node, limit: int | None = None):
    current = head
    count = 0
    while current is not None:
        print(current.value, end=" ")
        count += 1
        if limit is not None and count >= limit:
            break
        current = current.next
    print()


def do_stuff(head: Node | None):
    current = head
    while current is not None:
        stringified = str(current.value)
        if current.value == 0:
            current.value = 1
        elif len(stringified) % 2 == 0:
            current.value = int(stringified[: len(stringified) // 2])
            n = current.next
            current.next = Node(int(stringified[len(stringified) // 2 :]))
            current.next.next = n
            current = current.next
        else:
            current.value *= 2024
        current = current.next


def len_finder(value: int, iterations: int, memo: dict[str, int]) -> int:
    if iterations == 0:
        return 1
    key = f"{value},{iterations}"
    if key in memo:
        return memo[key]
    result: int
    stringified = str(value)
    if value == 0:
        result = len_finder(1, iterations - 1, memo)
    elif len(stringified) % 2 == 0:
        result = len_finder(
            int(stringified[: len(stringified) // 2]), iterations - 1, memo
        ) + len_finder(int(stringified[len(stringified) // 2 :]), iterations - 1, memo)
    else:
        result = len_finder(value * 2024, iterations - 1, memo)
    memo[key] = result
    return result


file = Path(__file__).parent / "data.txt"
text = file.read_text()
values = [int(x) for x in text.strip().split(" ")]
head = Node(values[0])
current = head
for value in values[1:]:
    current.next = Node(value)
    current = current.next
print_list(head)
for i in range(25):
    do_stuff(head)
print(len(head))

result = 0
for value in values:
    to_add = len_finder(value, 75, {})
    print(value, to_add)
    result += to_add
print(result)
