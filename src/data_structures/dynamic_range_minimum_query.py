from collections.abc import Callable, Iterable
from typing import TypeVar, Generic, Optional, Union

T = TypeVar("T", int, float)

Op = Callable[[T, T], T]


class DynamicRMQ(Generic[T]):
    """Data structure for efficient dynamic range queries on an array of values.

    Supports range queries and value updates in O(lg n).
    """

    __slots__ = ("_data", "_op")

    _data: list[list[T]]
    _op: Op

    def __init__(self, iterable: Iterable[T], *, op: Optional[Op] = None):
        """Initialize the data structure for queries on the values of iterable.

        If provided, op should be a semigroup operator. By default it is the
        built-in min function.
        """
        if op is None:
            op = min

        data = [list(iterable)]
        while len(data[-1]) > 1:
            data.append([])
            for i in range(0, len(data[-2]) - 1, 2):
                data[-1].append(op(data[-2][i], data[-2][i + 1]))

            if len(data[-2]) % 2 == 1:
                data[-1].append(data[-2][-1])

        self._op = op
        self._data = data

    def __len__(self) -> int:
        return len(self._data[0])

    def __getitem__(self, idx: Union[int, slice]) -> T:
        return self._data[0][idx]

    def __setitem__(self, idx: int, value: T):
        self._data[0][idx] = value

        for level in range(1, len(self._data)):
            idx -= idx & 1
            if idx == len(self._data[level - 1]) - 1:
                self._data[level][idx // 2] = self._data[level - 1][idx]
            else:
                self._data[level][idx // 2] = self._op(
                    self._data[level - 1][idx], self._data[level - 1][idx + 1])
            idx //= 2

    @property
    def operator(self) -> Op:
        return self._op

    def query(self, left: int, right: int) -> T:
        """Perform a range query on the current values.

        Returns the same value as
            itertools.reduce(self.op, self[left:right + 1])
        """
        if left == right:
            return self._data[0][left]

        l_idx = left
        r_idx = right
        l_val = None
        r_val = None
        level = 0
        while l_idx <= r_idx:
            if l_idx & 1:
                if l_val is None:
                    l_val = self._data[level][l_idx]
                else:
                    l_val = self._op(l_val, self._data[level][l_idx])
                l_idx += 1

            if not r_idx & 1:
                if r_val is None:
                    r_val = self._data[level][r_idx]
                else:
                    r_val = self._op(self._data[level][r_idx], r_val)
                r_idx -= 1
            level += 1
            l_idx //= 2
            r_idx //= 2

        if l_val is None and r_val is None:
            return self._data[level][l_idx]

        if l_val is None:
            return r_val

        if r_val is None:
            return l_val

        return self._op(l_val, r_val)
