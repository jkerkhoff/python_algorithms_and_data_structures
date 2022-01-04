import pytest

from hypothesis import given, strategies as st

from src.algorithms.geometry.convex_hull import monotone_chain


def is_strictly_ccw(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) > (q[1] - p[1]) * (r[0] - p[0])


def is_ccw(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) >= (q[1] - p[1]) * (r[0] - p[0])


def verify_no_repeated_points(points: list[tuple[int, int]],
                              indices: list[int]):
    indices_set = set(indices)
    if len(indices) != len(indices_set):
        for idx in indices:
            if idx not in indices_set:
                pytest.fail(f"repeated point: "
                            f"index {idx} appears more then once")
            indices_set.discard(idx)

    coords = [points[idx] for idx in indices]
    coords_set = set(coords)
    if len(coords) != len(coords_set):
        for point in coords:
            if point not in coords_set:
                pytest.fail(f"repeated point: "
                            f"point {point} appears more then once")
            coords_set.discard(point)


def verify_convex(points: list[tuple[int, int]], indices: list[int]):
    coords = [points[idx] for idx in indices]

    m = len(coords)
    if m > 2:
        for i in range(len(coords)):
            p = points[indices[i]]
            q = points[indices[(i + 1) % m]]
            r = points[indices[(i + 2) % m]]

            if not is_ccw(p, q, r):
                pytest.fail(f"not convex: points {p, q, r} form a right turn")


def verify_hull(points: list[tuple[int, int]], indices: list[int]):
    if not indices:
        if points:
            pytest.fail("not a hull: contains no points")
        return

    other_indices = set(range(len(points))).difference(indices)
    for i in range(len(indices)):
        p = points[indices[i]]
        r = points[indices[(i + 1) % len(indices)]]
        for j in other_indices:
            q = points[j]

            if is_strictly_ccw(p, q, r):
                pytest.fail(f"not a hull: {q} lies outside")


@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_monotone_chain(points: list[tuple[int, int]]):  # TODO: floats
    hull = monotone_chain(points)
    verify_no_repeated_points(points, hull)
    verify_convex(points, hull)
    verify_hull(points, hull)
