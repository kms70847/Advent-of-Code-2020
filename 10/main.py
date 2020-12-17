from collections import Counter
from functools import lru_cache

with open("input") as file:
    data = [int(line) for line in file]

data.append(0)
data.sort()
data.append(data[-1]+3)

#part 1
deltas = [data[i+1] - data[i] for i in range(len(data)-1)]
c = Counter(deltas)
print(c[1] * c[3])

#part 2
@lru_cache(None)
def ways(idx):
    """returns the number of ways that adapters can be arranged to get from zero jolts to the target index"""
    if idx == 0:
        return 1
    #identify all adapters preceding this one that can connect to it
    neighbors = [j for j in range(max(0, idx-3), idx) if data[idx] - data[j] <= 3]
    return sum(ways(x) for x in neighbors)

print(ways(len(data)-1))