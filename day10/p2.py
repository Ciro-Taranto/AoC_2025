from collections import deque
from heapq import heappop, heappush
from copy import deepcopy
from ortools.linear_solver import pywraplp


class ManualLine:
    def __init__(self, toggles: list[list[int]], joltages: list[int]):
        self.joltages = tuple(joltages)
        self.toggles = []
        for toggle in toggles:
            binary_toggle = [int(i in toggle) for i, _ in enumerate(self.joltages)]
            self.toggles.append(binary_toggle)
        self.toggles = sorted(self.toggles, key=lambda x: -sum(x))
        self.max_toggle_weight = max([sum(t) for t in self.toggles])

    def turn_on(self) -> int:
        start = tuple([0 for _ in self.joltages])
        visited = {start: 0}
        buttons = [0 for _ in self.toggles]
        pushes = 0
        d = self.heuristic(start)
        frontier = []
        heappush(frontier, (d, pushes, start, buttons))
        max_distance = d
        current_best = 10**10
        current_buttons = None
        while frontier:
            d, pushes, state, buttons = heappop(frontier)
            visited[state] = pushes
            if len(visited) % 100_000 == 0:
                print(
                    f"distance={d}, relative={d / max_distance * 100:2.4f}%."
                    f" State: {state} / Joltage: {self.joltages}"
                )
            if state == self.joltages:
                print(f"Found a candidate: {pushes}." f"Frontier len: {len(frontier)}")
                current_best = min(current_best, pushes)
                current_buttons = buttons
            for i, toggle in enumerate(self.toggles):
                for p in range(1, self.get_max_possible_pushes(state, toggle) + 1):
                    new_state = tuple([s + p * int(t) for s, t in zip(state, toggle)])
                    new_pushes = pushes + p
                    new_distance = self.heuristic(new_state) + new_pushes
                    if (
                        new_pushes < visited.get(new_state, 10**10)
                        and new_distance < current_best
                    ):
                        new_buttons = deepcopy(buttons)
                        new_buttons[i] += p
                        heappush(
                            frontier, (new_distance, new_pushes, new_state, new_buttons)
                        )

        return current_best, current_buttons

    def turn_on_naive(self) -> int:
        start = tuple([0 for _ in self.joltages])
        buttons = [0 for _ in self.joltages]
        visited = {start}
        frontier = deque([(0, start, buttons)])
        while frontier:
            steps, state, buttons = frontier.popleft()
            if state == self.joltages:
                return steps, buttons
            for i, toggle in enumerate(self.toggles):
                next_state = tuple([a + b for a, b in zip(state, toggle)])
                if next_state not in visited:
                    new_buttons = deepcopy(buttons)
                    new_buttons[i] += 1
                    frontier.append((steps + 1, next_state, new_buttons))
                    visited.add(next_state)
        raise ValueError("Should not reach.")

    def solve_lp(self) -> tuple[int, list[int]]:
        number_of_variables = len(self.toggles)
        number_of_constraints = len(self.joltages)

        solver = pywraplp.Solver.CreateSolver("SCIP")  # SCIP is included in OR-Tools

        x = [
            solver.IntVar(0, solver.infinity(), f"x_{k}")
            for k in range(number_of_variables)
        ]

        for j in range(number_of_constraints):
            solver.Add(
                sum(self.toggles[k][j] * x[k] for k in range(number_of_variables))
                == self.joltages[j]
            )
        solver.Minimize(solver.Sum(x))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Optimal solution found:")
            solution = [xi.solution_value() for xi in x]
            print(solution)
            print("Objective value:", solver.Objective().Value())
            return solver.Objective().Value(), solution
        else:
            print("No solution found.")
            raise ValueError

    def distance(self, state: list[int]) -> int:
        return sum(a - b for a, b in zip(self.joltages, state))

    def get_max_possible_pushes(self, state: list[int], toggle: list[bool]) -> int:
        return min([a - b for a, b, t in zip(self.joltages, state, toggle) if t])

    def heuristic(self, state: int):
        max_remaining = max(j - c for j, c in zip(self.joltages, state, strict=True))
        weighted_remaining = sum(
            j - c for j, c in zip(self.joltages, state, strict=True)
        )
        return max(max_remaining, weighted_remaining)


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
        manuals.append(ManualLine(toggles, joltages))
    solutions = []
    for manual in tqdm(manuals):
        pushes, buttons = manual.solve_lp()
        solutions.append(pushes)
        print(f"Pushes={pushes}, Buttons: {buttons}")

    print(f"The total button pushes is: {int(sum(solutions))}")
