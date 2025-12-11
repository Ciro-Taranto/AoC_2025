from __future__ import annotations
from collections import deque


def parse(input_: str) -> dict[str, set[str]]:
    circuit = {}
    for line in input_.split("\n"):
        parent, children = line.strip().split(":")
        children = children.strip(" ").split(" ")
        circuit[parent] = set(children)
    return circuit


def you_to_out(circuit: dict[str, set[str]]) -> int:
    paths = 0
    frontier = deque(["you"])
    while frontier:
        node = frontier.popleft()
        if node == "out":
            paths += 1

        for next_node in circuit.get(node, set()):
            frontier.append(next_node)
    return paths


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()
    circuit = parse(input_)
    print(you_to_out(circuit))
