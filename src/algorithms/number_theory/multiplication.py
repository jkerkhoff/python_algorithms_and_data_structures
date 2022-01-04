"""Integer multiplication algorithms."""


def russian_peasant_method(a: int, b: int) -> int:
    """Return the product of a and b."""
    positive = True
    if a < 0:
        a = -a
        positive = not positive
    if b < 0:
        b = -b
        positive = not positive

    result = 0
    while a:
        if a & 1:
            result += b
        a >>= 1
        b <<= 1

    return result if positive else -result
