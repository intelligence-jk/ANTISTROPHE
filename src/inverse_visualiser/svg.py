"""Plain SVG plot of f, f^-1 and y = x. No third-party libraries."""
from __future__ import annotations

from fractions import Fraction


def _curve(fn, lo, hi, scale, size, steps=400):
    """Polyline segments, broken where fn fails or jumps (asymptotes)."""
    segs, cur, prev = [], [], None
    for i in range(steps + 1):
        x = lo + (hi - lo) * i / steps
        try:
            y = float(fn(Fraction(x).limit_denominator(10**6)))
        except (ZeroDivisionError, ValueError):
            y = None
        if y is None or abs(y) > hi * 3 or (prev is not None and abs(y - prev) > (hi - lo) / 2):
            if len(cur) > 1:
                segs.append(cur)
            cur = []
            prev = None
            if y is None or abs(y) > hi * 3:
                continue
        cur.append((size / 2 + x * scale, size / 2 - y * scale))
        prev = y
    if len(cur) > 1:
        segs.append(cur)
    return segs


def plot_svg(f, extent: float = 8.0, size: int = 480) -> str:
    """Return SVG text for f (blue), f^-1 (orange) and y = x (grey dashed)."""
    inv = f.inverse() if not hasattr(f, "n") else f.root
    scale = size / (2 * extent)
    lo, hi = -extent, extent
    if hasattr(f, "n") and f.n % 2 == 0:
        lo_f = 0.0
    else:
        lo_f = lo
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">',
           f'<rect width="{size}" height="{size}" fill="white"/>',
           f'<line x1="0" y1="{size/2}" x2="{size}" y2="{size/2}" stroke="#999"/>',
           f'<line x1="{size/2}" y1="0" x2="{size/2}" y2="{size}" stroke="#999"/>',
           f'<line x1="0" y1="{size}" x2="{size}" y2="0" stroke="#777" stroke-dasharray="6 4"/>']
    for fn, lo_, colour in ((f, lo_f, "#1d4ed8"), (inv, 0.0 if hasattr(f, "n") and f.n % 2 == 0 else lo, "#ea580c")):
        for seg in _curve(fn, lo_, hi, scale, size):
            pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in seg)
            out.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="2"/>')
    out.append(f'<text x="8" y="16" font-family="sans-serif" font-size="12" fill="#1d4ed8">f</text>')
    out.append(f'<text x="24" y="16" font-family="sans-serif" font-size="12" fill="#ea580c">inverse of f</text>')
    out.append(f'<text x="120" y="16" font-family="sans-serif" font-size="12" fill="#777">y = x</text>')
    out.append("</svg>")
    return "\n".join(out)
