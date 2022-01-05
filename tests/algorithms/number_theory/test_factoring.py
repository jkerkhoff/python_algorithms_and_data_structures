import math
from functools import cache

import pytest

from hypothesis import given, strategies as st

from src.algorithms.number_theory.factoring import trial_division


@cache
def is_prime(n: int) -> bool:
    if n in (0, 1):
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True


def verify_factorization(n: int, factors: list[tuple[int, int]]):
    prod = math.prod(p**e for p, e in factors)
    assert prod == n

    for factor, _ in factors:
        if not is_prime(factor):
            pytest.fail(f"factor {factor} is not prime")


@given(st.integers(2, 2**40))
def test_trial_division(n: int):
    factors = trial_division(n)
    verify_factorization(n, factors)
