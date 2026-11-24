"""Inverse function finder and checker (exact, Fraction based)."""
from .core import (Linear, Power, Rational, check_inverse, make_function,
                   fmt_linear, fmt_num)

__all__ = ["Linear", "Power", "Rational", "check_inverse", "make_function",
           "fmt_linear", "fmt_num"]
__version__ = "0.1.0"
