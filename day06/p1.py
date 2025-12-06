from typing import Literal
import re

OPERATORS = {"*": int.__mul__, "+": int.__add__}


def solve(problems: list[list[int]], ops: Literal["*", "+"]):
    accumulators = [1 if op == "*" else 0 for op in ops]
    for line in problems:
        for i, (op, number) in enumerate(zip(ops, line)):
            accumulators[i] = OPERATORS[op](accumulators[i], number)
    return accumulators


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        lines = f.read().strip("\n").split("\n")
    problems = []
    for line in lines[:-1]:
        vals = list(map(int, re.findall("\d+", line)))
        problems.append(vals)
    operators = [i for i in lines[-1] if i in "+*"]
    results = solve(problems, operators)
    print(sum(results))
