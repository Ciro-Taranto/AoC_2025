from typing import Literal
import re
from functools import reduce

OPERATORS = {"*": int.__mul__, "+": int.__add__}


def solve(input_: str) -> list[int]:
    lines = input_.strip().split("\n")
    operations = []
    for i, char in enumerate(lines[-1]):
        if char in "*+":
            operations.append((i, char))
    operations.append((max([len(line) for line in lines]) + 1, None))
    solutions = []
    for (start_position, operation), (end_position, _) in zip(
        operations[:-1], operations[1:]
    ):
        values = []
        for position in range(end_position - 2, start_position - 1, -1):
            value = 0
            for line in lines[:-1]:
                if line[position] != " ":
                    value *= 10
                    value += int(line[position])
            values.append(value)
        solutions.append(
            reduce(OPERATORS[operation], values, 0 if operation == "+" else 1)
        )
    return solutions


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read()
    print(sum(solve(input_)))
