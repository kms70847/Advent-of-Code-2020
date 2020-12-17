import re
from collections import defaultdict
from functools import lru_cache

#generate a graph of parent-child dependencies
d = defaultdict(dict)
with open("input") as file:
    for line in file:
        color = re.match("(.*?) bags contain", line).group(1)
        for req in re.findall(r"(\d+ .*?) bags?", line):
            amt, _, req_color = req.partition(" ")
            d[color][req_color] = int(amt)

#reverse graph
parents = defaultdict(set)
for parent, req in d.items():
    for child, amt in req.items():
        parents[child].add(parent)

#part 1
#use BFS find the number of ancestors of shiny gold
to_visit = {"shiny gold"}
seen = set()
while to_visit:
    c = to_visit.pop()
    seen.add(c)
    for parent in parents[c]:
        if parent not in seen:
            to_visit.add(parent)
print(len(seen)-1)

#part 2
#use DFS to find the cost of a shiny gold bag.
#todo: detect infinite loops, allow very deep nesting
@lru_cache(None)
def cost(color):
    return 1 + sum(amt*cost(child) for child,amt in d[color].items())
print(cost("shiny gold")-1)