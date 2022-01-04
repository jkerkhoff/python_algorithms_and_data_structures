"""Implementations of greatest common divisor algorithms for integers."""


def euclidean(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)
    if a < b:
        a, b = b, a

    while b:
        a -= (a // b) * b
        a, b = b, a

    return a


def binary_euclidean(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)

    if a == 0:
        return b

    if b == 0:
        return a

    a_trailing_zeros = (a & -a).bit_length() - 1
    b_trailing_zeros = (b & -b).bit_length() - 1
    a >>= a_trailing_zeros
    b >>= b_trailing_zeros

    while True:
        if a < b:
            a, b = b, a

        a -= b

        if a == 0:
            return b << min(a_trailing_zeros, b_trailing_zeros)

        a >>= (a & -a).bit_length() - 1
