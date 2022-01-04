import functools
import itertools
import math
import operator

from hypothesis import given, example, strategies as st

from src.data_structures.dynamic_range_minimum_query import DynamicRMQ
from tests.helpers import lists_and_range_queries, size_updates_and_range_queries

bool_ops = (
    None,
    max,
    min,
    operator.and_,
    operator.xor,
    operator.or_,
)

int_ops = (None, max, min, operator.add, operator.mul, operator.and_,
           operator.xor, operator.or_, math.gcd)

float_ops = (
    None,
    max,
    min,
    # operator.add,
    # operator.mul,
)


def list_and_all_queries(iterable):
    values = list(iterable)
    queries = itertools.combinations(range(len(values)), 2)
    return values, queries


# TODO: stateful hypothesis test


class TestDynamicRMQ:

    @given(st.lists(st.booleans()), st.sampled_from(bool_ops))
    def test_init_values_bool(self, values, op):
        rmq = DynamicRMQ(values, op=op)

        for i, val in enumerate(values):
            assert rmq[i] == val

    @given(st.lists(st.integers()), st.sampled_from(int_ops))
    def test_init_values_int(self, values, op):
        rmq = DynamicRMQ(values, op=op)

        for i, val in enumerate(values):
            assert rmq[i] == val

    @given(st.lists(st.floats(allow_nan=False)), st.sampled_from(float_ops))
    def test_init_values_float(self, values, op):
        rmq = DynamicRMQ(values, op=op)

        for i, val in enumerate(values):
            assert rmq[i] == val

    @given(lists_and_range_queries(st.integers()), st.sampled_from(int_ops))
    @example(list_and_all_queries(range(59)), None)
    @example(list_and_all_queries(range(59)), operator.add)
    def test_init_queries_int(self, ex, op):
        values, queries = ex
        rmq = DynamicRMQ(values, op=op)

        for start, stop in queries:
            if stop <= start:  # TODO: make this a parameter for laaq
                continue
            query_result = rmq.query(start, stop - 1)
            reduce_result = functools.reduce(op or min, values[start:stop])
            assert query_result == reduce_result

    @given(lists_and_range_queries(st.floats(allow_nan=False)),
           st.sampled_from(float_ops))
    @example(list_and_all_queries(map(math.sqrt, range(59))), None)
    @example(list_and_all_queries(map(math.sqrt, range(59))), operator.add)
    def test_init_queries_float(self, ex, op):
        values, queries = ex
        rmq = DynamicRMQ(values, op=op)

        for start, stop in queries:
            if stop <= start:  # TODO: see ^
                continue
            query_result = rmq.query(start, stop - 1)
            reduce_result = functools.reduce(op or min, values[start:stop])
            if math.isnan(reduce_result):
                assert math.isnan(query_result)
            else:
                assert math.isclose(query_result, reduce_result)

    @given(size_updates_and_range_queries(st.integers()),
           st.sampled_from(int_ops))
    def test_updates_then_queries_int(self, ex, op):
        size, updates, queries = ex

        values = [0 for _ in range(size)]
        rmq = DynamicRMQ(values, op=op)

        for idx, value in updates:
            rmq[idx] = value
            values[idx] = value
            assert rmq[idx] == value

        for start, stop in queries:
            query_result = rmq.query(start, stop)
            reduce_result = functools.reduce(op or min, values[start:stop + 1])
            assert query_result == reduce_result

    @given(size_updates_and_range_queries(st.floats(allow_nan=False)),
           st.sampled_from(float_ops))
    def test_updates_then_queries_float(self, ex, op):
        size, updates, queries = ex

        values = [.0 for _ in range(size)]
        rmq = DynamicRMQ(values, op=op)

        for idx, value in updates:
            rmq[idx] = value
            values[idx] = value
            assert rmq[idx] == value

        for start, stop in queries:
            query_result = rmq.query(start, stop)
            reduce_result = functools.reduce(op or min, values[start:stop + 1])
            if math.isnan(reduce_result):
                assert math.isnan(query_result)
            else:
                assert math.isclose(query_result, reduce_result)
