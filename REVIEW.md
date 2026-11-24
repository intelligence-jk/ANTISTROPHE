# Review (24 Nov 2026)

1. Maths checked twice: PASS. Exact Fraction tests (10 tests, including (3x-1)/(x+2) giving (2x+1)/(3-x) with x != 3), plus an independent brute-force run over every (a,b,c,d) in -3..3 with ad-bc != 0: 38,636 points, g(f(x)) = x every time, and f never output the excluded value a/c.
2. Tests pass locally (10 passed) and from a clean virtualenv with `pip install -e . pytest`, as CI does. CI itself has not run: nothing is on GitHub yet.
3. No student data, no board-paper or textbook text, nothing of any other business: PASS (searched).
4. README has what it solves, a real example output, the maths: PASS.
5. MIT licence, copyright MATH and MYTH FZ-LLC: PASS (template LICENSE).
6. No em dashes, no "Dubai", no outcome promises: PASS (searched). Dependencies: standard library only, sympy and matplotlib not used.
