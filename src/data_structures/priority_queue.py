"""Specification of priority queue protocol and implementations."""

from abc import abstractmethod
from collections import defaultdict, deque
from collections.abc import Iterable
from typing import TypeVar, Protocol, runtime_checkable

from src.data_structures.van_emde_boas_tree import VEBTree

K = TypeVar("K")
V = TypeVar("V")


@runtime_checkable
class PriorityQueue(Protocol[K, V]):
    """Queue that allows retrieving an item with minimal key."""

    # noinspection PyUnusedLocal
    @abstractmethod
    def __init__(self, iterable: Iterable[tuple[K, V]]):
        """Initialize a priority queue with the given key/value pairs."""
        raise NotImplementedError

    @abstractmethod
    def top(self) -> tuple[K, V] | None:
        """Return an item with minimal key.

        If the queue is empty, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def push(self, key: K, value: V) -> None:
        """Push a new key/value pair onto the queue."""
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> tuple[K, V]:
        """Remove an item with minimal key and return it."""
        raise NotImplementedError

    def pop_push(self, key: K, value: V) -> tuple[K, V]:
        """Pop, then push the given key/value pair.

        Popped key could be smaller than the one inserted.
        """
        result = self.pop()
        self.push(key, value)
        return result

    def push_pop(self, key: K, value: V) -> tuple[K, V]:
        """Push the given key/value pair, then pop.

        Popped item could be the one inserted.
        """
        self.push(key, value)
        return self.pop()

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    def __bool__(self) -> bool:
        return bool(self.__len__())


class Heap(PriorityQueue[K, V]):
    """Priority queue implemented as a min-heap."""

    __slots__ = ("_data", )

    _data: list[tuple[K, V]]

    # TODO: investigate if I'm doing this wrong
    # PyCharm complains about incompatible type
    # Pylint complains about missing super call
    def __init__(self, iterable: Iterable[tuple[K, V]] = ()):
        self._data = list(iterable)
        self._make_heap()

    def top(self) -> tuple[K, V] | None:
        return self._data[0] if self._data else None

    def push(self, key: K, value: V) -> None:
        self._data.append((key, value))
        self._fixup(len(self._data) - 1)

    def pop(self) -> tuple[K, V]:
        if not self._data:
            raise IndexError("can't pop from empty queue.")

        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        result = self._data.pop()
        if self._data:
            self._fixdown(0)

        return result

    def pop_push(self, key: K, value: V) -> tuple[K, V]:
        if not self._data:
            raise IndexError("can't pop from empty queue.")

        self._data.append((key, value))
        return self.pop()

    def push_pop(self, key: K, value: V) -> tuple[K, V]:  # TODO
        self.push(key, value)
        return self.pop()

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def _make_heap(self):
        for i in range(len(self._data) - 1, -1, -1):  # TODO efficient Floyd
            self._fixdown(i)

    def _fixup(self, idx: int):
        while idx:
            p_idx = (idx - 1) // 2
            if self._data[idx][0] < self._data[p_idx][0]:
                self._data[idx], self._data[p_idx] = self._data[
                    p_idx], self._data[idx]
                idx = p_idx
            else:
                break

    def _fixdown(self, idx: int):
        while True:
            c_idx = idx * 2 + 1

            if c_idx >= len(self._data):
                break

            if (c_idx + 1 < len(self._data)
                    and self._data[c_idx + 1][0] < self._data[c_idx][0]):
                c_idx += 1

            if self._data[c_idx][0] < self._data[idx][0]:
                self._data[c_idx], self._data[idx] = self._data[
                    idx], self._data[c_idx]
                idx = c_idx
            else:
                break


class VEBQueue(PriorityQueue[int, V]):
    """Priority queue implemented with a van Emde Boas tree."""

    __slots__ = ("_veb", "_buckets", "_size")

    _veb: VEBTree
    _buckets: defaultdict[int, deque[V]]
    _size: int

    def __init__(self,
                 iterable: Iterable[tuple[int, V]] = (),
                 priority_bound: int = 2**64):
        """Priority bound must be larger than any possible key."""
        self._veb = VEBTree(priority_bound)
        self._buckets = defaultdict(deque)
        self._size = 0

        for key, value in iterable:
            self.push(key, value)

    def top(self) -> tuple[int, V] | None:
        if self._size == 0:
            return None

        key = self._veb.min()
        val = self._buckets[key][0]
        return key, val

    def push(self, key: int, value: V) -> None:
        if key not in self._buckets:
            self._veb.add(key)
        self._buckets[key].append(value)
        self._size += 1

    def pop(self) -> tuple[int, V]:
        if self._size == 0:
            raise IndexError("can't pop from empty queue")

        key = self._veb.min()
        val = self._buckets[key].popleft()

        if not self._buckets[key]:
            del self._buckets[key]
            self._veb.pop_min()

        self._size -= 1
        return key, val

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return bool(self._size)
