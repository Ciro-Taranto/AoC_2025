from bisect import bisect_left
from itertools import combinations
from heapq import heapify, heappop

Position = tuple[int, int]


def compute_area(t1: Position, t2: Position) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def check_no_vertex_inside(
    t1: Position,
    t2: Position,
    sorted_tiles: list[Position],
    neighbors: dict[Position, tuple[Position, Position]],
) -> bool:
    min_x, max_x = (t1[0], t2[0]) if t2[0] >= t1[0] else (t2[0], t1[0])
    min_y, max_y = (t1[1], t2[1]) if t2[1] >= t1[1] else (t2[1], t1[1])
    lo = bisect_left(sorted_tiles, (min_x, 0))
    hi = bisect_left(sorted_tiles, (max_x, 10**10))
    for t in sorted_tiles[lo:hi]:
        if t in {t1, t2}:
            continue
        if min_x < t[0] < max_x and min_y < t[1] < max_y:
            return False

        p, n = neighbors[t]
        if {p, n} == {t1, t2}:
            continue
        if t[0] == min_x and max(p[0], n[0]) > min_x:
            return False
        elif t[0] == max_x and min(p[0], n[0]) < max_x:
            return False

        if t[1] == min_y and max(p[1], n[1]) > min_y:
            return False
        elif t[1] == max_y and min(p[1], n[1]) < max_x:
            return False
    return True


def solve(tiles: list[tuple[int, int]]) -> int:
    neighbors = {tiles[0]: (tiles[1], tiles[-1]), tiles[-1]: (tiles[0], tiles[-2])}
    for l, m, r in zip(tiles[:-2], tiles[1:-1], tiles[2:]):
        neighbors[m] = (l, r)
    tiles = sorted(tiles)
    possible_squares = [
        (-compute_area(t1, t2), (t1, t2)) for t1, t2 in combinations(tiles, 2)
    ]
    heapify(possible_squares)
    while possible_squares:
        area, (t1, t2) = heappop(possible_squares)
        if check_no_vertex_inside(t1, t2, tiles, neighbors):
            return -area
    raise ValueError("should not reach")


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    tiles = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    max_area = solve(tiles)

    print(f"The max area is (hopefully): {max_area}")
