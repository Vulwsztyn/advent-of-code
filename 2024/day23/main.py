from pathlib import Path
import re
from collections import defaultdict
from collections.abc import Mapping


def get_connections(text):
    result = defaultdict(set)
    for line in text:
        a, b = line.split("-")
        result[a].add(b)
        result[b].add(a)
    return result


def is_clique(pretendent, connections):
    for x in pretendent:
        if not connections[x] | {x} >= pretendent:
            return False
    return True


def get_pairs(text):
    result = []
    for line in text:
        a, b = line.split("-")
        result.append({a, b})
    return result


def get_3s_with_t(connections: Mapping[str, set]):
    result = []
    for k in connections.keys():
        if not k.startswith("t"):
            continue
        key_connections = connections[k]
        for connection in key_connections:
            for common_connection in key_connections.intersection(
                connections[connection]
            ):
                to_add = {k, connection, common_connection}
                if to_add not in result:
                    result.append({k, connection, common_connection})
    return result


def get_3s(connections: Mapping[str, set]):
    result = []
    for k in connections.keys():
        # if not k.startswith("t"):
        #     continue
        key_connections = connections[k]
        for connection in key_connections:
            for common_connection in key_connections.intersection(
                connections[connection]
            ):
                to_add = {k, connection, common_connection}
                if to_add not in result:
                    result.append({k, connection, common_connection})
    return result


def get_one_larger_sets(sets, connections):
    current_len = len(sets[0])
    result = set()
    for i, set1 in enumerate(sets):
        if i % 100 == 0:
            print(i, len(result))
        for j in range(i + 1, len(sets)):
            set2 = sets[j]
            sum_ = set1 | set2
            if len(sum_) != current_len + 1:
                continue
            only_in_set1 = sum_ - set2
            only_in_set2 = sum_ - set1
            if not only_in_set2 < connections[list(only_in_set1)[0]]:
                continue
            result.add(tuple(sorted(sum_)))
    return [set(x) for x in result]


def get_fully_connected_subgraph(nodes, connections):
    connected_to_all = connections[nodes[0]]
    for i in range(1, len(nodes)):
        connected_to_all = connected_to_all.intersection(connections[nodes[i]])
    if not connected_to_all:
        return nodes
    biggest = None
    for i in connected_to_all:
        x = get_fully_connected_subgraph([*nodes, i], connections)
        if biggest is None or len(x) > len(biggest):
            biggest = x
    return biggest


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
connections = get_connections(text)
print(connections)
result = get_3s_with_t(connections)
for i in result:
    print(i)
print(len(result))
computers = {v for _, values in connections.items() for v in values}
pairs = get_pairs(text)
print(len(pairs))
for k, v in connections.items():
    print(k, v)
print(len(connections))
clique_pretenders = [
    set(x) for x in {tuple(sorted({k} | v)) for k, v in connections.items()}
]
for i in clique_pretenders:
    if is_clique(i, connections):
        print(i)
for i in clique_pretenders:
    for j in i:
        if is_clique(i - {j}, connections):
            print(",".join(sorted(i - {j})))
