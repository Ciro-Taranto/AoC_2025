import pygame
from bisect import bisect_left, bisect_right
from itertools import combinations
from heapq import heapify, heappop
from collections import defaultdict
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection

Position = tuple[int, int]


def get_colors() -> tuple[int, int]:
    colors = []
    for i in range(10):
        if i == 0:
            # First polygon: "tile color" (light brown)
            colors.append((210, 180, 140))
        elif i == 1:
            # Second polygon: green
            colors.append((0, 255, 0))
        else:
            # Next polygons: magenta variations
            base = 200
            step = 20
            val = max(0, min(255, base - (i - 2) * step))
            colors.append((val, 0, val))  # RGB: (R=magenta tone, G=0, B=magenta tone)
    return colors


class PolyTiles:
    def __init__(self, tiles: list[Position]):
        if tiles[0] != tiles[-1]:
            tiles = tiles + [tiles[0]]
        v, h = defaultdict(list), defaultdict(list)
        for p, n in zip(tiles[:-1], tiles[1:]):
            if p[0] == n[0]:
                x = p[0]
                min_y, max_y = (p[1], n[1]) if p[1] < n[1] else (n[1], p[1])
                v[x].append((min_y, max_y))
            elif p[1] == n[1]:
                y = p[1]
                min_x, max_x = (p[0], n[0]) if p[0] < n[0] else (n[0], p[0])
                h[y].append((min_x, max_x))
            else:
                raise ValueError
        self.h = {key: sorted(value) for key, value in h.items()}
        self.v = {key: sorted(value) for key, value in v.items()}

        self.xs = sorted(self.v)
        self.ys = sorted(self.h)
        self.polygon = Polygon(tiles)
        self.colors = get_colors()
        pygame.init()
        width = height = 1000
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.x_scaling = width / (self.xs[-1] * 1.05)
        self.y_scaling = width / (self.ys[-1] * 1.05)
        pygame.display.set_caption("Will the boxes fit?")
        self.screen.fill((0, 0, 0))

    def intersection(self, t1: Position, t2: Position) -> bool:
        box = Polygon([(t1[0], t1[1]), (t1[0], t2[1]), (t2[0], t2[1]), (t2[0], t1[1])])
        intersection = self.polygon.intersection(box)
        fully_included = intersection.area == box.area
        exterior_points = self.get_exterior_points(intersection)
        self.draw(box, exterior_points)
        return fully_included

    def draw(self, box: Polygon, exterior_points: list[list[Position]]) -> None:
        polygons = (
            self.get_exterior_points(self.polygon)
            + self.get_exterior_points(box)
            + exterior_points
        )

        # Draw intersection polygons
        for verts, color in zip(polygons, self.colors):
            pygame.draw.polygon(self.screen, color, verts)  # fill
            pygame.draw.polygon(self.screen, (0, 0, 0), verts, 2)  # black border
        pygame.display.flip()
        self.clock.tick(5)

    def get_exterior_points(
        self,
        intersection: Polygon | MultiPolygon | GeometryCollection,
    ) -> list[list[Position]]:
        exterior_points = []
        if intersection.is_empty:
            return exterior_points
        match intersection:
            case Polygon():
                if intersection.area > 0:
                    coords = []
                    for x, y in list(intersection.exterior.coords)[:-1]:
                        coords.append((x * self.x_scaling, y * self.y_scaling))
                    exterior_points.append(coords)
            case MultiPolygon() | GeometryCollection():
                for geom in intersection.geoms:
                    exterior_points.extend(self.get_exterior_points(geom))
        return exterior_points

    def is_valid(self, t1: Position, t2: Position) -> bool:
        min_x = min(t1[0], t2[0])
        min_y = min(t1[1], t2[1])
        max_x = max(t1[0], t2[0])
        max_y = max(t1[1], t2[1])
        vertical_lines = [
            (min_x, (min_y, max_y)),
            (min_x + 1, (min_y, max_y)),
            (max_x, (min_y, max_y)),
            (max_x - 1, (min_y, max_y)),
        ]

        horizontal_lines = [
            (min_y, (min_x, max_x)),
            (min_y + 1, (min_x, max_x)),
            (max_y, (min_x, max_x)),
            (max_y - 1, (min_x, max_x)),
        ]

        for c, (start, end) in vertical_lines:
            if self.is_any_line_crossing(c, start, end, self.ys, self.h):
                return False
        for c, (start, end) in horizontal_lines:
            if self.is_any_line_crossing(c, start, end, self.xs, self.v):
                return False
        return True

    @staticmethod
    def is_any_line_crossing(
        c: int,
        start: int,
        end: int,
        positions: list[int],
        perpendicular_lines: dict[int, list[tuple[int, int]]],
    ) -> bool:
        start_idx = bisect_left(positions, start)
        end_idx = bisect_right(positions, end)
        for position in positions[start_idx:end_idx]:
            if position in {start, end}:
                continue
            for s, e in perpendicular_lines[position]:
                if s < c < e:
                    return True
        return False


def compute_area(t1: Position, t2: Position) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def solve(tiles: list[tuple[int, int]]) -> tuple[int, tuple[Position, Position]]:
    poly_tiles = PolyTiles(tiles)
    possible_squares = [
        (-compute_area(t1, t2), (t1, t2)) for t1, t2 in combinations(tiles, 2)
    ]
    heapify(possible_squares)
    running = True
    while possible_squares and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        area, (t1, t2) = heappop(possible_squares)
        if poly_tiles.intersection(t1, t2):
            return -area, (t1, t2)

    raise ValueError("should not reach")


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    tiles = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    max_area, (t1, t2) = solve(tiles)
    print(f"The max area is (hopefully): {max_area}")
