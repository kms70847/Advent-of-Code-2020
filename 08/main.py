with open("input") as file:
    program = []
    for line in file:
        op, arg = line.split()
        program.append((op, int(arg)))

def execute(program):
    """
    execute the given program.
    returns an (acc, reason) tuple. 
        acc is the value of the accumulator.
        reason is either 'loop' or 'success' or 'out of bounds' depending on why the program ended.
    """
    pc = 0
    acc = 0
    seen = set()
    while pc not in seen:
        seen.add(pc)
        if pc == len(program):
            return acc, "success"
        elif pc < 0 or pc > len(program):
            return acc, "out of bounds"
        op, arg = program[pc]
        if op == "nop":
            pass
        elif op == "acc":
            acc += arg
        elif op == "jmp":
            pc += arg - 1 #since we'll increment it after this
        pc += 1
    return acc, "loop"

#part 1
acc, _ = execute(program)
print(acc)

#part 2
for idx, (op, arg) in enumerate(program):
    if op in ("nop", "jmp"):
        new_op = "nop" if op == "jmp" else "jmp"
        program[idx] = (new_op, arg)

        acc, reason = execute(program)
        if reason == "success":
            print(acc)
            break

        program[idx] = (op, arg)
else:
    print("No solution found.")