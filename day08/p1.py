from heapq import heappop, heappush, nsmallest
from itertools import combinations

Position = tuple[int, int, int]


def distance(p1: Position, p2: Position) -> int:
    return sum((a - b) ** 2 for a, b in zip(p1, p2))


def sort_pairs_(boxes: list[Position]):
    heap = []
    for p1, p2 in combinations(boxes, 2):
        heappush(heap, (distance(p1, p2), (p1, p2)))
    return heap


def sort_pairs(boxes: list[Position], max_connections: int = 1000):
    return nsmallest(
        max_connections,
        [(distance(p1, p2), (p1, p2)) for p1, p2 in combinations(boxes, 2)],
    )


def solve(boxes: list[Position], max_connections: int = 1000) -> list[set[Position]]:
    distance_heap = sort_pairs(boxes, max_connections=max_connections)
    connections: dict[Position, set[Position]] = {b: {b} for b in boxes}
    for _ in range(max_connections):
        _, (b1, b2) = heappop(distance_heap)
        merged_circuit = connections[b1].union(connections[b2])
        for b in merged_circuit:
            connections[b] = merged_circuit
    unique_circuits = set()
    for _, circuit in connections.items():
        unique_circuits.add(tuple(sorted(circuit)))
    return sorted(unique_circuits, key=len, reverse=True)


if __name__ == "__main__":
    from functools import reduce
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read()
    boxes = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    circuits = solve(boxes, 1000)
    solution = reduce(int.__mul__, [len(c) for c in circuits[:3]], 1)
    print([len(c) for c in circuits[:3]])
    print(f"The solution is (hopefully) = {solution}")
