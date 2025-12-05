def check_naive_fresh(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    """
    This is the most naive solution.
    Scales like n_ingredients * n_ranges

    Proper solution:
    merge and sort ranges
    use bisect

    n_ingredients * log(n_ranges)

    only marginally faster if sorting ingredients and shortening
    list of ranges
    """
    for low, high in ranges:
        if low <= ingredient <= high:
            return True
    return False


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        ranges_str, ingredients_str = f.read().strip().split("\n\n")
    ranges = []
    for line in ranges_str.split("\n"):
        low, high = line.split("-")
        ranges.append((int(low), int(high)))
    ingredients = list(map(int, ingredients_str.split("\n")))
    n_fresh = sum([check_naive_fresh(ingredient, ranges) for ingredient in ingredients])
    print(f"I found {n_fresh} fresh ingredients.")
