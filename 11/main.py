import itertools

OCCUPIED = "#"
EMPTY = "L"
FLOOR = "."

DELTAS = [(dx, dy) for dx in range(-1,2) for dy in range(-1,2) if not dx==dy==0]

with open("input") as file:
    data = tuple(line.strip() for line in file)

def p1_tick(data):
    height = len(data)
    width = len(data[0])

    rows = []
    for j in range(height):
        row = []
        for i in range(width):
            neighbors=[data[j+dy][i+dx] for dx,dy in DELTAS if 0 <= i+dx < width and 0 <= j+dy < height]

            state = data[j][i]
            if state == EMPTY and neighbors.count(OCCUPIED) == 0:
                row.append(OCCUPIED)
            elif state == OCCUPIED and neighbors.count(OCCUPIED) >= 4:
                row.append(EMPTY)
            else:
                row.append(state)
        rows.append("".join(row))
    return tuple(rows)

line_of_sight_neighbors = {}
height = len(data)
width = len(data[0])
for j in range(height):
    for i in range(width):
        neighbors = []
        for dx, dy in DELTAS:
            for k in itertools.count(1):
                if not (0 <= i+k*dx < width and 0 <= j+k*dy < height):
                    break
                if data[j+k*dy][i+k*dx] != FLOOR:
                    neighbors.append((i+k*dx, j+k*dy))
                    break
        line_of_sight_neighbors[i,j] = neighbors

def p2_tick(data):
    height = len(data)
    width = len(data[0])

    rows = []
    for j in range(height):
        row = []
        for i in range(width):
            neighbors=[data[y][x] for x,y in line_of_sight_neighbors[i,j]]

            state = data[j][i]
            if state == EMPTY and neighbors.count(OCCUPIED) == 0:
                row.append(OCCUPIED)
            elif state == OCCUPIED and neighbors.count(OCCUPIED) >= 5:
                row.append(EMPTY)
            else:
                row.append(state)
        rows.append("".join(row))
    return tuple(rows)

    
original_data = data

#part 1
while True:
    new_data = p1_tick(data)
    if new_data == data:
        break
    data = new_data

print(sum(row.count(OCCUPIED) for row in data))

#part 2
data = original_data
while True:
    new_data = p2_tick(data)
    if new_data == data:
        break
    data = new_data

print(sum(row.count(OCCUPIED) for row in data))