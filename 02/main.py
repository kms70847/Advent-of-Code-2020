import re

def try_int(x):
    try:
        return int(x)
    except:
        return x

def iter_file():
    """yields (a,b, char, password) collections from the input file."""
    pattern = re.compile("(\d+)-(\d+) (.): (\w+)")
    with open("input") as file:
        for line in file:
            if m := pattern.match(line):
                yield [try_int(x) for x in m.groups()]
            else:
                raise Exception(f"Can't parse line: {repr(line)}")


#part 1
num_valid = 0
for a, b, char, password in iter_file():
    if a <= password.count(char) <= b:
        num_valid += 1
print(num_valid)

#part 2
num_valid = 0
for a, b, char, password in iter_file():
    if (password[a-1] == char) ^ (password[b-1] == char):
        num_valid += 1
print(num_valid)