import pytest

from hypothesis import given, strategies as st

from tests.helpers import lists_and_indices

from src.algorithms.arrays.selection import select_from_sort, quickselect


@given(lists_and_indices(st.integers()))
def test_select_from_sort(ex):
    arr, rank = ex
    n = len(arr)

    ground_truth = sorted(range(n), key=arr.__getitem__)[rank]
    idx1 = select_from_sort(arr, rank)
    idx2 = select_from_sort(arr, rank - n)
    assert idx1 == ground_truth
    assert idx2 == ground_truth

    with pytest.raises(IndexError):
        select_from_sort(arr, rank + n)
    with pytest.raises(IndexError):
        select_from_sort(arr, rank - 2 * n)


@given(lists_and_indices(st.integers()))
def test_quickselect(ex):
    arr, rank = ex
    n = len(arr)

    ground_truth = sorted(range(n), key=arr.__getitem__)[rank]
    idx1 = quickselect(arr, rank)
    idx2 = quickselect(arr, rank - n)
    assert idx1 == ground_truth
    assert idx2 == ground_truth

    with pytest.raises(IndexError):
        select_from_sort(arr, rank + n)
    with pytest.raises(IndexError):
        select_from_sort(arr, rank - 2 * n)
