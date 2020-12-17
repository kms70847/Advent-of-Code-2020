with open("input") as file:
    data = [int(line) for line in file]

nums = set(data)

def p1():
    for x in data:
        if 2020-x in data:
            return x * (2020-x)

def p2():
    for x in data:
        for y in data:
            if 2020-x-y in data:
                return x * y * (2020-x-y)

print(p1())
print(p2())                