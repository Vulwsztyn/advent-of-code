from pathlib import Path
from collections import defaultdict


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


def is_valid_helper(previous, index, update, rules):
    current = update[index]
    must_be_after = rules[current]
    violate = must_be_after.intersection(previous)
    # print(update, previous, current, must_be_after)
    if violate:
        print(violate)
        return False
    if index == len(update) - 1:
        return True
    return is_valid_helper(previous | {update[index]}, index + 1, update, rules)


def is_valid(update, rules):
    return is_valid_helper(set(), 0, update, rules)


file = Path("test.txt")
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
    print(update, valid)
print(result)
