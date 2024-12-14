from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: "Node | None" = None
    previous: "Node | None" = None

    def __len__(self):
        current = self
        count = 0
        while current is not None:
            count += 1
            current = current.next
        return count

    def get(self, index):
        current = self
        for i in range(index):
            if current is None:
                return None
            current = current.next
        return current


def get_rules_and_updates(text):
    rules = defaultdict(set)
    updates = []
    should_get_updates = False
    for line in text:
        if not line:
            should_get_updates = True
            continue
        if should_get_updates:
            updates.append([int(x) for x in line.split(",")])
        else:
            a, b = [int(x) for x in line.split("|")]
            rules[a].add(b)
    return rules, updates


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


def is_valid_helper(previous, index, update, rules):
    current = update[index]
    must_be_after = rules[current]
    violate = must_be_after.intersection(previous)
    # print(update, previous, current, must_be_after)
    if violate:
        return False
    if index == len(update) - 1:
        return True
    return is_valid_helper(previous | {update[index]}, index + 1, update, rules)


def is_valid(update, rules):
    return is_valid_helper(set(), 0, update, rules)


file = Path(__file__).parent / "data.txt"
text = file.read_text().split("\n")
rules, updates = get_rules_and_updates(text)
print(rules)
print(updates)
result = 0
for update in updates:
    valid = is_valid(update, rules)
    if valid:
        to_add = update[len(update) // 2]
        print(to_add)
        result += to_add
        print(update)
print(result)
print()

result = 0
for update in updates:
    linked_list = Node(update[0])
    current = linked_list
    for i in update[1:]:
        current.next = Node(i)
        current.next.previous = current
        current = current.next
    changed = False
    current = linked_list
    while current is not None:
        current_2 = current.next
        next_current = current.next
        previous_current = current.previous
        changed_this_round = False
        while current_2 is not None:
            # print(current.value, current_2.value)
            if current.value in rules[current_2.value]:
                changed_this_round = True
                changed = True
                next_current2 = current_2.previous
                current_2.previous.next = current_2.next
                if current_2.next is not None:
                    current_2.next.previous = current_2.previous
                current_2.previous = current.previous
                current_2.next = current
                if current.previous is not None:
                    current.previous.next = current_2
                else:
                    linked_list = current_2
                current.previous = current_2
                # print_list(linked_list)
                current_2 = next_current2
            current_2 = current_2.next
        if not changed_this_round:
            current = next_current
        elif previous_current is not None:
            current = previous_current.next
        else:
            current = linked_list
    if changed:
        to_add = linked_list.get(len(update) // 2).value
        # print(to_add)
        result += to_add
print(result)
