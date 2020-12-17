import re
data = []
with open("input") as file:
    all_ids = {int(line.translate(str.maketrans("FLBR","0011")),2) for line in file}

#part 1
print(max(all_ids))

#part 2
for x in all_ids:
    if x+1 not in all_ids and x+2 in all_ids:
        print(x+1)