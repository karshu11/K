# K — Safe Arithmetic Calculator

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

K is a small, secure command-line calculator implemented in Python. It safely evaluates arithmetic expressions (no eval, no arbitrary code execution) and provides a lightweight REPL and a one-shot expression mode.

Why use K?
- Safe: parses expressions with Python's AST and only allows a small, well-defined set of nodes and operators.
- Small and dependency-free: single-file implementation with no external packages.
- User-friendly: one-shot CLI mode and interactive REPL with simple controls.

Features
- Supported operators: +, -, *, /, //, %, **
- Unary operators: +, -
- Parentheses and numeric literals (int and float)
- One-shot evaluation: `-e` / `--expr`
- Interactive REPL fallback (type `exit` or `quit` to leave)

Quick example
```bash
$ python3 calculator.py -e "2 + 3 * 4"
14
$ python3 calculator.py -e "2 ** 10"
1024
```

Interactive REPL
```text
$ python3 calculator.py
calc> (1 + 2) * 3
9
calc> -5 + 2
-3
calc> exit
$
```

Security & design notes
- No eval(): expressions are parsed with ast.parse(..., mode="eval") and only these AST node types are allowed: Constant/Num, BinOp, UnaryOp, and Expression body traversal. Names, attribute access, calls, comprehensions, and other potentially unsafe nodes are rejected.
- Booleans currently evaluate as numbers (True == 1). If you prefer to reject booleans explicitly, that can be changed.
- The evaluator does not limit numeric size or exponentiation depth — extremely large computations may use significant memory/CPU. Consider adding limits for production use.

Installation
- Clone the repo and run with your system Python (3.8+ recommended):
```bash
git clone https://github.com/karshu11/K.git
cd K
python3 calculator.py
```

Command-line options
- -e, --expr: Evaluate an expression and exit
- No args: starts interactive REPL

Examples
```bash
# one-shot:
python3 calculator.py -e "10 // 3"
# interactive:
python3 calculator.py
calc> 10 % 3
1
```

Ideas for improvements
- Exclude bool values explicitly from numeric literals.
- Add a max exponent or integer size guard to avoid resource exhaustion.
- Optional whitelist for a few math functions/constants (e.g. sqrt, pi) with safe calling.
- Add command history (readline) and unit tests (pytest) with edge-case coverage.

Contributing
- Bug reports, suggestions and pull requests are welcome!
- To contribute: fork the repo, make your change in a branch, and open a PR explaining the change.

License
- MIT License. See LICENSE file (or ask me to add one).

Author
- karshu11 — small, safe calculator tool

Enjoy — and tell me if you'd like me to commit this README.md into your repository.
