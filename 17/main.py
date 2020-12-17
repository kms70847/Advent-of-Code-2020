from collections import defaultdict
from itertools import product


def neighbor_coords(pos):
    for delta in product(range(-1,2),repeat=len(pos)):
        if not all(w == 0 for w in delta):
            yield tuple(a+b for a,b in zip(pos, delta))

def neighbor_count(field, pos):
    return sum(int(field[neighbor]) for neighbor in neighbor_coords(pos))

def bbox(field):
    return [f(key[i] for key, value in field.items() if value) for i in range(3) for f in (min, max)]

# def display(field):
    # xmin, xmax, ymin, ymax, zmin, zmax = bbox(field)
    # slices = []
    # for z in range(zmin, zmax+1):
        # rows = []
        # rows.append(f"z={z}")
        # for y in range(ymin, ymax+1):
            # row = []
            # for x in range(xmin, xmax+1):
                # row.append("#" if field[x,y,z] else ".")
            # rows.append("".join(row))
        # slices.append("\n".join(rows))
    # print("\n\n".join(slices))

def tick(field):
    result = defaultdict(bool)
    #only need to examine coordinates one space away from an active cell
    to_visit = set()
    for pos, cell in field.items():
        if cell: to_visit.update(list(neighbor_coords(pos)))
    for pos in to_visit:
        cell = field[pos]
        neighbors = neighbor_count(field, pos)
        new_cell = (cell and neighbors in (2,3)) or (not cell and neighbors==3)
        result[pos] = new_cell
    return result

for dimensions in (3,4):
    field = defaultdict(bool)
    with open("input") as file:
        for y, line in enumerate(file):
            line = line.strip()
            if not line: continue
            for x, c in enumerate(line):
                pos = (x,y) + (0,)*(dimensions-2)
                field[pos] = c == "#"

    for i in range(6):
        field = tick(field)

    print(sum(field.values()))