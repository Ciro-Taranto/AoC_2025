from itertools import product

Position = tuple[int, int]


def can_be_accessed(position: tuple[int, int], positions: set[Position]) -> bool:
    x, y = position
    n = 0
    for dx, dy in product(range(-1, 2), range(-1, 2)):
        if (x + dx, y + dy) in positions:
            n += 1
    # Note: we know that (x, y) is in positions so instead of < 4 we do <= 4.
    return n <= 4


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    positions = set()
    for y, line in enumerate(input_.split("\n")):
        for x, char in enumerate(line):
            if char == "@":
                positions.add((x, y))
    print(len(positions))
    print(sum([can_be_accessed(position, positions) for position in positions]))
