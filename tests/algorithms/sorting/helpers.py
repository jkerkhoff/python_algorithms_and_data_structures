import pytest

import itertools

from typing import Optional, Any, TypeVar, Generic
from collections.abc import Iterable, Callable

from hypothesis import strategies as st

T = TypeVar("T")


class WrappedValue(Generic[T]):
    idx: int
    value: T

    def __init__(self, idx: int, value: T):
        self.idx = idx
        self.value = value

    def __eq__(self, other) -> bool:
        if isinstance(other, WrappedValue):
            return self.value.__eq__(other.value)
        return self.value.__eq__(other)

    def __ne__(self, other) -> bool:
        if isinstance(other, WrappedValue):
            return self.value.__ne__(other.value)
        return self.value.__ne__(other)

    def __lt__(self, other) -> bool:
        if isinstance(other, WrappedValue):
            return self.value.__lt__(other.value)
        return self.value.__lt__(other)

    def __le__(self, other) -> bool:
        if isinstance(other, WrappedValue):
            return self.value.__le__(other.value)
        return self.value.__le__(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, WrappedValue):
            return self.value.__gt__(other.value)
        return self.value.__gt__(other)

    def __ge__(self, other) -> bool:
        if isinstance(other, WrappedValue):
            return self.value.__ge__(other.value)
        return self.value.__ge__(other)

    def __index__(self) -> int:
        return self.value.__index__()

    def __int__(self) -> int:
        return self.value.__int__()

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return getattr(self.value, item)

    def __repr__(self) -> str:
        return f"<{self.value}[{self.idx}]>"


@st.composite
def wrapped_value_lists(draw: st.DrawFn, *args,
                        **kwargs) -> list[WrappedValue[T]]:
    values = draw(st.lists(*args, **kwargs))
    return [WrappedValue(i, x) for i, x in enumerate(values)]


def check_sorted(iterable: Iterable[T],
                 key: Optional[Callable[[T], Any]] = None):
    __tracebackhide__ = True

    if key is None:
        key = lambda k: k

    for (i, x), (j, y) in itertools.pairwise(enumerate(iterable)):
        if key(x) > key(y):
            pytest.fail(f"not sorted: {x} appears at index {i}, "
                        f"before {y} at index {j}")


def check_stable(original: Iterable[T],
                 modified: Iterable[T],
                 key: Optional[Callable[[T], Any]] = None):
    __tracebackhide__ = True

    if key is None:
        key = lambda k: k

    for x, y in zip(sorted(original, key=key), sorted(modified, key=key)):
        if x is not y:
            pytest.fail(f"not stable: {x} appears before {y} in original, but "
                        f"not in modified")
