from collections import deque


class ManualLine:
    def __init__(self, pattern: str, toggles: list[list[int]], joltages: list[int]):
        self.pattern = tuple([True if char == "#" else False for char in pattern])
        self.joltages = joltages
        self.toggles = []
        for toggle in toggles:
            binary_toggle = [i in toggle for i, _ in enumerate(self.pattern)]
            self.toggles.append(binary_toggle)

    def turn_on(self) -> int:
        start = tuple([False for _ in self.pattern])
        visited = {start}
        frontier = deque([(0, start)])
        while frontier:
            steps, state = frontier.popleft()
            if state == self.pattern:
                return steps
            for toggle in self.toggles:
                next_state = tuple([a != b for a, b in zip(state, toggle)])
                if next_state not in visited:
                    frontier.append((steps + 1, next_state))
                    visited.add(next_state)
        raise ValueError("Should not reach.")


if __name__ == "__main__":
    import re
    from pathlib import Path
    from tqdm import tqdm

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read()

    light_pattern = re.compile(r"\[([\.\#]+)\]")
    toggles_pattern = re.compile(r"\(([\d,]+)\)")
    joltage_pattern = re.compile(r"\{([\d,]+)\}")
    manuals: list[ManualLine] = []
    for line in input_.split("\n"):
        lights = light_pattern.findall(line)[0]
        toggles = toggles_pattern.findall(line)
        toggles = [list(map(int, toggle.split(","))) for toggle in toggles]
        joltages = joltage_pattern.findall(line)[0]
        joltages = list(map(int, joltages.split(",")))
        manuals.append(ManualLine(lights, toggles, joltages))
    solutions = []
    for manual in tqdm(manuals):
        solutions.append(manual.turn_on())
    print(f"The total button pushes is: {sum(solutions)}")
