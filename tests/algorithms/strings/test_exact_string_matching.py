from hypothesis import given, strategies as st

from tests.algorithms.strings.helpers import string_with_substring
from src.algorithms.strings.exact_matching import match_brute_force


@given(st.one_of(string_with_substring(), st.tuples(st.text(), st.text())))
def test_brute_force(ex: tuple[str, str]):
    text, pattern = ex
    assert match_brute_force(text, pattern) == text.find(pattern)
