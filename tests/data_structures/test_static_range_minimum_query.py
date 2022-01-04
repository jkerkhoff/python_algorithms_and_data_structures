import itertools

from hypothesis import given, strategies as st

from src.data_structures.static_range_minimum_query import StaticRMQ, StaticRMQLogTable

value_strategy = st.lists(st.integers(), min_size=1)

# TODO floats, make generic maybe


@given(values=value_strategy, data=st.data())
def test_static_rmq(values: list[int], data: st.DataObject):
    n = len(values)
    rmq = StaticRMQ(values)

    for _ in range(10):
        start = data.draw(st.integers(0, n - 1))
        stop = data.draw(st.integers(start, n - 1))

        _, ground_truth = min(
            zip(values[start:stop + 1], itertools.count(start)))
        assert rmq.idx_query(start, stop) == ground_truth


@given(values=value_strategy, data=st.data())
def test_static_rmq_logtable(values: list[int], data: st.DataObject):
    n = len(values)
    rmq = StaticRMQLogTable(values)

    for _ in range(10):
        start = data.draw(st.integers(0, n - 1))
        stop = data.draw(st.integers(start, n - 1))

        _, ground_truth = min(
            zip(values[start:stop + 1], itertools.count(start)))
        assert rmq.idx_query(start, stop) == ground_truth
