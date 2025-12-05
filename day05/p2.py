from collections import deque


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    sorted_ranges = deque(sorted(ranges))
    merged_ranges = []
    while sorted_ranges:
        low, high = sorted_ranges.popleft()
        while sorted_ranges and sorted_ranges[0][0] <= high:
            _, next_high = sorted_ranges.popleft()
            high = max(high, next_high)
        merged_ranges.append((low, high))
    return merged_ranges


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        ranges_str, _ = f.read().strip().split("\n\n")
    ranges = []
    for line in ranges_str.split("\n"):
        low, high = line.split("-")
        ranges.append((int(low), int(high)))
    print(len(ranges))
    ranges = merge_ranges(ranges)
    print(len(ranges))
    total_fresh_ingredients = sum([high - low + 1 for low, high in ranges])
    print(f"I have found {total_fresh_ingredients} fresh ingredients.")
