def try_int(x):
    try:
        return int(x)
    except:
        return x

with open("input") as file:
    estimate = int(next(file))
    buses = [try_int(x) for x in file.read().split(",")]

#part 1
def first_time(bus):
    return ((bus-estimate) % bus)
time, bus = min((first_time(bus), bus) for bus in buses if bus != "x")
print(time*bus)

#part 2

x = 0
delta = 1
for i, bus in enumerate(buses):
    if bus == "x":
        continue
    while (x+i) % bus != 0:
        x += delta
    #use lcm here if not all buses are coprime
    delta *= bus
print(x)