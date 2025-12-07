from collections import defaultdict


class TachyonicRays:
    def __init__(self, input_: str):
        lines = input_.split("\n")
        self.max_y = len(lines)
        self.max_x = len(lines[0])
        self.start_x = lines[0].index("S")
        self.splitters = defaultdict(set)
        self.visited_splitters = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "^":
                    self.splitters[y].add(x)

    def propagate_ray(self) -> None:
        y = 0
        rays_x = {self.start_x}
        while y <= self.max_y:
            y += 1
            new_rays = set()
            for ray_x in rays_x:
                if ray_x in self.splitters[y]:
                    new_rays.add(ray_x - 1)
                    new_rays.add(ray_x + 1)
                    self.visited_splitters.add((ray_x, y))
                else:
                    new_rays.add(ray_x)
            rays_x = new_rays

    def quantum_propagate(self) -> int:
        timelines = defaultdict(int)
        timelines[self.start_x] = 1
        y = 0
        while y <= self.max_y:
            y += 1
            new_timelines = defaultdict(int)
            for x, occurrences in timelines.items():
                if x in self.splitters[y]:
                    new_timelines[x - 1] += occurrences
                    new_timelines[x + 1] += occurrences
                else:
                    new_timelines[x] += occurrences
            timelines = new_timelines
        return sum(timelines.values())


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()
    tachyonic_rays = TachyonicRays(input_)
    timelines = tachyonic_rays.quantum_propagate()
    print(f"Total quantum timelines: {timelines}")
