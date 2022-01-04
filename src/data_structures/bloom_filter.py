"""Basic implementation of a bloom filter."""
import math
import random
import array

from collections.abc import Iterator

_hash_universe = 10**18 + 3


class BitVector:
    """Set of integer keys represented as a bit vector."""

    __slots__ = ("data", )

    data: array.array

    def __init__(self, size: int):
        self.data = array.array("B", (0 for _ in range(math.ceil(size / 8))))

    def __int__(self) -> int:
        result = 0
        for word in self.data:
            result <<= 8
            result += word
        return result

    def get(self, idx: int) -> bool:
        array_idx, bit_idx = divmod(idx, 8)
        return bool(self.data[array_idx] & (1 << bit_idx))

    def set(self, idx: int, val: bool = True):
        array_idx, bit_idx = divmod(idx, 8)
        if val:
            self.data[array_idx] |= 1 << bit_idx
        else:
            self.data[array_idx] ^= self.data[array_idx] & (1 << bit_idx)


class BloomFilter:
    """Probabilistic data structure for incremental set membership queries.

    If a key has been added, it will always be recognized as a member,
    but there is a small probability of false positives.
    """

    __slots__ = ("_data", "_size", "_hash_params")

    _size: int
    _data: BitVector
    _hash_params: list[tuple[int, int]]

    def __init__(self, size: int, hash_count: int):
        self._size = size
        self._data = BitVector(size)
        self._hash_params = [(random.randrange(1, _hash_universe),
                              random.randrange(_hash_universe))
                             for _ in range(hash_count)]

    @classmethod
    def from_parameters(cls,
                        capacity: int,
                        tol: float = 1e-2) -> "BloomFilter":
        """Construct a bloom filter for the given number of elements."""
        hash_count = math.ceil(0.5 - math.log2(tol))
        size = max(
            8,
            math.ceil(0.5 - hash_count * capacity /
                      math.log1p(-1 * tol**(1 / hash_count))))
        return cls(size, hash_count)

    def _key_indices(self, key) -> Iterator[int]:
        key = hash(key)
        for a, b in self._hash_params:
            yield (a * key + b) % _hash_universe % self._size

    def add(self, key):
        for idx in self._key_indices(key):
            self._data.set(idx)

    def __contains__(self, key):
        for idx in self._key_indices(key):
            if not self._data.get(idx):
                return False
        return True
