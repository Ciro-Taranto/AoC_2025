def joltage(line: str, digits: int = 12) -> int:
    numbers = list(line)[::-1]
    current = numbers[:digits]
    current_best = _get_value(current)
    for number in numbers[digits:]:
        if number >= current[-1]:
            best = _select_best_reduced(current)
            candidate = best + [number]
            if (current_value := _get_value(candidate)) >= current_best:
                current_best = current_value
                current = candidate
    return _get_value(current)


def _get_value(current: list[str]) -> int:
    return int("".join(current[::-1]))


def _select_best_reduced(current: list[str]) -> list[str]:
    best = current[1:]
    best_value = _get_value(best)
    for i in range(1, len(current)):
        candidate = current[:i] + current[i + 1 :]
        candidate_value = _get_value(candidate)
        if candidate_value > best_value:
            best_value = candidate_value
            best = candidate
    return best


if __name__ == "__main__":
    from pathlib import Path
    from time import perf_counter

    start = perf_counter()
    with open(Path(__file__).parent / "input.txt", "r") as f:
        lines = f.read().strip().split("\n")
    values = []
    for line in lines:
        values.append(joltage(line, digits=12))
    print(sum(values))
    print(f"Elapsed={perf_counter() - start:2.4f} seconds.")
