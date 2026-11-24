"""Command line: python -m inverse_visualiser rational 3 -1 1 2 [--svg out.svg]"""
import argparse
import sys
from fractions import Fraction

from .core import check_inverse, fmt_num, make_function


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="inverse_visualiser",
                                description="Find and check the inverse of a simple function.")
    p.add_argument("kind", choices=["rational", "linear", "power"],
                   help="rational a b c d = (ax+b)/(cx+d); linear m k = mx+k; power n = x^n")
    p.add_argument("numbers", nargs="+", help="coefficients (integers or fractions like 1/2)")
    p.add_argument("--svg", metavar="FILE", help="also write an SVG plot of f, its inverse and y = x")
    a = p.parse_args(argv)
    try:
        f = make_function(a.kind, *[Fraction(n) for n in a.numbers])
        res = f.solve()
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print(res.function)
    if res.inverse is None:
        print(f"No inverse: {res.reason}")
        return 1
    print(res.inverse)
    print(f"Domain of inverse: {res.domain_of_inverse}  (this is the range of f)")
    print("Steps:")
    for s in res.steps:
        print("  " + s)
    rows = check_inverse(f)
    ok = all(r[2] for r in rows)
    print(f"Check f(f^-1(x)) = x on {len(rows)} points: {'all exact' if ok else 'FAILED'}")
    for x, back, good in rows[:4]:
        print(f"  x = {fmt_num(x)}: f(f^-1(x)) = {fmt_num(back)}")
    if a.svg:
        from .svg import plot_svg
        with open(a.svg, "w", encoding="utf-8") as fh:
            fh.write(plot_svg(f))
        print(f"Wrote {a.svg}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
