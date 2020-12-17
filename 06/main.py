groups = []
with open("input") as file:
    for group in file.read().strip().split("\n\n"):
        groups.append([set(line) for line in group.split("\n")])

#print(sum(len(set.union(*group)) for group in groups))
print(sum(len(set.intersection(*group)) for group in groups))
#3188 - too low