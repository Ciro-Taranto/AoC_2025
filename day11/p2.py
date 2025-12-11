from __future__ import annotations


def parse(input_: str) -> dict[str, set[str]]:
    circuit = {}
    for line in input_.lstrip().split("\n"):
        parent, children = line.strip().split(":")
        children = children.strip(" ").split(" ")
        circuit[parent] = set(children)
    return circuit


def dfs(
    circuit: dict[str, set[str]],
    start: str,
    end: str,
    cache: dict[tuple[str, str], int],
) -> int:
    if (start, end) in cache:
        return cache[(start, end)]
    if start == end:
        return 1
    possibilities = sum(
        [dfs(circuit, node, end, cache) for node in circuit.get(start, {})]
    )
    cache[(start, end)] = possibilities
    return possibilities


def server_to_out(circuit: dict[str, set[str]]) -> int:
    cache = {}
    server_to_fft = dfs(circuit, "svr", "fft", cache)
    server_to_dac = dfs(circuit, "svr", "dac", cache)
    if server_to_fft < server_to_dac:
        fft_to_dac = dfs(circuit, "fft", "dac", cache)
        dac_to_out = dfs(circuit, "dac", "out", cache)
        total = server_to_fft * fft_to_dac * dac_to_out
    else:
        dac_to_fft = dfs(circuit, "dac", "fft", cache)
        fft_to_out = dfs(circuit, "fft", "out", cache)
        total = server_to_dac * dac_to_fft * fft_to_out
    print(f"Found {total} paths")
    return total


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    circuit = parse(input_)
    server_to_out(circuit)
