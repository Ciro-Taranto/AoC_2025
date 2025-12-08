from heapq import heappop, heappush
from itertools import combinations

Position = tuple[int, int, int]


def distance(p1: Position, p2: Position) -> int:
    return sum((a - b) ** 2 for a, b in zip(p1, p2))


def sort_pairs(boxes: list[Position]):
    heap = []
    for p1, p2 in combinations(boxes, 2):
        heappush(heap, (distance(p1, p2), (p1, p2)))
    return heap


def solve(boxes: list[Position]) -> tuple[Position, Position]:
    distance_heap = sort_pairs(boxes)
    connections: dict[Position, set[Position]] = {b: {b} for b in boxes}
    while True:
        _, (b1, b2) = heappop(distance_heap)
        merged_circuit = connections[b1].union(connections[b2])
        if len(merged_circuit) == len(boxes):
            return b1, b2
        for b in merged_circuit:
            connections[b] = merged_circuit


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read()
    boxes = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    b1, b2 = solve(boxes)
    print(b1, b2)
    print(f"The solution is (hopefully) = {b1[0] * b2[0]}")
