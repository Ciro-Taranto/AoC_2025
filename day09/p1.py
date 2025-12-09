from itertools import combinations


def solve(tiles: list[tuple[int, int]]) -> int:
    max_area = 0
    for t1, t2 in combinations(tiles, 2):
        area = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
        max_area = area if area > max_area else max_area
    return max_area


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    tiles = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    max_area = solve(tiles)

    print(f"The max area is (hopefully): {max_area}")
