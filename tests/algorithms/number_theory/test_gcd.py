import math

from hypothesis import given, strategies as st

from src.algorithms.number_theory.gcd import euclidean, binary_euclidean


@given(st.integers(), st.integers())
def test_euclidean(a: int, b: int):
    assert euclidean(a, b) == math.gcd(a, b)


@given(st.integers(), st.integers())
def test_binary_euclidean(a: int, b: int):
    assert binary_euclidean(a, b) == math.gcd(a, b)
