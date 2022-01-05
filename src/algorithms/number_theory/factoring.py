"""Algorithms for decomposing an integer into prime factors."""


def trial_division(n: int) -> list[tuple[int, int]]:
    """Factor an integer using trial division.

    Result will be a list of (prime, exponent) tuples.

    Complexity: O(sqrt(n))

    Note that the input size is O(lg n), making the complexity exponential.
    """
    if n < 2:
        raise ValueError("input must be an integer larger than 1")

    factors = []
    i = 2
    while i * i <= n:
        count = 0
        while n % i == 0:
            count += 1
            n //= i
        if count:
            factors.append((i, count))
        i += 1
    if n != 1:
        factors.append((n, 1))
    return factors
