from typing import TypeVar, Optional

from hypothesis import assume, strategies as st

T = TypeVar("T")


@st.composite
def with_index_permutation(
        draw: st.DrawFn,
        sequence: st.SearchStrategy[T]) -> tuple[T, list[int]]:
    sequence = draw(sequence)
    permutation = draw(st.permutations(range(len(sequence))))
    return sequence, permutation


@st.composite
def ordered_pairs(draw: st.DrawFn,
                  elements: st.SearchStrategy[T]) -> tuple[T, T]:
    a = draw(elements)
    b = draw(elements)
    assume(a <= b)
    return a, b


@st.composite
def index_updates(draw: st.DrawFn,
                  elements: st.SearchStrategy[T],
                  index_size: int,
                  *,
                  min_updates: int = 1,
                  max_updates: Optional[int] = None) -> list[tuple[int, T]]:
    return draw(
        st.lists(st.tuples(st.integers(0, index_size - 1), elements),
                 min_size=min_updates,
                 max_size=max_updates))


@st.composite
def size_and_index_updates(
        draw: st.DrawFn,
        elements: st.SearchStrategy[T],
        min_size: int = 1,
        max_size: int = 1025,
        *,
        min_updates: int = 1,
        max_updates: Optional[int] = None) -> tuple[int, list[tuple[int, T]]]:
    size = draw(st.integers(min_size, max_size))
    updates = draw(
        index_updates(elements,
                      size,
                      min_updates=min_updates,
                      max_updates=max_updates))
    return size, updates


@st.composite
def size_and_range_queries(
        draw: st.DrawFn,
        *,
        min_size: int = 1,
        max_size: int = 1025,
        min_queries: int = 0,
        max_queries: Optional[int] = None
) -> tuple[int, list[tuple[int, int]]]:
    size = draw(st.integers(min_size, max_size))
    queries = draw(
        st.lists(ordered_pairs(st.integers(0, size - 1)),
                 min_size=min_queries,
                 max_size=max_queries))
    return size, queries


@st.composite
def lists_and_indices(draw: st.DrawFn,
                      elements: st.SearchStrategy[T],
                      *,
                      min_size: int = 1,
                      max_size: Optional[int] = None) -> tuple[list[T], int]:
    el_list = draw(st.lists(elements, min_size=min_size, max_size=max_size))
    max_idx = len(el_list) - 1
    idx = draw(st.integers(0, max_idx))
    return el_list, idx


@st.composite
def lists_and_range_queries(
    draw: st.DrawFn,
    elements: st.SearchStrategy[T],
    *,
    min_size: int = 1,
    max_size: Optional[int] = None,
    min_queries: int = 0,
    max_queries: Optional[int] = None
) -> tuple[list[T], list[tuple[int, int]]]:
    el_list = draw(st.lists(elements, min_size=min_size, max_size=max_size))
    max_idx = len(el_list)
    queries = draw(
        st.lists(ordered_pairs(st.integers(0, max_idx)),
                 min_size=min_queries,
                 max_size=max_queries))
    return el_list, queries


@st.composite
def size_updates_and_range_queries(
    draw: st.DrawFn,
    elements: st.SearchStrategy[T],
    *,
    min_size: int = 1,
    max_size: Optional[int] = 1000,
    min_updates: int = 0,
    max_updates: Optional[int] = None,
    min_queries: int = 0,
    max_queries: Optional[int] = None
) -> tuple[int, list[tuple[int, T]], list[tuple[int, int]]]:
    size = draw(st.integers(min_size, max_size))
    max_idx = size - 1
    updates = draw(
        st.lists(st.tuples(st.integers(0, max_idx), elements),
                 min_size=min_updates,
                 max_size=max_updates))
    queries = draw(
        st.lists(ordered_pairs(st.integers(0, max_idx)),
                 min_size=min_queries,
                 max_size=max_queries))
    return size, updates, queries
