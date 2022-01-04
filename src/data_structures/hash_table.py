from collections.abc import Iterable
from itertools import count
from typing import TypeVar, Generic, Union, Optional

from enum import Enum
from random import randrange

K = TypeVar('K')
V = TypeVar('V')


class SlotIndicator(Enum):
    EMPTY = 0
    DELETED = 1


KeySlotItem = Union[V, SlotIndicator]


class ParameterizedHash:
    __slots__ = ('m', 'p', 'a', 'b')

    def __init__(self, m: int, p: int = 10**18 + 3):
        self.m = m
        self.p = p
        self.a = randrange(1, p)
        self.b = randrange(p)

    def __call__(self, key: int, probe: int) -> int:
        return (probe + (self.a * key + self.b) % self.p) % self.m


class HashTable(Generic[K, V]):
    __slots__ = ('_keys', '_values', '_size', '_capacity', '_min_capacity',
                 '_hash', '_target_load', '_min_load', '_max_load')

    def __init__(self, iterable: Iterable[tuple[K, V]] = ()):
        self._target_load = 0.35
        self._min_load = 0.20
        self._max_load = 0.80
        self._min_capacity = 8

        self._capacity = self._min_capacity
        self._keys: list[KeySlotItem] = []
        self._values: list[Optional[V]] = []

        for key, value in iterable:
            self._keys.append(key)
            self._values.append(value)

        self._size = len(self._keys)

        self._rehash(self._target_capacity())

    def _target_capacity(self) -> int:
        return max(self._min_capacity, int(self._size / self._target_load))

    def _rehash(self, new_capacity: int):
        old_keys = self._keys
        old_values = self._values

        self._capacity = new_capacity
        self._size = 0

        self._keys = [SlotIndicator.EMPTY for _ in range(new_capacity)]
        self._values = [None for _ in range(new_capacity)]

        self._hash = ParameterizedHash(new_capacity)

        for key, value in zip(old_keys, old_values):
            if not isinstance(key, SlotIndicator):
                self._insert(key, value, False)

    def _insert(self, key: K, value: V, check_rehash: bool = True):
        if not isinstance(key, int):
            raise NotImplementedError()

        for i in count():
            # TODO: when a slot is deleted, our key might still exist later in the table
            h = self._hash(key, i)

            if isinstance(self._keys[h], SlotIndicator):
                self._keys[h] = key
                self._values[h] = value
                self._size += 1
                if check_rehash:
                    self._rehash_if_necessary()
                return
            elif self._keys[h] == key:
                self._keys[h] = key
                self._values[h] = value
                return

    def _erase_key_at_index(self, idx: int) -> bool:
        if self._keys[idx] not in (SlotIndicator.EMPTY, SlotIndicator.DELETED):
            self._keys[idx] = SlotIndicator.DELETED
            self._size -= 1
            self._rehash_if_necessary()
            return True
        return False

    def remove(self, key: K) -> bool:
        if not isinstance(key, int):
            raise NotImplementedError()

        idx = self._find_key_idx(key)
        if idx is not None:
            return self._erase_key_at_index(idx)
        return False

    def _find_key_idx(self, key: K) -> Optional[int]:
        if not isinstance(key, int):
            raise NotImplementedError()

        for i in count():
            h = self._hash(key, i)

            if self._keys[h] == key:
                return h
            if self._keys[h] is SlotIndicator.EMPTY:
                return None

    def load_factor(self) -> float:
        return self._size / self._capacity

    def _rehash_if_necessary(self):
        load = self.load_factor()
        target_capacity = self._target_capacity()

        if load > self._max_load and self._capacity < target_capacity:
            self._rehash(target_capacity)
        elif load < self._min_load and self._capacity > self._min_capacity:
            self._rehash(target_capacity)

    def __len__(self):
        return self._size

    def __contains__(self, key: K) -> bool:
        return self._find_key_idx(key) is not None

    def insert(self, key: K, value: V):
        self._insert(key, value)

    def get(self, key: K) -> Optional[V]:
        idx = self._find_key_idx(key)

        if idx is None:
            return None

        return self._values[idx]
