"""Algorithms for finding the index for a given rank in an array of numbers."""

import random
from collections.abc import Sequence, MutableSequence


def select_from_sort(arr: Sequence, rank: int = 0) -> int:
    """Return an index corresponding to a value of given rank in the list.

    If rank is negative, it will be interpreted as in slice notation.

    Ties are broken by index.

    Complexity: O(n lg n)
    """
    return sorted(range(len(arr)), key=arr.__getitem__)[rank]


def partition(arr: MutableSequence, start: int, stop: int,
              pivot_idx: int) -> int:
    """Partition a range of arr and return the new index of the pivot.

    Note: partition is not guaranteed to be stable.

    Complexity: O(k), where k is the length of the range
    """
    pivot_val = arr[pivot_idx]
    arr[pivot_idx], arr[stop - 1] = arr[stop - 1], arr[pivot_idx]

    i = start
    for j in range(start, stop):
        if arr[j] <= pivot_val:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1

    return i - 1


def quickselect(arr: Sequence, rank: int = 0) -> int:
    """Return an index corresponding to a value of given rank in the list.

    If rank is negative, it will be interpreted as in slice notation.

    Ties are broken by index.

    Complexity: O(n) expected, O(n^2) worst case
    """
    n = len(arr)
    arr = list((x, i) for i, x in enumerate(arr))

    if rank < 0:
        rank += n

    if rank < 0 or rank > n - 1:
        raise IndexError(
            f"no element of rank {rank} in list of length {len(arr)}")

    start = 0
    stop = n
    while True:
        pivot_idx = random.randrange(start, stop)
        pivot_rank = partition(arr, start, stop, pivot_idx)

        if pivot_rank < rank:
            start = pivot_rank + 1
        elif pivot_rank > rank:
            stop = pivot_rank
        else:
            return arr[pivot_rank][1]


def quickselect_with_median_of_medians(arr: Sequence, rank: int = 0) -> int:
    """Return an index corresponding to a value of given rank in the list.

    If rank is negative, it will be interpreted as in slice notation.

    Ties are broken by index.

    Complexity: O(n)
    """
    raise NotImplementedError()  # TODO
