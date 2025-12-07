from collections import defaultdict
import pygame
import numpy as np


GRID_W = 60
GRID_H = 40
SCALE = 15
FPS = 10
MAX_VALUE = 8


def value_to_color(v, max_v):
    """
    Map value in [1 .. max_v] to a color from dark red → bright yellow.
    """
    if v <= 0:
        return (0, 0.0, 0)  # black for 0 or invalid
    if v >= max_v:
        return (255, 255, 0)

    # Start (dark red) and end (yellow)
    r1, g1, b1 = (255, 0, 0)
    r2, g2, b2 = (255, 255, 0)

    t = np.log(v) / np.log(max_v)

    # Spectral colormap keypoints from Matplotlib
    # (position, R, G, B) in 0–1 range
    spectral = [
        (0.0, 0.6196, 0.0039, 0.2588),  # dark red
        (0.1, 0.8353, 0.2431, 0.3098),
        (0.2, 0.9569, 0.4275, 0.2627),
        (0.4, 0.9922, 0.6824, 0.3804),
        (0.6, 0.9961, 0.8784, 0.5451),
        (0.8, 0.8784, 0.9529, 0.9725),
        (1.0, 0.5725, 0.7725, 0.8706),  # blue
    ]

    # Find which interval t belongs to
    for i in range(len(spectral) - 1):
        t0, r0, g0, b0 = spectral[i]
        t1, r1, g1, b1 = spectral[i + 1]
        if t0 <= t <= t1:
            # Local interpolation factor
            u = (t - t0) / (t1 - t0)
            r = r0 + (r1 - r0) * u
            g = g0 + (g1 - g0) * u
            b = b0 + (b1 - b0) * u
            return (int(r * 255), int(g * 255), int(b * 255))

    # Fallback (should never happen)
    return (0, 0, 0)


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

        self.frames: list[dict[int, int]] = []

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
            self.frames.append(timelines)
        return sum(timelines.values())

    def draw(self):
        max_value = max(self.frames[-1].values())
        grid = np.zeros((self.max_y + 2, self.max_x, 3), dtype=np.uint8)
        for y, xs in self.splitters.items():
            for x in xs:
                grid[y, x] = (255, 255, 255)

        pygame.init()
        screen = pygame.display.set_mode((GRID_W * SCALE, GRID_H * SCALE))
        clock = pygame.time.Clock()

        frame = 0

        for y, frame in enumerate(self.frames, start=1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            for x, rays in frame.items():
                color = value_to_color(rays, max_value)
                grid[y, x] = color

            surface = pygame.surfarray.make_surface(grid.swapaxes(0, 1))
            if SCALE != 1:
                surface = pygame.transform.scale(
                    surface, (GRID_W * SCALE, GRID_H * SCALE)
                )

            screen.blit(surface, (0, 0))
            pygame.display.flip()

            clock.tick(FPS)

        # ----- Keep last frame displayed -----
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()
    tachyonic_rays = TachyonicRays(input_)
    timelines = tachyonic_rays.quantum_propagate()
    print(f"Total quantum timelines: {timelines}")
    tachyonic_rays.draw()
