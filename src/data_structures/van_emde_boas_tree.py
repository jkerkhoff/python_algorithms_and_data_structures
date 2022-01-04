"""Implementation of a van Emde Boas tree."""

import math
from typing import Optional, Union

_base_size = 256  # up to this size we simply use a bit-vector


class VEBTree:
    """Efficient predecessor/successor/update queries on integer keys."""

    __slots__ = ("_k", "_galaxy", "_summary", "_min", "_max")

    _k: int
    # in the base case _galaxy is a bit vector
    _galaxy: Union[int, dict[int, "VEBTree"]]
    _summary: Optional["VEBTree"]
    _min: Optional[int]
    _max: Optional[int]

    def __init__(self, size: int):
        size = max(_base_size, size)

        self._k = math.ceil(math.log2(size))
        size = 1 << self._k

        self._min = None
        self._max = None

        if size == _base_size:
            self._galaxy = 0
        else:
            self._galaxy = {}

        self._summary = None

    def _high(self, x: int) -> int:
        """Return the highest order bits."""
        return x >> (self._k // 2)

    def _low(self, x: int) -> int:
        """Return the lowest order bits."""
        return x & ((1 << (self._k // 2)) - 1)

    def _index(self, high: int, low: int) -> int:
        return (high << (self._k // 2)) + low

    def _assert_in_universe(self, x: int) -> None:
        if x < 0 or x >= self.capacity():
            raise ValueError(
                f"Query failed: "
                f"value `{x}` not in universe [0, {1 << self._k}]")

    def capacity(self) -> int:
        return 1 << self._k

    def empty(self) -> bool:
        return self._min is None

    def min(self) -> Optional[int]:
        return self._min

    def max(self) -> Optional[int]:
        return self._max

    def _contains(self, x: int) -> bool:
        if x in (self._min, self._max):
            return True

        if isinstance(self._galaxy, int):
            return bool(self._galaxy & (1 << x))

        high = self._high(x)
        if high not in self._galaxy:
            return False

        return self._galaxy[high]._contains(self._low(x))

    def __contains__(self, x: int) -> bool:
        self._assert_in_universe(x)

        return self._contains(x)

    def _add(self, x: int) -> None:
        if self._min is None:
            self._min = self._max = x
            self._summary = VEBTree(1 << (self._k - self._k // 2))
            return

        if isinstance(self._galaxy, int):
            if x < self._min:
                self._galaxy |= 1 << self._min
                self._min = x
            elif x > self._max:
                self._galaxy |= 1 << x
                self._max = x
            else:
                self._galaxy |= 1 << x
        else:
            to_insert = x
            if x < self._min:
                # min was lazily inserted
                to_insert = self._min
                self._min = x
            elif x > self._max:
                # max is always fully inserted or equal to min
                self._max = x

            hi = self._high(to_insert)
            lo = self._low(to_insert)
            if hi not in self._galaxy:
                self._galaxy[hi] = VEBTree(1 << (self._k // 2))
                self._summary._add(hi)
            self._galaxy[hi]._add(lo)

    def add(self, x: int) -> None:
        self._assert_in_universe(x)

        if self._contains(x):
            raise ValueError(f"Insert query failed: {x} is already a member.")

        self._add(x)

    def _remove(self, x: int) -> None:
        if self._min == self._max:
            self._min = self._max = None
            self._summary = None
            return

        if isinstance(self._galaxy, int):
            if x == self._min:
                self._min = self._successor(x)
                self._galaxy -= 1 << self._min
            elif x == self._max:
                self._max = self._predecessor(x)
                self._galaxy -= 1 << x
            else:
                self._galaxy -= 1 << x
            return

        to_delete = x

        if x == self._min:
            # _min was lazily inserted, _summary and _galaxy don't know about it
            # instead, we remove the successor (the new _min)
            to_delete = self._min = self._successor(x)

        hi = self._high(to_delete)
        lo = self._low(to_delete)

        self._galaxy[hi]._remove(lo)
        if self._galaxy[hi].empty():
            self._summary._remove(hi)
            del self._galaxy[hi]

        if to_delete == self._max:
            if self._summary.empty():
                self._max = self._min
            else:
                self._max = self._predecessor(to_delete)

    def remove(self, x: int) -> None:
        self._assert_in_universe(x)

        if not self._contains(x):
            raise ValueError(f"Remove query failed: {x} is not a member.")

        self._remove(x)

    def _successor(self, x: int) -> Optional[int]:
        if self._min is None or x < self._min:
            return self._min

        if x >= self._max:
            return None

        if isinstance(self._galaxy, int):
            # mask out last x bits
            masked = self._galaxy & ~((1 << (x + 1)) - 1)
            # least significant set bit
            return (masked & -masked).bit_length() - 1

        hi = self._high(x)
        lo = self._low(x)

        if hi in self._galaxy and lo < self._galaxy[hi].max():
            return self._index(hi, self._galaxy[hi]._successor(lo))

        hi = self._summary._successor(hi)
        return self._index(hi, self._galaxy[hi].min())

    def successor(self, x: int) -> Optional[int]:
        """Return the smallest contained value greater than x."""

        self._assert_in_universe(x)
        return self._successor(x)

    def _predecessor(self, x: int) -> Optional[int]:
        if self._max is None or x > self._max:
            return self._max

        if x <= self._min:
            return None

        if isinstance(self._galaxy, int):
            masked = self._galaxy & ((1 << x) - 1)
            if masked == 0:
                return self._min
            return masked.bit_length() - 1

        hi = self._high(x)
        lo = self._low(x)

        if hi in self._galaxy and lo > self._galaxy[hi].min():
            return self._index(hi, self._galaxy[hi]._predecessor(lo))

        hi = self._summary._predecessor(hi)
        if hi is None:
            return self._min
        return self._index(hi, self._galaxy[hi].max())

    def predecessor(self, x: int) -> Optional[int]:
        """Return the largest contained value smaller than x."""

        self._assert_in_universe(x)
        return self._predecessor(x)

    def pop_min(self) -> Optional[int]:
        """Return the smallest contained value and remove it."""

        val = self._min
        if val is not None:
            self._remove(val)

        return val

    def pop_max(self) -> Optional[int]:
        """Return the largest contained value and remove it."""

        val = self._max
        if val is not None:
            self._remove(val)

        return val
