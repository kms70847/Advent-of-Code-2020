import re

full_mask = (2**37) - 1
def apply_mask_v1(mask, value):
    for i, bitmask in enumerate(mask[::-1]):
        if bitmask == "1":
            value |= 1 << i
        elif bitmask == "0":
            value &= full_mask ^ (1 << i)
        else:
            pass
    return value

def apply_mask_v2(mask, value):
    def iter_possible_masks(mask):
        if mask.count("X") == 0:
            yield int(mask, 2)
        else:
            for c in "01":
                yield from iter_possible_masks(mask.replace("X", c, 1))
    value = f"{value:036b}"
    mask = "".join({"0":v,"1":"1","X":"X"}[m] for m,v in zip(mask,value))
    yield from iter_possible_masks(mask)

with(open("input")) as file:
    program = [line.strip() for line in file]


for part in (1,2):
    mask = None
    mem = {}
    for line in program:
        if m := re.match("mask = ([01X]{36})", line):
            #store mask in reverse so it's easier to enumerate later
            mask = m.group(1)
        elif m := re.match(r"mem\[(\d+)\] = (\d+)", line):
            addr, value = map(int, m.groups())
            if part == 1:
                value = apply_mask_v1(mask, value)
                mem[addr] = value
            else:
                for masked_addr in apply_mask_v2(mask, addr):
                    mem[masked_addr] = value
    print(sum(mem.values()))