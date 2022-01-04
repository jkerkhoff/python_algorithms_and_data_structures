from typing import Optional

from hypothesis import given, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, Bundle, initialize, rule, multiple, invariant

from tests.helpers import size_and_range_queries

from src.data_structures.union_find import UnionFind


class TestUnionFind:

    @given(st.integers(0, 1000))
    def test_init(self, size: int):
        uf = UnionFind(size)
        assert len(uf) == size
        for x in range(size):
            assert uf.find(x) == x

    @given(size_and_range_queries())
    def test_merge(self, ex):
        size, merges = ex
        uf = UnionFind(size)
        for x, y in merges:
            uf.merge(x, y)
            assert uf.find(x) == uf.find(y)
            assert not uf.merge(x, y)

    @given(st.integers(0, 1000))
    def test_make_set(self, size: int):
        uf = UnionFind(size)
        idx = uf.make_set()
        assert idx == size
        for x in range(size + 1):
            assert uf.find(x) == x


class UnionFindTester(RuleBasedStateMachine):
    union_find: Optional[UnionFind]
    sets: list[set[int]]
    size: int

    def __init__(self):
        super().__init__()
        self.union_find = None
        self.sets = []
        self.size = 0

    indices = Bundle("indices")

    @initialize(target=indices, size=st.integers(0, 50))
    def init(self, size: int):
        self.union_find = UnionFind(size)
        self.sets = [{i} for i in range(size)]
        self.size = size
        return multiple(*range(size))

    @rule(target=indices)
    def make_set(self):
        self.sets.append({self.size})
        idx = self.union_find.make_set()
        self.size += 1
        assert idx == self.size - 1
        assert self.union_find.find(idx) == idx
        return self.size - 1

    @rule(x=indices, y=indices)
    def merge(self, x: int, y: int):
        if self.sets[x] is self.sets[y]:
            assert not self.union_find.merge(x, y)
        else:
            assert self.union_find.merge(x, y)
            self.sets[x].update(self.sets[y])
            for z in self.sets[y]:
                self.sets[z] = self.sets[x]

    @rule(x=indices)
    def find(self, x: int):
        assert self.sets[x] == self.sets[self.union_find.find(x)]

    @rule(x=indices, y=indices)
    def compare_find(self, x: int, y: int):
        if self.sets[x] == self.sets[y]:
            assert self.union_find.find(x) == self.union_find.find(y)
        else:
            assert self.union_find.find(x) != self.union_find.find(y)

    @invariant()
    def correct_length(self):
        assert len(self.union_find) == self.size


TestUnionFindStateful = UnionFindTester.TestCase
