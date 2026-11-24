from fractions import Fraction as Fr

import pytest

from inverse_visualiser import Linear, Power, Rational, check_inverse
from inverse_visualiser.__main__ import main
from inverse_visualiser.svg import plot_svg


def test_headline_case():
    f = Rational(3, -1, 1, 2)
    r = f.solve()
    assert r.inverse == "f^-1(x) = (2x + 1)/(-x + 3)"
    assert r.domain_of_inverse == "x != 3"
    assert f.inverse_coeffs() == (2, 1, -1, 3)


def test_headline_values_exact():
    f, g = Rational(3, -1, 1, 2), Rational(3, -1, 1, 2).inverse()
    for x in [0, 1, 2, 5, -4, Fr(1, 3)]:
        assert g(x) == (2 * Fr(x) + 1) / (3 - Fr(x))
        assert f(g(x)) == x
    with pytest.raises(ZeroDivisionError):
        g(3)


def test_inverse_is_its_own_inverse_pair():
    f = Rational(2, 3, 5, -1)
    g = f.inverse()
    for x in [-2, 0, 1, 4, Fr(3, 7)]:
        assert g(f(x)) == x if f.c * x + f.d != 0 else True


def test_self_inverse_function():
    f = Rational(1, 0, 1, -1)  # x/(x-1) is its own inverse
    assert all(f.inverse()(x) == f(x) for x in [2, 3, -1, Fr(1, 2)])
    for x in [2, 3, -1, Fr(1, 2)]:
        assert f(f(x)) == x


def test_reciprocal_excluded_value_zero():
    r = Rational(0, 1, 1, 0).solve()  # 1/x
    assert r.domain_of_inverse == "x != 0"


def test_linear_case():
    f = Linear(2, -3)
    g = f.inverse()
    assert (g.m, g.k) == (Fr(1, 2), Fr(3, 2))
    assert f.solve().inverse == "f^-1(x) = (1/2)x + 3/2"
    assert all(ok for _, _, ok in check_inverse(f))


def test_rational_with_c_zero_acts_linear():
    f = Rational(4, 2, 0, 2)  # 2x + 1
    assert f.solve().domain_of_inverse == "all real x"
    assert all(ok for _, _, ok in check_inverse(f))


def test_power_odd_and_even():
    assert Power(3).root(Fr(-8, 27)) == Fr(-2, 3)
    assert Power(3).solve().domain_of_inverse == "all real x"
    r = Power(2).solve()
    assert r.domain_of_inverse == "x >= 0"
    with pytest.raises(ValueError):
        Power(2).root(2)  # not a perfect square
    with pytest.raises(ValueError):
        Power(2).root(-4)
    assert all(ok for _, _, ok in check_inverse(Power(4)))


def test_no_inverse_when_constant():
    assert Rational(2, 4, 1, 2).solve().inverse is None  # ad - bc = 0
    assert Linear(0, 5).solve().inverse is None
    with pytest.raises(ValueError):
        Rational(2, 4, 1, 2).inverse()


def test_cli_and_svg(tmp_path, capsys):
    out = tmp_path / "p.svg"
    assert main(["rational", "3", "-1", "1", "2", "--svg", str(out)]) == 0
    text = capsys.readouterr().out
    assert "Domain of inverse: x != 3" in text
    assert out.read_text().startswith("<svg")
    assert "<polyline" in plot_svg(Linear(1, 1))
