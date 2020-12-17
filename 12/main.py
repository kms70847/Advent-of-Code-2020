import re

def try_int(x):
    try:
        return int(x)
    except:
        return x

data = []
with open("input") as file:
    for line in file:
        data.append(list(map(try_int, re.match("(\w)(\d+)", line).groups())))

I = 1j
directions = {c: I**i for i, c in enumerate("ENWS")}

#part 1
pos = 0+0j
facing = 1+0j
for op, arg in data:
    if op in directions:
        pos += directions[op] * arg
    elif op == "F":
        pos += facing * arg
    elif op == "L":
        facing *= I ** (arg//90)
    elif op == "R":
        facing *= I ** (4-arg//90) #does this work?
    else:
        raise Exception(f"Unknown arg {op}")

print(int(abs(pos.real)+abs(pos.imag)))

#part 2
pos = 0+0j
waypoint = 10+1j
for op, arg in data:
    if op in directions:
        waypoint += directions[op] * arg
    elif op == "F":
        pos += waypoint * arg
    elif op == "L":
        waypoint *= I ** (arg//90)
    elif op == "R":
        waypoint *= I ** (4-arg//90)
    else:
        raise Exception(f("Unknown arg {op}"))

print(int(abs(pos.real)+abs(pos.imag)))