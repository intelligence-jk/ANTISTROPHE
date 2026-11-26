# ANTISTROPHE: the Greek choir stanza that turns back and answers the first, as an inverse answers its function

Formerly `inverse-visualiser`.

Inverse function finder and checker: swap and solve, state the domain of the inverse, and prove it with exact fractions.

## What it does
For f(x) = (ax + b)/(cx + d), and for simple linear and power functions, it finds the inverse, states the domain of the inverse (which is the range of f, so the value a/c is excluded when c is not zero), and checks f(f^-1(x)) = x on test points using Python's `Fraction`, so there is no rounding. It can also write an SVG plot of f, its inverse and the line y = x, using plain SVG text.

## Example
```bash
python -m inverse_visualiser rational 3 -1 1 2 --svg plot.svg
```
```text
f(x) = (3x - 1)/(x + 2)
f^-1(x) = (2x + 1)/(-x + 3)
Domain of inverse: x != 3  (this is the range of f)
Steps:
  1. Write y = (3x - 1)/(x + 2).
  2. Swap x and y: x = (a y + b)/(c y + d).
  3. Clear the fraction: x(y + 2) = 3y - 1.
  4. Collect the y terms: y(x - 3) = -2x - 1.
  5. Divide: y = (-2x - 1)/(x - 3), written with a tidy sign as below.
  6. y = a/c = 3 is never reached by f (it would need b*c = a*d), so the range of f is y != 3.
  7. Domain of f^-1 = range of f: x != 3. Check: the denominator of f^-1 is zero exactly at x = 3.
Check f(f^-1(x)) = x on 9 points: all exact
  x = -3: f(f^-1(x)) = -3
  x = -2: f(f^-1(x)) = -2
  x = -1: f(f^-1(x)) = -1
  x = 0: f(f^-1(x)) = 0
```

Other forms: `python -m inverse_visualiser linear 2 -3` and `python -m inverse_visualiser power 3`. Coefficients can be fractions such as 1/2.

## The maths behind it
Write y = (ax + b)/(cx + d), swap x and y, and solve for y:

    x(cy + d) = ay + b   =>   y(cx - a) = b - dx   =>   y = (-dx + b)/(cx - a)

The inverse has a zero denominator at x = a/c, so its domain is x != a/c. This matches the range of f: a value y = a/c would need bc = ad, which is exactly the constant case, so f never reaches a/c. When ad - bc = 0 the function is constant and has no inverse. For power functions, x^n with odd n is one to one on all reals; for even n we restrict to x >= 0 (a stated choice), and the inverse is the nth root. A graph of an inverse is the mirror image of f in the line y = x.

## Install and run
Python 3.10 or later. Standard library only (no sympy, no matplotlib).
```bash
python -m pip install -e .
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
