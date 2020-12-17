from geometry import Point

def product(iter):
    result = 1
    for item in iter:
        result *= item
    return result

with open("input") as file:
    field = file.read().split()
width = len(field[0])

def treecount(slope):
    total = 0
    pos = Point(0,0)
    while pos.y < len(field):
        if field[pos.y][pos.x%width] == "#":
            total += 1
        pos += slope
    return total

#part 1
print(treecount(Point(3,1)))

#part 2
slopes = (Point(1,1), Point(3,1), Point(5,1), Point(7,1), Point(1,2))
print(product(treecount(slope) for slope in slopes))