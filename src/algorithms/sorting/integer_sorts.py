"""Implementations of various integer sorting algorithms."""

from collections.abc import MutableSequence


def counting_sort(seq: MutableSequence[int]) -> None:
    """Counting sort.

    Complexity: O(n + (max(seq) - min(seq)))
    """
    if not seq:
        return

    lo = min(seq)
    hi = max(seq)
    spread = hi - lo
    buckets = [0 for _ in range(spread + 1)]
    while seq:
        buckets[seq.pop() - lo] += 1

    for idx, count in enumerate(buckets):
        if count:
            value = idx + lo
            seq.extend(value for _ in range(count))
