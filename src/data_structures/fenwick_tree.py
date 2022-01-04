"""Implementation of a Fenwick/binary indexed tree.

Based on presentation in the following paper:
https://doi.org/10.1002%2Fspe.4380240306
"""

from collections.abc import Iterable
from typing import TypeVar, Generic

T = TypeVar('T')

# TODO: allow arbitrary associative operations
# TODO: specialize for floats: store exact values and use math.fsum
# TODO: dynamic length


class FenwickTree(Generic[T]):
    """Data structure for fast prefix sums and updates on lists of numbers."""

    __slots__ = ('_data', )

    def __init__(self, iterable: Iterable[T]):
        """Construct a fenwick tree representing the given sequence.

        Complexity: O(n lg n)
        """
        values = list(iterable)
        self._data = [values[0]]
        for i in range(1, len(values)):
            self._data.append(sum(values[(i & (i - 1)) + 1:i + 1]))

    def prefix_sum(self, k: int) -> T:
        """Return the sum of the first k values.

        Complexity: O(lg n)
        """
        if k == 0:
            return 0

        result = self._data[0]
        idx = k - 1
        while idx:
            result += self._data[idx]
            idx &= idx - 1
        return result

    def range_sum(self, start: int, stop: int) -> T:
        """Return the sum of the given range of values.

        Includes the value at index start, but not the value at index stop.

        Complexity: O(lg n)
        """
        if start == 0:
            return self.prefix_sum(stop)

        result = 0
        idx = stop - 1
        while idx >= start:
            result += self._data[idx]
            idx &= idx - 1

        parent = idx
        idx = start - 1
        while idx > parent:
            result -= self._data[idx]
            idx &= idx - 1

        return result

    def update(self, idx: int, value: T, absolute: bool = False) -> None:
        """Update the value at index idx.

        The given value is added to the current value at the given index.
        To assign a new value instead, use absolute=True.

        Complexity: O(lg n)
        """
        if absolute:
            value -= self[idx]

        if idx == 0:
            self._data[0] += value
            return

        while idx < len(self._data):
            self._data[idx] += value
            idx += idx & -idx

    def __getitem__(self, idx: int) -> T:
        if idx < 0:
            idx += len(self)

        result = self._data[idx]
        if idx:
            parent = idx & (idx - 1)
            idx -= 1
            while idx != parent:
                result -= self._data[idx]
                idx &= idx - 1
        return result

    def __setitem__(self, idx: int, value: T) -> None:
        if idx < 0:
            idx += len(self)
        self.update(idx, value, True)

    def __len__(self) -> int:
        return len(self._data)
