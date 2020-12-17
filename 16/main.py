import re

def valid_p1(field):
    return any(l <= field <= r for ranges in rules.values() for l,r in ranges)

def valid(name, value):
    return any(l <= value <= r for l,r in rules[name])

def product(iterable):
    result = 1
    for item in iterable:
        result *= item
    return result

rules = {}
nearbys = []
with open("input") as file:
    mode = "rules"
    for line in file:
        line = line.strip()
        if not line:
            continue
        elif line == "your ticket:":
            mode = "me"
        elif line == "nearby tickets:":
            mode = "nearby"
        elif mode == "rules":
            name, _, rule = line.partition(":")
            ranges = []
            for part in rule.split(" or "):
                l,_,r = part.partition("-")
                ranges.append((int(l), int(r)))
            rules[name] = ranges
        elif mode == "me":
            me = [int(x) for x in line.split(",")]
        elif mode == "nearby":
            nearbys.append([int(x) for x in line.split(",")])
        else:
            raise Exception(f"unknown mode{repr(mode)}")

valid_tickets = []
invalid_total = 0
for ticket in nearbys:
    is_valid = True
    for field in ticket:
        if not valid_p1(field):
            invalid_total += field
            is_valid = False
    if is_valid:
        valid_tickets.append(ticket)
print(invalid_total)

#number of fields in a ticket
num_fields = len(valid_tickets[0])

candidates = [set(rules.keys()) for _ in range(num_fields)]
for ticket in valid_tickets:
    for idx, value in enumerate(ticket):
        for name in list(candidates[idx]): #make a copy to avoid "size changed during iteration" problem
            if not valid(name, value):
                candidates[idx].remove(name)

#if any candidate collection has only one candidate, then remove that name from every other collection.
#hopefully this reduces all collections to a length of one
while True:
    loop_again = False
    for cand in candidates:
        if len(cand) == 1:
            name = list(cand)[0]
            for other in candidates:
                if len(other) > 1 and name in other:
                    other.remove(name)
                    loop_again = True
    if not loop_again:
       break
assert all(len(cand) == 1 for cand in candidates)
fields = [list(cand)[0] for cand in candidates]
print(fields)

print(product(value for field, value in zip(fields, me) if field.startswith("departure")))

12:19