import re
import ast

def compile(tokens):
    result = []
    while tokens:
        token = tokens.pop(0)
        if token == ")":
            break
        elif token == "(":
            result.append(compile(tokens))
        elif token.isdigit():
            result.append(int(token))
        elif token in "*+":
            result.append(token)
        else:
            raise Exception(f"Unrecognized token {token}")
    return result

def run(tree):
    if isinstance(tree, int):
        return tree
    while len(tree) > 1:
        l, op, r = tree.pop(0), tree.pop(0), tree.pop(0)
        op = {"*": lambda a,b: a*b, "+": lambda a,b: a+b}[op]
        value = op(run(l),run(r))
        tree.insert(0, value)
    return tree[0]

def eval(s):
    tokens = re.findall(r"\d+|\*|\+|\(|\)", s)
    tree = compile(tokens)
    return run(tree)

def eval_p2(s):
    def _run(node):
        if isinstance(node, ast.Expression):
            return _run(node.body)
        elif isinstance(node, ast.BinOp):
            op = (lambda a,b: a*b) if isinstance(node.op, ast.Add) else (lambda a,b: a+b)
            return op(_run(node.left), _run(node.right))
        elif isinstance(node, ast.Constant):
            return node.value
        else:
            raise Exception(f"Not yet implemented for node type {type(node)}")
    s = s.replace("+", "?").replace("*","+").replace("?","*")
    expr = ast.parse(s, mode="eval")
    return _run(expr)

with open("input") as file:
    data = [line.strip() for line in file if line.strip()]
print(sum(eval(s) for s in data))
print(sum(eval_p2(s) for s in data))