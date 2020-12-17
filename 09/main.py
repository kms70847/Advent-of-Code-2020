with open("input") as file:
    data = [int(line) for line in file]

#part 1
window_size = 25
for i in range(window_size, len(data)):
    window = [data[j] for j in range(i-window_size, i)]
    sums = {window[x] + window[y] for x in range(window_size) for y in range(x+1, window_size)}
    if data[i] not in sums:
        print(data[i])
        break

#part 2
invalid = data[i]
a = b = 0
while True:
    window = data[a:b]
    if sum(window) == invalid:
        print(min(window) + max(window))
        break
    elif sum(window) < invalid:
        b += 1
    else:
        a += 1

#1869035 -- too low