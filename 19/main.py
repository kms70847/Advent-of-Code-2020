import copy

def parse(rule):
    """translate a string rule into an equivalent AST"""
    if len(rule) == 3 and rule.startswith('"') and rule.endswith('"'):
        return ("literal", rule[1])
    elif "|" in rule:
        return ("or", [parse(s) for s in rule.split(" | ")])
    elif " " in rule:
        return ("and", [parse(s) for s in rule.split()])
    elif rule.isdigit:
        return ("ref", rule)

def compile(rules, start):
    """
    compile the ruleset into an assembly-like language that supports forking
    `start` is the key of the rule acting as the entry point.
    """
    
    """
    mini language specification. A program is a series of operators with one or more arguments.
    There are two registers, neither of which are directly accessible by the user.
        pc - the index of the operator that is currently executing.
        acc - the index of the character in the input currently being examined.
    oprator listing:
        jump addr: set pc to addr.
        call addr: push pc onto the call stack and jump to addr.
        ret: pop the top of the call stack into pc
        fork addr1, addr2, ...: create N copies of the program state, and have each thread jump to a respective address.
        expect str: if the current input matches the str, increment acc. Otherwise, terminate with a failure code.
        exit: terminate with a success code.
        label name: no-op. Used as alternative names for addresses in call/jump/fork calls.
    """

    _unique_label_id = 0
    def unique_label_name():
        """generate a unique label name guaranteed not to collide with any other names in the program, including ones not generated yet"""
        nonlocal _unique_label_id
        _unique_label_id += 1
        return f"u{_unique_label_id}"
    def literalize(op, label_addrs):
        """replace any labels in the given operators with their logical addresses"""
        if op[0] in ("call", "jump"):
            return (op[0], label_addrs[op[1]])
        elif op[0] == "fork":
            return ("fork", [label_addrs[label] for label in op[1]])
        else:
            return op
    def _compile(rule):
        """recursively compile a rule and append it to the program."""
        assert len(rule)==2, f"rule has unexpected shape: {rule}"
        name, value = rule
        if name == "literal":
            program.append(("expect", value))
        elif name == "and":
            for child in value:
                _compile(child)
        elif name == "or":
            label_names = [unique_label_name() for _ in range(len(value))]
            fork_done_label = unique_label_name()
            program.append(("fork", label_names))
            for child, label in zip(value, label_names):
                program.append(("label", label))
                _compile(child)
                program.append(("jump", fork_done_label)) #not strictly necessary for final case
            program.append(("label", fork_done_label))
        elif name == "ref":
            program.append(("call", value))
        else:
            raise Exception(f"Unrecognized rule name {name}")
    program = [("call", start), ("exit",)]
    for key, rule in rules.items():
        program.append(("label", key))
        _compile(rule)
        program.append(("ret",))

    #replace all labels with literal addresses
    label_addrs = {}
    literal_program = []
    for op in program:
        if op[0] == "label":
            label_addrs[op[1]] = len(literal_program)
        else:
            literal_program.append(op)
    literal_program = [literalize(op, label_addrs) for op in literal_program]
    return literal_program

def tick(state, input):
    """
    execute one operation for the current execution state, and return one or more resulting states as a list.
    the input state may be mutated.
    """
    assert state["exit"] is None
    op = program[state["pc"]]
    #print(state, op)
    if op[0] == "jump":
        state["pc"] = op[1]
    elif op[0] == "call":
        state["stack"].append(state["pc"])
        state["pc"] = op[1]
    elif op[0] == "ret":
        state["pc"] = state["stack"].pop() + 1
    elif op[0] == "fork":
        results = []
        for addr in op[1]:
            new_state = copy.deepcopy(state)
            new_state["pc"] = addr
            results.append(new_state)
        return results
    elif op[0] == "expect":
        c = op[1]
        assert len(c) == 1, "expect not implemented for strings longer than one character"
        if state["acc"] < len(input) and input[state["acc"]] == c:
            state["acc"] += 1
            state["pc"] += 1
        else:
            state["exit"] = 0
    elif op[0] == "exit":
        state["exit"] = 1
    elif op[0] == "label":
        raise Exception("Can't execute program with nonliteral addresses")
    else:
        raise Exception(f("Unrecognized operator {op}"))
    #everything but `fork` mutates and returns the input state as a one element list
    return [state]

def run(program, input):
    """
    run the program on the given input.
    return True if any thread exits with a success code. Return False otherwise.
    """
    state = {"stack": [], "pc": 0, "acc": 0, "exit": None}
    states = [state]
    t = 0
    while states:
        #print(f"t={t}. {len(states)} total thread(s).")
        #for state in states: print(state, program[state["pc"]])
        states = [next_state for state in states for next_state in tick(state, input)]
        if any(state["exit"] == 1 for state in states):
            return True
        states = [state for state in states if state["exit"] is None]
    return False

def show(program):
    """display the program's source code"""
    for idx, op in enumerate(program):
        if op[0] == "label":
            if not op[1].startswith("u"):
                print("")
            print(op[1]+ ":")
        elif op[0] == "fork":
            print(f"{idx:03} fork " + ", ".join(str(addr) for addr in op[1]))
        else:
            print(f"{idx:03} " + " ".join(str(arg) for arg in op))

rules = {}
messages = []
with open("input") as file:
    for line in file:
        line = line.strip()
        if not line: continue
        if ":" in line:
            key, _, rule = line.partition(": ")
            rules[key] = parse(rule)
        else:
            messages.append(line)

rules["start"] = ("and", [("ref", "0"), ("literal", "$")])
for part in (1,2):
    if part == 2:
        rules["8"] = parse("42 | 42 8")
        rules["11"] = parse("42 31 | 42 11 31")
    program = compile(rules, "start")
    valid = lambda s: run(program, s+"$")
    print(sum(run(program, message+"$") for message in messages))