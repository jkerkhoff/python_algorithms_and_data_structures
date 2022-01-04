"""Edsger Dijkstra's shunting yard algorithm for parsing infix expressions."""

import operator

# TODO: make more generic and clean

DIGITS = "0123456789"
OPS = "+-*/"

precedence = {"+": 0, "-": 0, "*": 1, "/": 1}
op_map = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda a, b: a // b if a * b >= 0 else -(abs(a) // abs(b))
}


def parse_infix(expr: str) -> list[str]:
    out = []
    op_stack = []

    n = len(expr)
    i = 0
    while i < n:
        if expr[i] in DIGITS:
            j = i + 1
            while j < n and expr[j] in DIGITS:
                j += 1
            out.append(expr[i:j])
            i = j - 1
        elif expr[i] in OPS:
            while op_stack and op_stack[-1] != "(" and precedence[
                    op_stack[-1]] >= precedence[expr[i]]:
                out.append(op_stack.pop())
            op_stack.append(expr[i])
        elif expr[i] == "(":
            op_stack.append("(")
        elif expr[i] == ")":
            while op_stack[-1] != "(":
                out.append(op_stack.pop())
            op_stack.pop()

        i += 1

    out.extend(op_stack[::-1])
    return out
