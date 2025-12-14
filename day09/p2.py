from itertools import combinations
from heapq import heapify, heappop

Position = tuple[int, int]


class Interval:
    def __init__(self, start: int, end: int, fix_coordinate: int):
        self.start = start
        self.end = end
        self.fixed_coordinate = fix_coordinate

    def __repr__(self):
        return f"Interval({self.start}, {self.end}, {self.fixed_coordinate})"


class IntervalTreeNode:
    def __init__(self, intervals: list[Interval]):
        """
        Note: Intervals must be sorted by start
        """
        self.center = intervals[len(intervals) // 2].start
        self.intervals = [iv for iv in intervals if iv.start <= self.center <= iv.end]
        left_intervals = [iv for iv in intervals if iv.end < self.center]
        right_intervals = [iv for iv in intervals if iv.start > self.center]

        self.left = IntervalTreeNode(left_intervals) if left_intervals else None
        self.right = IntervalTreeNode(right_intervals) if right_intervals else None

    def query(self, point: int, min_p: int, max_p: int) -> bool:
        for iv in self.intervals:
            if iv.start < point < iv.end and min_p < iv.fixed_coordinate < max_p:
                return True

        if self.left and point <= self.center:
            if self.left.query(point, min_p, max_p):
                return True

        if self.right and point >= self.center:
            if self.right.query(point, min_p, max_p):
                return True

        return False


class IntervalTree:
    def __init__(self, intervals: list[Interval]):
        intervals = sorted(intervals, key=lambda x: x.start)
        self.root = IntervalTreeNode(intervals)

    def query(self, point: int, min_p: int, max_p: int) -> bool:
        return self.root.query(point, min_p, max_p)


class IntervalTiles:
    def __init__(self, tiles: list[Position]):
        if tiles[0] != tiles[-1]:
            tiles = tiles + [tiles[0]]
        v_intervals = []
        h_intervals = []
        for (x1, y1), (x2, y2) in zip(tiles[:-1], tiles[1:]):
            if x1 == x2:
                v_intervals.append(Interval(*sorted([y1, y2]), x1))
            elif y1 == y2:
                h_intervals.append(Interval(*sorted([x1, x2]), y1))
            else:
                raise ValueError()
        self.h_tree = IntervalTree(h_intervals)
        self.v_tree = IntervalTree(v_intervals)

    def is_valid(self, t1: Position, t2: Position) -> bool:
        min_x = min(t1[0], t2[0])
        min_y = min(t1[1], t2[1])
        max_x = max(t1[0], t2[0])
        max_y = max(t1[1], t2[1])
        for x in [min_x, min_x + 1, max_x - 1, max_x]:
            if self.h_tree.query(x, min_y, max_y):
                return False
        for y in [min_y, min_y + 1, max_y - 1, max_y]:
            if self.v_tree.query(y, min_x, max_x):
                return False
        return True


def compute_area(t1: Position, t2: Position) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def solve(tiles: list[Position]) -> int:
    interval_tiles = IntervalTiles(tiles)
    possible_squares = [
        (-compute_area(t1, t2), (t1, t2)) for t1, t2 in combinations(tiles, 2)
    ]
    heapify(possible_squares)
    while possible_squares:
        area, (t1, t2) = heappop(possible_squares)
        if interval_tiles.is_valid(t1, t2):
            return -area


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        input_ = f.read().strip()

    tiles = [tuple(list(map(int, line.split(",")))) for line in input_.split("\n")]
    max_area = solve(tiles)

    points = tiles

    points = points + [points[0]]

    print(f"The max area is (hopefully): {max_area}")
    print(f"The difference is: {max_area - 1573359081}")
