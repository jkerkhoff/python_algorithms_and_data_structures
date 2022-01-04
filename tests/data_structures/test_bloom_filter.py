from hypothesis import given, strategies as st

from src.data_structures.bloom_filter import BloomFilter

_trials = 100
_sub_trials = 100


@given(st.integers(1, 1000), st.integers(1, 16), st.lists(st.integers()))
def test_insert(size: int, hash_count: int, keys: list):
    bf = BloomFilter(size, hash_count)

    for key in keys:
        bf.add(key)
        assert key in bf


@given(st.lists(st.integers(0)), st.floats(0.001, 0.9))
def test_error_bound(values: list, tol: float):
    n = len(values)
    false_positives = 0
    for _ in range(_trials):
        bf = BloomFilter.from_parameters(n, tol)
        for val in values:
            bf.add(val)

        for i in range(1, _sub_trials + 1):
            if -i in bf:
                false_positives += 1

    # TODO: more precise test using tail bound
    error_rate = false_positives / (_trials * _sub_trials)
    assert error_rate < 2 * tol
