from hypothesis import given, strategies as st

from src.data_structures.polynomial import Polynomial


class TestInit:

    @given(st.lists(st.integers(), max_size=10))
    def test_correct_coefficients(self, coefficients):
        f = Polynomial(coefficients)
        if any(coefficients):
            assert f.coefficients[-1] != 0
            while coefficients and coefficients[-1] == 0:
                coefficients.pop()
            assert f.coefficients == coefficients


class TestMultiply:

    @given(st.integers(), st.lists(st.integers(), max_size=10))
    def test_scalar_commutative(self, a, f_coefficients):
        f = Polynomial(f_coefficients)
        assert a * f == f * a

    @given(st.integers(), st.lists(st.integers(), max_size=10), st.integers())
    def test_scalar_correct_eval(self, a, f_coefficients, x):
        f = Polynomial(f_coefficients)
        g = a * f
        assert g.evaluate(x) == a * f.evaluate(x)

    @given(st.integers(), st.lists(st.integers(), max_size=10))
    def test_scalar_inplace(self, a, f_coefficients):
        f = Polynomial(f_coefficients)
        g = f * a
        f *= a
        assert f == g

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_poly_commutative(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        assert f * g == g * f

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10), st.integers())
    def test_poly_correct_eval(self, f_coefficients, g_coefficients, x):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f * g
        assert h.evaluate(x) == f.evaluate(x) * g.evaluate(x)

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_poly_valid_degree(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f * g
        if -1 in (f.degree, g.degree):
            assert h.degree == -1
            assert not h.coefficients
        else:
            assert h.degree == f.degree + g.degree
            assert h.coefficients[-1] != 0

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_poly_inplace(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f * g
        f *= g
        assert f == h


class TestAdd:

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_commutative(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        assert f + g == g + f

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10), st.integers())
    def test_correct_eval(self, f_coefficients, g_coefficients, x):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f + g
        assert h.evaluate(x) == f.evaluate(x) + g.evaluate(x)

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_valid_degree(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f + g
        assert h.degree <= max(f.degree, g.degree)
        if h != 0:
            assert h.coefficients[-1] != 0

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_inplace(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f + g
        f += g
        assert f == h


class TestSubtract:

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_anticommutative(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        assert f - g == -(g - f)

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10), st.integers())
    def test_correct_eval(self, f_coefficients, g_coefficients, x):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f - g
        assert h.evaluate(x) == f.evaluate(x) - g.evaluate(x)

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_valid_degree(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f - g
        assert h.degree <= max(f.degree, g.degree)
        if h != 0:
            assert h.coefficients[-1] != 0

    @given(st.lists(st.integers(), max_size=10),
           st.lists(st.integers(), max_size=10))
    def test_inplace(self, f_coefficients, g_coefficients):
        f = Polynomial(f_coefficients)
        g = Polynomial(g_coefficients)
        h = f - g
        f -= g
        assert f == h
