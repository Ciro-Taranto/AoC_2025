from itertools import product

Position = tuple[int, int]


def is_accessible(position: tuple[int, int], positions: set[Position]) -> bool:
    x, y = position
    n = 0
    for dx, dy in product(range(-1, 2), range(-1, 2)):
        if (x + dx, y + dy) in positions:
            n += 1
    # Note: we know that (x, y) is in positions so instead of < 4 we do <= 4.
    return n <= 4


def all_accessible(positions: set[Position]) -> set[Position]:
    return {position for position in positions if is_accessible(position, positions)}


def remove_rolls(positions: set[Position]) -> set[Position]:
    while can_be_removed := all_accessible(positions):
        print(f"Removing {len(can_be_removed)} rolls.")
        positions = positions.difference(can_be_removed)
    return positions


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    positions = set()
    for y, line in enumerate(input_.split("\n")):
        for x, char in enumerate(line):
            if char == "@":
                positions.add((x, y))
    n_original_rolls = len(positions)
    final_rolls = remove_rolls(positions)
    print(f"Removed: {n_original_rolls - len(final_rolls)} rolls of paper.")
