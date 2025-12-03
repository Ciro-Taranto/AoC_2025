def joltage(line: str) -> int:
    if not line:
        return 0
    numbers = list(line)
    candidates = sorted(numbers, reverse=True)[:2]
    if candidates[0] == candidates[1]:
        return int("".join(candidates))
    i0 = numbers.index(candidates[0])
    i1 = numbers.index(candidates[1])
    if i0 < i1 or len(line) == 2:
        return int(candidates[0] + candidates[1])
    elif i0 == len(line) - 1:
        return int(candidates[1] + candidates[0])
    else:
        return max(int(candidates[1] + candidates[0]), joltage(line[i0:]))


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        lines = f.read().strip().split("\n")
    values = []
    for line in lines:
        values.append(joltage(line))
        print(values[-1])
    print(sum(values))
