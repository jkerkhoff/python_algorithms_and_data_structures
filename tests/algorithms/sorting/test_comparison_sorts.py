from hypothesis import given, strategies as st

from tests.algorithms.sorting.helpers import wrapped_value_lists, check_sorted, check_stable

from src.algorithms.sorting.comparison_sorts import insertion_sort, recursive_merge_sort, recursive_quicksort


@given(wrapped_value_lists(st.integers()))
def test_insertion_sort(values):
    original = values[:]
    insertion_sort(values)
    check_sorted(values)
    check_stable(original, values)


@given(wrapped_value_lists(st.integers()))
def test_recursive_merge_sort(values):
    original = values[:]
    recursive_merge_sort(values)
    check_sorted(values)
    check_stable(original, values)


@given(wrapped_value_lists(st.integers()))
def test_recursive_quicksort(values):
    recursive_quicksort(values)
    check_sorted(values)
