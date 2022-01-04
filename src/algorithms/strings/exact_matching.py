"""Algorithms for exact pattern matching."""


def match_brute_force(text: str, pattern: str) -> int:
    """Check if the string text contains the string pattern.

    If the pattern is found, return the first index it appears.
    If the pattern is not found, return -1.

    Complexity: O(n * m)
    """
    if not pattern:
        return 0

    n = len(text)
    m = len(pattern)
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            return i
    return -1
