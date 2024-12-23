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


file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
connections = get_connections(text)
print(connections)
result = get_3s_with_t(connections)
for i in result:
    print(i)
print(len(result))
