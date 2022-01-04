from typing import Optional

from hypothesis import assume, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, Bundle, initialize, rule, multiple

from src.data_structures.fenwick_tree import FenwickTree

value_strategy = st.integers()
values_strategy = st.lists(value_strategy, min_size=1)


class FenwickTreeTester(RuleBasedStateMachine):
    fenwick_tree: Optional[FenwickTree]
    values: list[int]

    def __init__(self):
        super().__init__()
        self.fenwick_tree = None
        self.values = []

    indices = Bundle("indices")

    @initialize(target=indices, values=values_strategy)
    def init_values(self, values: list[int]):
        self.fenwick_tree = FenwickTree(values)
        self.values = values
        return multiple(*range(len(values)))

    @rule(idx=indices, value=value_strategy, absolute=st.booleans())
    def update(self, idx: int, value, absolute: bool):
        if absolute:
            self.values[idx] = value
        else:
            self.values[idx] += value
        self.fenwick_tree.update(idx, value, absolute)

    @rule(idx=indices, value=value_strategy, negative=st.booleans())
    def setitem(self, idx: int, value, negative: bool):
        if negative:
            idx -= len(self.values)
        self.values[idx] = value
        self.fenwick_tree[idx] = value

    @rule(idx=indices, negative=st.booleans())
    def getitem(self, idx: int, negative: bool):
        if negative:
            idx -= len(self.values)
        assert self.fenwick_tree[idx] == self.values[idx]

    @rule(length=indices)  # TODO: include full sum
    def prefix_sum(self, length: int):
        assert self.fenwick_tree.prefix_sum(length) == sum(
            self.values[:length])

    @rule(start=indices, stop=indices)
    def range_sum(self, start: int, stop: int):
        assume(start <= stop)
        stop += 1
        s = sum(self.values[start:stop])
        assert self.fenwick_tree.range_sum(start, stop) == s


TestFenwickTree = FenwickTreeTester.TestCase
