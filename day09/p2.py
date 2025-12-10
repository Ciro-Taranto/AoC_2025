from bisect import bisect_left, bisect_right
from itertools import combinations
from heapq import heapify, heappop
from collections import defaultdict

Position = tuple[int, int]


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

    def no_crossings(self, t1: Position, t2: Position) -> bool:
        if t1[0] == t2[0]:
            perpendiculars = self.h
            vals = self.ys
            c = t1[0]
            lo, hi = (t1[1], t2[1]) if t1[1] < t2[1] else (t2[1], t1[1])
        elif t1[1] == t2[1]:
            perpendiculars = self.v
            vals = self.xs
            c = t1[1]
            lo, hi = (t1[0], t2[0]) if t1[0] < t2[0] else (t2[0], t1[0])
        else:
            raise ValueError
        start = bisect_left(vals, lo)
        end = bisect_right(vals, hi)
        for v in vals[start:end]:
            if not (lo <= v <= hi):
                continue
            lines = perpendiculars[v]
            for s, e in lines:
                if s < c < e:
                    # there is a crossing!
                    return False

        return True

    def no_line_crossing(self, c: int, start: int, end: int, horizontal: bool) -> bool:
        perpendicular = self.v if horizontal else self.h
        for a, lines in perpendicular.items():
            if start < a < end:
                for s, e in lines:
                    if s < c < e:
                        return False
        return True

    def is_valid_pair(self, t1: Position, t2: Position) -> bool:
        min_x, max_x = t1[0], t2[0]
        if min_x > max_x:
            min_x, max_x = max_x, min_x
        min_y, max_y = t1[1], t2[1]
        if min_y > max_y:
            min_y, max_y = max_y, min_y
        lines = [
            (min_x, min_y, max_y, False),
            (max_x, min_y, max_y, False),
            (min_y, min_x, max_x, True),
            (min_y, min_x, max_x, True),
            (min_x + 1, min_y, max_y, False),
            (max_x - 1, min_y, max_y, False),
            (min_y + 1, min_x, max_x, True),
            (min_y - 1, min_x, max_x, True),
        ]
        return all([self.no_line_crossing(*line) for line in lines])

    def corners_are_inside(self, t1: Position, t2: Position) -> bool:
        additional_corners = [(t1[0], t2[1]), (t2[0], t1[1])]
        return all([self.point_inside(p) for p in additional_corners])

    def point_inside(self, p: Position) -> bool:
        x, y = p

        if y in self.h:
            for lo, hi in self.h[y]:
                if lo <= x <= hi:
                    return True

        # 2. Check if point lies exactly on a vertical edge
        if x in self.v:
            for lo, hi in self.v[x]:
                if lo <= y <= hi:
                    return True

        cnt = 0
        for vx, intervals in self.v.items():
            if vx <= x:
                continue
            for lo, hi in intervals:
                if lo <= y < hi:  # standard ray-cast convention
                    cnt += 1

        return (cnt % 2) == 1


def compute_area(t1: Position, t2: Position) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def solve(tiles: list[tuple[int, int]]) -> tuple[int, tuple[Position, Position]]:
    poly_tiles = PolyTiles(tiles)
    possible_squares = [
        (-compute_area(t1, t2), (t1, t2)) for t1, t2 in combinations(tiles, 2)
    ]
    heapify(possible_squares)
    while possible_squares:
        area, (t1, t2) = heappop(possible_squares)
        if poly_tiles.is_valid_pair(t1, t2):
            return -area, (t1, t2)

    raise ValueError("should not reach")


if __name__ == "__main__":
    from pathlib import Path
    import drawsvg as draw

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    tiles = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    max_area, (t1, t2) = solve(tiles)

    points = tiles

    points = points + [points[0]]

    extra_points = [t1, (t1[0], t2[1]), t2, (t2[0], t1[1])]
    extra_points = extra_points + extra_points[0:1]

    # determine bounding box
    def save_polygon_svg(
        points, extra_points, filename="polygon.svg", viewport_size=500, margin=10
    ):
        xs, ys = zip(*points)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width, height = max_x - min_x, max_y - min_y

        if width == 0:
            width = 1
        if height == 0:
            height = 1

        # scale to fit viewport
        scale = min(
            (viewport_size - 2 * margin) / width, (viewport_size - 2 * margin) / height
        )

        # shift and scale points
        d = draw.Drawing(viewport_size, viewport_size)

        scaled = [
            ((x - min_x) * scale + margin, (y - min_y) * scale + margin)
            for x, y in extra_points
        ]

        d.append(
            draw.Lines(
                *sum(scaled, ()),
                close=True,
                stroke="red",
                fill="none",
                stroke_width=2.0,
            )
        )
        scaled = [
            ((x - min_x) * scale + margin, (y - min_y) * scale + margin)
            for x, y in points
        ]

        d.append(
            draw.Lines(
                *sum(scaled, ()),
                close=True,
                stroke="black",
                fill="none",
                stroke_width=2.0,
            )
        )
        d.save_svg(filename)
        print(f"SVG saved to {filename}")

    save_polygon_svg(points, extra_points, viewport_size=1000, margin=10)
    print(f"The max area is (hopefully): {max_area}")
