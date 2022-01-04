"""Algorithms for finding the convex hull of a set of points in the plane."""

from collections.abc import Sequence
from numbers import Real

Point = tuple[Real, Real]


def recursive_convex_hull(points: Sequence[Point]) -> list[int]:
    """Return the indices of the convex hull of the given set of points."""
    indices = sorted(range(len(points)), key=points.__getitem__)
    points = [points[idx] for idx in indices]

    def rch(start: int, stop: int) -> list[int]:
        if stop - start == 1:
            return [start]

        mid = (start + stop) // 2
        left_hull = rch(start, mid)
        right_hull = rch(mid, stop)

        # TODO: combine

    return [indices[idx] for idx in rch(0, len(points))]


def monotone_chain(points: Sequence[Point]) -> list[int]:
    """Return the indices of the convex hull of the given set of points.

    Points will be in counterclockwise order, with the leftmost point first.
    """
    points = sorted((x, y, i) for i, (x, y) in enumerate(points))

    def clockwise(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) <= (q[1] - p[1]) * (r[0] - p[0])

    lo_hull = []
    hi_hull = []
    for i in range(len(points)):
        point = points[i]

        if i > 0 and points[i - 1][:2] == point[:2]:
            continue

        while len(lo_hull) > 1 and clockwise(lo_hull[-2], lo_hull[-1], point):
            lo_hull.pop()
        lo_hull.append(point)

        while len(hi_hull) > 1 and clockwise(point, hi_hull[-1], hi_hull[-2]):
            hi_hull.pop()
        hi_hull.append(point)

    hull = lo_hull + hi_hull[-2:0:-1]
    return [point[2] for point in hull]
