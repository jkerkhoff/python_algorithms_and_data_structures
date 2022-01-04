from hypothesis import given, strategies as st

from tests.algorithms.sorting.helpers import check_sorted

from src.algorithms.sorting.integer_sorts import counting_sort


@given(st.lists(st.integers(-1000, 1000)))
def test_counting_sort(values):
    counting_sort(values)
    check_sorted(values)
