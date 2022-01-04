from typing import Optional

from hypothesis import strategies as st

from tests.helpers import ordered_pairs


@st.composite
def string_with_substring(draw: st.DrawFn,
                          min_length: int = 0,
                          max_length: Optional[int] = None):
    text = draw(st.text(min_size=min_length, max_size=max_length))
    start, stop = draw(ordered_pairs(st.integers(0, len(text))))
    pattern = text[start:stop]
    return text, pattern
