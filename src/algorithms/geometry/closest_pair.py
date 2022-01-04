"""Algorithms for finding the closest pair in a set of points."""

import math
import random
from collections import defaultdict
from numbers import Real

# TODO: Khuller-Matias
# TODO: sweep line
# TODO: divide and conquer
# TODO: dynamic


def brute_force(points: list[tuple[Real, ...]]) -> tuple[int, int]:
    """Return the indices of two points at pairwise minimal distance.

    Complexity: O(d n^2) where d is the number of dimensions
    """
    n = len(points)
    if n < 2:
        raise ValueError("input smaller than 2")

    smallest_distance = math.inf
    out = None
    for i in range(n):
        for j in range(i + 1, n):
            distance = math.dist(points[i], points[j])
            if distance < smallest_distance:
                smallest_distance = distance
                out = (i, j)
    return out


def rabin_lipton_2d(points: list[tuple[Real, Real]]) -> tuple[int, int]:
    """Return the indices of two points at pairwise minimal distance.

    Complexity: O(n) expected, O(n^2) worst case.
    """
    n = len(points)
    if n < 2:
        raise ValueError("input smaller than 2")

    grid_unit = math.inf
    for _ in range(n):
        i, j = random.sample(range(n), 2)
        distance = math.dist(points[i], points[j])
        if distance < grid_unit:
            grid_unit = distance
            if distance == 0:
                return i, j

    grid = defaultdict(list)
    for i in range(n):
        x = round(points[i][0] / grid_unit)
        y = round(points[i][1] / grid_unit)
        grid[(x, y)].append(i)

    smallest_distance = math.inf
    out = None
    for (x, y), local_points in grid.items():
        for a, i in enumerate(local_points):
            for j in local_points[a + 1:]:
                distance = math.dist(points[i], points[j])
                if distance < smallest_distance:
                    smallest_distance = distance
                    out = (i, j)

        for key in (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1):
            for i in local_points:
                for j in grid.get(key, ()):
                    distance = math.dist(points[i], points[j])
                    if distance < smallest_distance:
                        smallest_distance = distance
                        out = (i, j)

    return out
