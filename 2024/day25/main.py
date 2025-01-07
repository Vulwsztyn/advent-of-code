from pathlib import Path
import re
from collections import defaultdict
from collections.abc import Mapping

def parse_input(text):
    locks=[]
    keys=[]
    index=0
    while index<len(text):
        values=[6]*5
        locks_or_keys = locks if all(x=='#'for x in text[index]) else keys
        for i in range(7):
            for j in range(5):
                if text[index][j] == '.':
                    values[j]-=1
            index+=1
        index+=1
        locks_or_keys.append(values)
    return locks,keys

file = Path(__file__).parent / "data.txt"
text = file.read_text().strip().splitlines()
locks, keys = parse_input(text)
print(locks,keys)
result=0
for lock in locks:
    for key in keys:
        if all(lock[i]+key[i]<6 for i in range(5)):
            result+=1
print(result)            
