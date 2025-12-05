from itertools import product
from collections import defaultdict
from functools import reduce

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
        # print(f"Removing {len(can_be_removed)} rolls.")
        positions = positions.difference(can_be_removed)
    return positions


def remove_rolls_v2(positions: set[Position]) -> set[Position]:
    neighbors = defaultdict(set)
    rolls_by_connectivity = defaultdict(set)
    for x, y in positions:
        for dx, dy in product(range(-1, 2), range(-1, 2)):
            if (neighbor := (x + dx, y + dy)) in positions and (dx or dy):
                neighbors[(x, y)].add(neighbor)
        if not neighbors[(x, y)]:
            rolls_by_connectivity[0].add((x, y))
    for roll, roll_neighbors in neighbors.items():
        rolls_by_connectivity[len(roll_neighbors)].add(roll)
    removable = reduce(set.union, [rolls_by_connectivity[n] for n in range(0, 4)])
    while removable:
        rolls_by_connectivity = {
            k: v if k >= 4 else set() for k, v in rolls_by_connectivity.items()
        }
        for roll in removable:
            for next_roll in neighbors[roll]:
                n = len(neighbors[next_roll])
                neighbors[next_roll].remove(roll)
                if n >= 4:
                    rolls_by_connectivity[n].remove(next_roll)
                    rolls_by_connectivity[n - 1].add(next_roll)
        removable = reduce(set.union, [rolls_by_connectivity[n] for n in range(0, 4)])
    return reduce(set.union, rolls_by_connectivity.values())


if __name__ == "__main__":
    from pathlib import Path
    from time import perf_counter

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    start = perf_counter()
    positions = set()
    for y, line in enumerate(input_.split("\n")):
        for x, char in enumerate(line):
            if char == "@":
                positions.add((x, y))
    n_original_rolls = len(positions)
    final_rolls = remove_rolls(positions)
    print(f"Removed: {n_original_rolls - len(final_rolls)} rolls of paper.")
    print(f"Elapsed {perf_counter() - start:2.4f} seconds.")
    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    start = perf_counter()
    positions = set()
    for y, line in enumerate(input_.split("\n")):
        for x, char in enumerate(line):
            if char == "@":
                positions.add((x, y))
    final_rolls = remove_rolls_v2(positions)
    print(f"Removed: {n_original_rolls - len(final_rolls)} rolls of paper.")
    print(f"Elapsed {perf_counter() - start:2.4f} seconds.")
