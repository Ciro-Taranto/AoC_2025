from math import ceil, log10


def check_valid(pair: str) -> list[int]:
    valid = []
    low, high = pair.split("-")
    digits = ceil(len(low) / 2)
    low, high = int(low), int(high)
    left = low // (10**digits)
    current = left * 10**digits + left
    while current <= high:
        if current > 0 and ceil(log10(current)) % 2 == 0 and current >= low:
            valid.append(current)
        left += 1
        digits = ceil(
            log10(left) + 1e-10
        )  # 1e-10 is for the case that left is a power of ten
        current = left * 10**digits + left
    return valid


def check_valid_p2_bf(pair: str) -> list[int]:
    """
    Brute forcing it, but I am sure one does not actually need to check all the numbers.
    This could be done the other way round. Checking for each possible number of digits,
    and creating only the valid combinations with 1, 2, ... n digits.
    """
    valid = set()
    low, high = pair.split("-")
    low, high = int(low), int(high)
    for value in range(low, high + 1):
        n_digits = int(ceil(log10(value)))
        for sequence_len in range(1, n_digits // 2 + 1):
            if n_digits % sequence_len == 0:
                pattern = value % 10**sequence_len
                candidate = sum(
                    pattern * 10 ** (j * sequence_len)
                    for j in range(n_digits // sequence_len)
                )
                if candidate == value:
                    valid.add(candidate)
    return valid


def check_valid_p2(low: int, high: int) -> set[int]:
    """
    Brute forcing it, but I am sure one does not actually need to check all the numbers.
    This could be done the other way round. Checking for each possible number of digits,
    and creating only the valid combinations with 1, 2, ... n digits.
    """
    valid = set()
    min_digits, max_digits = ceil(log10(low) + 1e-9), ceil(log10(high) + 1e-9)
    if max_digits > min_digits:
        return check_valid_p2(low, 10**min_digits - 1).union(
            check_valid_p2(10**min_digits, high)
        )
    low, high = int(low), int(high)
    digits = min_digits
    for sequence_len in range(1, digits // 2 + 1):
        start_pattern = low // 10 ** (digits - sequence_len)
        end_pattern = high // 10 ** (digits - sequence_len)
        for pattern in range(start_pattern, end_pattern + 1):
            candidate = sum(
                pattern * 10 ** (j * sequence_len)
                for j in range(digits // sequence_len)
            )
            if low <= candidate <= high:
                valid.add(candidate)
    return valid


if __name__ == "__main__":
    from pathlib import Path
    from time import perf_counter

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    valid = []
    valid_part_2 = set()
    vp2 = set()
    start = perf_counter()
    # for i, pair in enumerate(input_.split(",")):
    #     valid.extend(check_valid(pair))
    # print(f"Elapsed {perf_counter() - start:2.4f} seconds")
    # start = perf_counter()
    # for i, pair in enumerate(input_.split(",")):
    #     valid_part_2 = valid_part_2.union(set(check_valid_p2_bf(pair)))
    # print(f"Elapsed {perf_counter() - start:2.4f} seconds")
    start = perf_counter()
    for pair in input_.split(","):
        v1, v2 = pair.split("-")
        v1, v2 = int(v1), int(v2)
        vp2 = vp2.union(check_valid_p2(v1, v2))
    print(f"Elapsed {perf_counter() - start:2.4f} seconds")

    # print(sum(valid))
    # print(sum(valid_part_2))
    print(sum(vp2))
