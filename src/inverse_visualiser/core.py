"""Exact inverse of rational-linear, linear and power functions."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Union

Num = Union[int, Fraction, str]


def F(v: Num) -> Fraction:
    return v if isinstance(v, Fraction) else Fraction(v)


def fmt_num(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def fmt_linear(p: Fraction, q: Fraction, var: str = "x") -> str:
    """Format p*var + q, e.g. 3x - 1, -x + 3, 5."""
    parts = ""
    if p != 0:
        mag = abs(p)
        coef = "" if mag == 1 else (fmt_num(mag) if mag.denominator == 1 else f"({fmt_num(mag)})")
        parts = ("-" if p < 0 else "") + coef + var
    if q != 0 or p == 0:
        if parts == "":
            parts = fmt_num(q)
        else:
            parts += (" - " if q < 0 else " + ") + fmt_num(abs(q))
    return parts


@dataclass
class Result:
    """What the finder reports."""
    function: str
    inverse: Optional[str]
    domain_of_inverse: str
    range_of_f: str
    steps: List[str]
    reason: Optional[str] = None  # set when no inverse exists


class Rational:
    """f(x) = (a x + b) / (c x + d)."""

    def __init__(self, a: Num, b: Num, c: Num, d: Num):
        self.a, self.b, self.c, self.d = F(a), F(b), F(c), F(d)

    def __str__(self) -> str:
        if self.c == 0:
            return f"f(x) = ({fmt_linear(self.a, self.b)})/{fmt_num(self.d)}"
        return f"f(x) = ({fmt_linear(self.a, self.b)})/({fmt_linear(self.c, self.d)})"

    @property
    def det(self) -> Fraction:
        return self.a * self.d - self.b * self.c

    def __call__(self, x: Num) -> Fraction:
        x = F(x)
        den = self.c * x + self.d
        if den == 0:
            raise ZeroDivisionError("x is outside the domain of f")
        return (self.a * x + self.b) / den

    def inverse_coeffs(self):
        """(p, q, r, s) with f^-1(x) = (p x + q)/(r x + s), normalised."""
        p, q, r, s = -self.d, self.b, self.c, -self.a
        if s < 0 or (s == 0 and r < 0):
            p, q, r, s = -p, -q, -r, -s
        return p, q, r, s

    def inverse(self) -> "Rational":
        if self.det == 0:
            raise ValueError("f is constant (ad - bc = 0), so it has no inverse")
        if self.c == 0 and self.a == 0:
            raise ValueError("f is constant, so it has no inverse")
        return Rational(*self.inverse_coeffs())

    def excluded_input(self) -> Optional[Fraction]:
        return None if self.c == 0 else -self.d / self.c

    def excluded_output(self) -> Optional[Fraction]:
        return None if self.c == 0 else self.a / self.c

    def solve(self) -> Result:
        a, b, c, d = self.a, self.b, self.c, self.d
        if self.det == 0 or (c == 0 and a == 0):
            return Result(str(self), None, "none", "a single value", [],
                          "ad - bc = 0 makes f a constant (or undefined), so it is not one-to-one.")
        inv = self.inverse()
        ex = self.excluded_output()
        steps = [
            f"1. Write y = ({fmt_linear(a, b)})/({fmt_linear(c, d)}).",
            "2. Swap x and y: x = (a y + b)/(c y + d).",
            f"3. Clear the fraction: x({fmt_linear(c, d, 'y')}) = {fmt_linear(a, b, 'y')}.",
            f"4. Collect the y terms: y({fmt_linear(c, -a, 'x')}) = {fmt_linear(-d, b, 'x')}.",
            f"5. Divide: y = ({fmt_linear(-d, b)})/({fmt_linear(c, -a)}), written with a tidy sign as below.",
        ]
        if c == 0:
            dom = "all real x"
            rng = "all real y"
            steps.append("6. c = 0, so f is linear: its range is all reals and nothing is excluded.")
        else:
            dom = f"x != {fmt_num(ex)}"
            rng = f"y != {fmt_num(ex)}"
            steps.append(f"6. y = a/c = {fmt_num(ex)} is never reached by f (it would need b*c = a*d), "
                         f"so the range of f is y != {fmt_num(ex)}.")
            steps.append(f"7. Domain of f^-1 = range of f: {dom}. "
                         f"Check: the denominator of f^-1 is zero exactly at x = {fmt_num(ex)}.")
        p, q, r, s = self.inverse_coeffs()
        text = (f"f^-1(x) = ({fmt_linear(p, q)})/({fmt_linear(r, s)})" if c != 0
                else f"f^-1(x) = {fmt_linear(p / s, q / s)}")
        return Result(str(self), text, dom, rng, steps)


class Linear:
    """f(x) = m x + k."""

    def __init__(self, m: Num, k: Num):
        self.m, self.k = F(m), F(k)

    def __str__(self) -> str:
        return f"f(x) = {fmt_linear(self.m, self.k)}"

    def __call__(self, x: Num) -> Fraction:
        return self.m * F(x) + self.k

    def inverse(self) -> "Linear":
        if self.m == 0:
            raise ValueError("m = 0 makes f constant, so it has no inverse")
        return Linear(1 / self.m, -self.k / self.m)

    def solve(self) -> Result:
        if self.m == 0:
            return Result(str(self), None, "none", "a single value", [],
                          "m = 0 makes f constant, so it is not one-to-one.")
        inv = self.inverse()
        steps = [
            f"1. Write y = {fmt_linear(self.m, self.k)}.",
            "2. Swap x and y: x = m y + k.",
            f"3. Solve for y: y = (x - ({fmt_num(self.k)}))/({fmt_num(self.m)}).",
        ]
        return Result(str(self), f"f^-1(x) = {fmt_linear(inv.m, inv.k)}", "all real x", "all real y", steps)


class Power:
    """f(x) = x^n for a positive integer n.

    Odd n is one-to-one on all reals. Even n is not, so we restrict to x >= 0
    (the usual choice), which gives the inverse x^(1/n) with domain x >= 0.
    """

    def __init__(self, n: int):
        if int(n) != n or n < 1:
            raise ValueError("n must be a positive integer")
        self.n = int(n)

    def __str__(self) -> str:
        return f"f(x) = x^{self.n}" + (" for x >= 0" if self.n % 2 == 0 else "")

    def __call__(self, x: Num) -> Fraction:
        x = F(x)
        if self.n % 2 == 0 and x < 0:
            raise ValueError("outside the restricted domain x >= 0")
        return x ** self.n

    def root(self, y: Num) -> Fraction:
        """Exact n-th root of y when y is a perfect n-th power of a rational."""
        y = F(y)
        if self.n % 2 == 0 and y < 0:
            raise ValueError("no real root")
        sign = -1 if y < 0 else 1
        num, den = _iroot(abs(y.numerator), self.n), _iroot(y.denominator, self.n)
        if num is None or den is None:
            raise ValueError("not a perfect power; no exact rational root")
        return sign * Fraction(num, den)

    def inverse(self):
        return self.root

    def solve(self) -> Result:
        n = self.n
        even = n % 2 == 0
        steps = [f"1. Write y = x^{n}.", f"2. Swap x and y: x = y^{n}.",
                 f"3. Take the {n}th root: y = x^(1/{n})."]
        if even:
            steps.insert(0, f"0. x^{n} is not one-to-one on all reals (x and -x agree), so restrict to x >= 0.")
            return Result(str(self), f"f^-1(x) = x^(1/{n})", "x >= 0", "y >= 0", steps)
        return Result(str(self), f"f^-1(x) = x^(1/{n})", "all real x", "all real y", steps)


def _iroot(v: int, n: int) -> Optional[int]:
    if v < 2:
        return v
    lo, hi = 1, 1 << (v.bit_length() // n + 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** n < v:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo ** n == v else None


def check_inverse(f, points=None) -> List[tuple]:
    """Return [(x, f(f^-1(x)), ok)] on test points inside the domain of f^-1.

    Every comparison uses Fraction, so there is no rounding.
    """
    out = []
    if isinstance(f, Power):
        pts = points if points is not None else [Fraction(k) ** f.n for k in (0, 1, 2, 3)] + [Fraction(1, 8) ** f.n]
        for x in pts:
            x = F(x)
            try:
                back = f(f.root(x))
            except ValueError:
                continue
            out.append((x, back, back == x))
        return out
    inv = f.inverse()
    pts = points if points is not None else [-3, -2, -1, 0, 1, 2, 3, 5, Fraction(1, 2), Fraction(7, 3)]
    for x in pts:
        x = F(x)
        try:
            back = f(inv(x))
        except ZeroDivisionError:
            continue  # x outside the domain of f^-1
        out.append((x, back, back == x))
    return out


def make_function(kind: str, *args: Num):
    kind = kind.lower()
    if kind == "rational" and len(args) == 4:
        return Rational(*args)
    if kind == "linear" and len(args) == 2:
        return Linear(*args)
    if kind == "power" and len(args) == 1:
        return Power(int(args[0]))
    raise ValueError("use: rational a b c d | linear m k | power n")
