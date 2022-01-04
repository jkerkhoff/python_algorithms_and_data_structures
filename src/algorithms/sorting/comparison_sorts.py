"""Implementations of various comparison sort algorithms."""
import random
from collections.abc import MutableSequence, Sequence
from typing import TypeVar, Optional

T = TypeVar("T")


def insertion_sort(seq: MutableSequence[T]) -> None:
    """Stable in-place insertion sort.

    Complexity: O(n^2)
    """
    for i in range(1, len(seq)):
        j = i
        while j > 0 and seq[i] < seq[j - 1]:
            j -= 1

        seq.insert(j, seq.pop(i))


def recursive_merge_sort(seq: MutableSequence[T],
                         start: Optional[int] = 0,
                         stop: Optional[int] = None) -> None:
    """Stable merge sort.

    Complexity: O(n lg n)
    """
    if stop is None:
        stop = len(seq)

    if stop - start <= 1:
        return

    mid = (start + stop) // 2
    recursive_merge_sort(seq, start, mid)
    recursive_merge_sort(seq, mid, stop)

    a = seq[start:mid]
    b = seq[mid:stop]

    i = 0
    j = 0
    for k in range(start, stop):
        if a[i] <= b[j]:
            seq[k] = a[i]
            i += 1

            if i == len(a):
                seq[k + 1:stop] = b[j:]
                break
        else:
            seq[k] = b[j]
            j += 1

            if j == len(b):
                seq[k + 1:stop] = a[i:]
                break


def recursive_quicksort(seq: MutableSequence[T],
                        start: Optional[int] = 0,
                        stop: Optional[int] = None) -> None:
    """In-place recursive quicksort (random pivot).

    Complexity: O(n lg n) expected, O(n^2) worst case

    Note that the expectation is over the internal randomness, not the input.
    """
    if stop is None:
        stop = len(seq)

    if stop - start <= 1:
        return

    pivot_idx = random.randrange(start, stop)
    seq[pivot_idx], seq[stop - 1] = seq[stop - 1], seq[pivot_idx]

    pivot_val = seq[stop - 1]

    i = start
    for j in range(start, stop):
        if seq[j] <= pivot_val:
            seq[i], seq[j] = seq[j], seq[i]
            i += 1

    recursive_quicksort(seq, start, i - 1)
    recursive_quicksort(seq, i - 1, stop)
