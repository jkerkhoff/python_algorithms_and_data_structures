from datetime import timedelta
from itertools import tee

from hypothesis import given, strategies as st, example, settings

from src.data_structures.hash_table import HashTable

# TODO: stateful hypothesis test


class TestHashTable:

    @settings(deadline=timedelta(milliseconds=1000))
    @given(st.iterables(st.tuples(st.integers(), st.integers())))
    @example((x, x) for x in range(100000))
    def test_init(self, initializer):
        it1, it2 = tee(initializer)
        ht = HashTable(it1)
        reference = dict(it2)
        assert len(ht) == len(reference)

        for key, _ in reference.items():
            assert ht.get(key) == reference.get(key)

    @given(st.integers(), st.integers())
    def test_insert_once(self, key, value):
        ht = HashTable()
        ht.insert(key, value)
        assert ht.get(key) == value
        assert len(ht) == 1

    @given(st.integers(), st.integers())
    def test_insert_erase_once(self, key, value):
        ht = HashTable()
        ht.insert(key, value)
        assert key in ht
        ht.remove(key)
        assert key not in ht

    @settings(deadline=timedelta(milliseconds=1000))
    @given(st.iterables(st.tuples(st.integers(), st.integers())))
    @example((x, x) for x in range(100000))
    def test_insert_sequence(self, iterable):
        ht = HashTable()
        keys = set()

        for key, value in iterable:
            keys.add(key)
            ht.insert(key, value)
            assert ht.get(key) == value
            assert len(ht) == len(keys)
