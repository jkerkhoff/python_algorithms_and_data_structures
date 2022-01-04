from hypothesis import given, strategies as st

from src.algorithms.number_theory.multiplication import russian_peasant_method


@given(st.integers(), st.integers())
def test_russian_peasant_method(a: int, b: int):
    assert russian_peasant_method(a, b) == a * b
