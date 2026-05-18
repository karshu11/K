#!/usr/bin/env python3
"""
calculator.py — safe arithmetic evaluator and small CLI.

Supports: +, -, *, /, //, %, **, unary +/-, parentheses and numeric literals.
Does NOT allow names, attribute access, calls, or other unsafe AST nodes.
"""

import ast
import operator as op
import argparse
import sys

# Allowed binary operators
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_UNARY_OPS = {
    ast.UAdd: lambda x: x,
    ast.USub: op.neg,
}


def eval_node(node):
    if isinstance(node, ast.Constant):  # Python 3.8+: numbers
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.Num):  # for older ASTs
        return node.n
    if isinstance(node, ast.BinOp):
        left = eval_node(node.left)
        right = eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    if isinstance(node, ast.Expression):
        return eval_node(node.body)
    # Disallow everything else (calls, names, attributes, etc.)
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def eval_expr(expr: str):
    """Safely evaluate an arithmetic expression and return a number."""
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Invalid expression") from e
    return eval_node(parsed.body)


def main():
    parser = argparse.ArgumentParser(description="Safe calculator (no eval).")
    parser.add_argument("-e", "--expr", help="Evaluate expression and exit")
    args = parser.parse_args()

    if args.expr:
        try:
            result = eval_expr(args.expr)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)
        print(result)
        return

    # REPL mode
    try:
        while True:
            s = input("calc> ").strip()
            if not s:
                continue
            if s in ("quit", "exit"):
                break
            try:
                print(eval_expr(s))
            except Exception as e:
                print("Error:", e)
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
