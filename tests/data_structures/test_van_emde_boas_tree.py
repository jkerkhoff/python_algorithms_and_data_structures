import itertools
from typing import Optional

import pytest
from hypothesis import given, strategies as st

from src.data_structures.van_emde_boas_tree import VEBTree

# TODO: hypothesis stateful test


@st.composite
def universe_and_samples(draw: st.DrawFn,
                         max_universe: int = 2**30,
                         max_samples: Optional[int] = None,
                         unique: bool = False):
    universe = draw(st.integers(1, max_universe))
    samples = draw(
        st.iterables(st.integers(0, universe - 1),
                     max_size=max_samples,
                     unique=unique))
    return universe, samples


class TestVEBTree:

    @given(st.one_of(universe_and_samples(unique=True)))
    def test_insert_sequence(self, ex):
        universe, samples = ex

        v = VEBTree(universe)
        for value in samples:
            v.add(value)
            assert value in v

    @given(st.one_of(universe_and_samples()))
    def test_insert_remove_sequence(self, ex):
        universe, samples = ex

        it1, it2 = itertools.tee(samples)

        v = VEBTree(universe)
        for value in it1:
            if value in v:
                with pytest.raises(ValueError):
                    v.add(value)
            else:
                v.add(value)
            assert value in v

        for value in it2:
            if value not in v:
                with pytest.raises(ValueError):
                    v.remove(value)
            else:
                v.remove(value)
            assert value not in v

    @given(st.one_of(universe_and_samples()), st.booleans())
    def test_insert_pop_sequence(self, ex, pop_min):
        universe, samples = ex

        count = 0
        v = VEBTree(universe)
        for value in samples:
            if value in v:
                with pytest.raises(ValueError):
                    v.add(value)
            else:
                v.add(value)
                count += 1
            assert value in v

        for _ in range(count):
            top = v.pop_min() if pop_min else v.pop_max()
            assert top not in v
