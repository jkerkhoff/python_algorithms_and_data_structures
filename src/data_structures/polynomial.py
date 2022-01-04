"""Implementation of a univariate polynomial type with standard operations."""

import copy
from collections.abc import Iterable
from numbers import Complex
from typing import Union


class Polynomial:
    """Univariate polynomial type."""
    __slots__ = ("coefficients", )

    coefficients: list[Complex]

    def __init__(self, coefficients: Iterable[Complex] = ()):
        self.coefficients = list(coefficients)
        self.trim()

    def trim(self) -> None:
        while self.coefficients and self.coefficients[-1] == 0:
            self.coefficients.pop()

    def evaluate(self, x: Complex):
        result = 0
        for c in reversed(self.coefficients):
            result *= x
            result += c
        return result

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    def __eq__(self, other: Union["Polynomial", Complex]) -> bool:
        if isinstance(other, Complex):
            if other == 0:
                return not self.coefficients
            return self.coefficients and self.coefficients[0] == other

        return self.coefficients == other.coefficients

    def __bool__(self) -> bool:
        return bool(self.coefficients)

    def __add__(self, other: "Polynomial") -> "Polynomial":
        result = copy.deepcopy(self)
        result += other
        return result

    def __iadd__(self, other: "Polynomial") -> "Polynomial":
        m = min(len(other.coefficients), len(self.coefficients))
        if len(other.coefficients) > m:
            self.coefficients.extend(other.coefficients[m:])
        for i in range(m):
            self.coefficients[i] += other.coefficients[i]
        self.trim()
        return self

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        result = copy.deepcopy(self)
        result -= other
        return result

    def __isub__(self, other: "Polynomial") -> "Polynomial":
        m = min(len(other.coefficients), len(self.coefficients))
        for i in range(m):
            self.coefficients[i] -= other.coefficients[i]
        for i in range(m, len(other.coefficients)):
            self.coefficients.append(other.coefficients[i] * -1)
        self.trim()
        return self

    def __neg__(self) -> "Polynomial":
        return Polynomial(-x for x in self.coefficients)

    def __mul__(self, other: Union["Polynomial", Complex]) -> "Polynomial":
        result = copy.deepcopy(self)
        result *= other
        return result

    def __rmul__(self, other: Union["Polynomial", Complex]) -> "Polynomial":
        return self * other

    def __imul__(self, other: Union["Polynomial", Complex]) -> "Polynomial":
        if other == 0:
            self.coefficients.clear()
            return self

        if not self.coefficients:
            return self

        if isinstance(other, Complex):
            for i in range(len(self.coefficients)):
                self.coefficients[i] *= other
        else:
            old_degree = self.degree
            new_degree = old_degree + other.degree
            coefficients = self.coefficients[:]
            self.coefficients.extend(0 for _ in range(other.degree))
            for k in range(new_degree + 1):
                c = 0
                for i in range(max(0, k - other.degree),
                               min(k, old_degree) + 1):
                    c += coefficients[i] * other.coefficients[k - i]
                self.coefficients[k] = c

        return self

    def __repr__(self) -> str:
        return f"Polynomial({self.coefficients})"
