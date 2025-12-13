from ortools.sat.python import cp_model
from itertools import product
from collections import defaultdict

Shape = set[tuple[int, int]]


def parse(
    input_: str,
) -> tuple[list[Shape], tuple[int, int], list[list[int]]]:
    input_ = input_.strip()
    shapes = []
    for block in input_.split("\n\n")[:-1]:
        shape = set()
        for i, line in enumerate(block.split("\n")[1:]):
            for j, char in enumerate(line):
                if char == "#":
                    shape.add((i, j))
        shapes.append(shape)

    sizes = []
    allocations = []
    for line in input_.split("\n\n")[-1].strip().split("\n"):
        size, allocation = line.split(":")
        sizes.append(list(map(int, size.split("x"))))
        allocations.append(list(map(int, allocation.lstrip().strip().split(" "))))
    return shapes, sizes, allocations


def rotate(shape: Shape) -> Shape:
    rotated = {(-j, i) for i, j in shape}
    return normalize(rotated)


def normalize(shape: Shape) -> Shape:
    min_x = min(i for i, _ in shape)
    min_y = min(i for _, i in shape)
    return {(i - min_x, j - min_y) for i, j in shape}


def flip_h(shape: Shape) -> Shape:
    flipped = {(-x, y) for x, y in shape}
    return normalize(flipped)


def flip_v(shape: Shape) -> Shape:
    flipped = {(x, -y) for x, y in shape}
    return normalize(flipped)


def get_all_shape_variations(shape: Shape) -> list[Shape]:
    curr = shape
    variations = []
    for _ in range(4):
        curr = rotate(curr)
        if curr not in variations:
            variations.append(curr)
    curr = flip_h(shape)
    for _ in range(4):
        curr = rotate(curr)
        if curr not in variations:
            variations.append(curr)
    curr = flip_v(shape)
    for _ in range(4):
        curr = rotate(curr)
        if curr not in variations:
            variations.append(curr)
    return variations


def check_feasibility(
    shapes: dict[int, list[Shape]], size: tuple[int, int], allocation: list[int]
) -> bool:
    if len(shapes) != len(allocation):
        raise ValueError
    if set(shapes) != set(range(len(allocation))):
        raise ValueError

    placements = []  # list of (shape_name, cells)

    for shape, variants in shapes.items():
        for variant in variants:
            max_x = max(x for x, _ in variant)
            max_y = max(y for _, y in variant)

            for x_off, y_off in product(
                range(size[0] - max_x + 1), range(size[1] - max_y + 1)
            ):
                cells = [(x_off + x, y_off + y) for x, y in variant]
                placements.append((shape, cells))

    model = cp_model.CpModel()
    # one boolean variable for each possible placement:
    # it is either there or not
    shape_to_variables = {i: [] for i in shape_variants}
    cell_to_variables = defaultdict(list)
    for i, (shape, cells) in enumerate(placements):
        x = model.NewBoolVar(f"p{i}")
        shape_to_variables[shape].append(x)
        for cell in cells:
            cell_to_variables[cell].append(x)

    for shape, variables in shape_to_variables.items():
        model.Add(sum(variables) == allocation[shape])

    for _, vars in cell_to_variables.items():
        model.Add(sum(vars) <= 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60  # optional limit

    res = solver.Solve(model)

    if res == cp_model.OPTIMAL or res == cp_model.FEASIBLE:
        print("Feasible arrangement found!\n")
        return True
        # grid = [["." for _ in range(GRID_W)] for _ in range(GRID_H)]
        # for i, (shape, cells) in enumerate(placements):
        #     if solver.Value(x[i]):
        #         for r, c in cells:
        #             grid[r][c] = shape[0]

        # for row in grid:
        #     print(" ".join(row))

    else:
        print("No feasible placement exists.")
        return False


if __name__ == "__main__":
    from pathlib import Path
    from tqdm import tqdm

    input_ = Path(__file__).with_name("input.txt").open().read()
    shapes, sizes, allocations = parse(input_)
    shape_variants = {
        i: get_all_shape_variations(shape) for i, shape in enumerate(shapes)
    }
    feasible = 0
    for size, allocation in tqdm(zip(sizes, allocations, strict=True)):
        feasible += int(check_feasibility(shape_variants, size, allocation))
    print(f"Feasible={feasible}")
