import itertools
import math
from numbers import Real
from typing import TypeVar

from hypothesis import given, strategies as st

from src.algorithms.geometry.closest_pair import brute_force, rabin_lipton_2d

T = TypeVar("T")

int_strategy = st.integers()
float_strategy = st.floats(allow_nan=False, allow_infinity=False, width=32)


@st.composite
def n_point_lists(draw: st.DrawFn,
                  elements: st.SearchStrategy[T],
                  min_dimension: int = 1,
                  max_dimension: int = 5,
                  *,
                  min_size: int = 2,
                  max_size: int | None = None) -> list[tuple[T, ...]]:
    dimension = draw(st.integers(min_dimension, max_dimension))
    return draw(
        st.lists(st.tuples(*(elements for _ in range(dimension))),
                 min_size=min_size,
                 max_size=max_size))


def verify_closest(points: list[tuple[Real, ...]], i: int, j: int):
    m_dist = min(math.dist(p, q) for p, q in itertools.combinations(points, 2))
    assert math.dist(points[i], points[j]) == m_dist


@given(n_point_lists(float_strategy))
def test_brute_force(points: list[tuple[Real, ...]]):
    i, j = brute_force(points)
    verify_closest(points, i, j)


@given(n_point_lists(float_strategy, min_dimension=2, max_dimension=2))
def test_rabin_lipton_2d(points: list[tuple[Real, Real]]):
    i, j = rabin_lipton_2d(points)
    verify_closest(points, i, j)
