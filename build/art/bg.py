# -*- coding: utf-8 -*-
"""Dunkle Parallax-Hintergruende, einer je Seite.

Sie liegen unter einem Overlay von 74-88 % Deckung. Deshalb zaehlt hier
Struktur, nicht Motiv: ein grosses, sehr blasses Motiv, ein Raster und eine
Diagonale reichen, damit die Bewegung beim Scrollen sichtbar wird.
"""
import math, hashlib
import kart as K
from base import svg_open, grid, corner_ticks, label, FONT

BW, BH = 1920, 1280


def _seed(slug):
    return int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)


def _mono(fn, *a, **kw):
    """Zeichnet ein Motiv einfarbig hell - fuer die Silhouette."""
    keep = {k: getattr(K, k) for k in
            ("INK", "INK_SOFT", "STEEL", "STEEL_D", "TYRE", "TYRE_L",
             "RED", "RED_L", "PAPER")}
    for k in keep:
        setattr(K, k, "none")
    K.INK = "#ffffff"
    K.INK_SOFT = "#ffffff"
    K.STEEL = "none"
    K.STEEL_D = "none"
    K.TYRE = "none"
    K.TYRE_L = "#ffffff"
    K.RED = "none"
    K.RED_L = "none"
    try:
        out = fn(*a, **kw)
    finally:
        for k, v in keep.items():
            setattr(K, k, v)
    return out


def _kart_outline(s, ox, oy, flip=False):
    return _mono(K.kart_side, s, ox, oy, accent="none", pod="none",
                 number=None, flip=flip, shadow=False)


def _gear(cx, cy, r, teeth=16, col="#ffffff", op=0.1, lw=6):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" '
         f'stroke-width="{lw}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.34}" fill="none" '
         f'stroke="{col}" stroke-width="{lw}"/>']
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        o.append(f'<line x1="{cx + math.cos(a)*r:.1f}" '
                 f'y1="{cy + math.sin(a)*r:.1f}" '
                 f'x2="{cx + math.cos(a)*r*1.14:.1f}" '
                 f'y2="{cy + math.sin(a)*r*1.14:.1f}" stroke="{col}" '
                 f'stroke-width="{lw*1.6}" stroke-linecap="round"/>')
    return f'<g opacity="{op}">' + "".join(o) + "</g>"


def _cone_field(w, h, n, op=0.12):
    o = []
    for i in range(n):
        x = w * (0.06 + 0.88 * ((i * 0.37) % 1.0))
        y = h * (0.52 + 0.42 * ((i * 0.61) % 1.0))
        sc = 0.5 + 0.9 * ((i * 0.23) % 1.0)
        cw, ch = 70 * sc, 100 * sc
        o.append(f'<path d="M{x - cw*0.5:.0f} {y:.0f} L{x - cw*0.16:.0f} '
                 f'{y - ch:.0f} L{x + cw*0.16:.0f} {y - ch:.0f} '
                 f'L{x + cw*0.5:.0f} {y:.0f} Z" fill="none" stroke="#ffffff" '
                 f'stroke-width="5"/>')
    return f'<g opacity="{op}">' + "".join(o) + "</g>"


def _chassis_outline(w, h, op=0.11):
    cx, cy = w * 0.52, h * 0.50
    L, B = w * 0.70, h * 0.46
    x0, y0 = cx - L / 2, cy - B / 2
    o = [f'<path d="M{x0 + L*0.10} {y0} L{x0 + L*0.86} {y0} '
         f'Q{x0 + L} {y0} {x0 + L} {y0 + B*0.14} L{x0 + L} {y0 + B*0.86} '
         f'Q{x0 + L} {y0 + B} {x0 + L*0.86} {y0 + B} L{x0 + L*0.10} {y0 + B} '
         f'Q{x0} {y0 + B} {x0} {y0 + B*0.80} L{x0} {y0 + B*0.20} '
         f'Q{x0} {y0} {x0 + L*0.10} {y0} Z" fill="none" stroke="#ffffff" '
         f'stroke-width="9" stroke-linejoin="round"/>']
    for fx in (0.22, 0.50, 0.78):
        o.append(f'<line x1="{x0 + L*fx}" y1="{y0}" x2="{x0 + L*fx}" '
                 f'y2="{y0 + B}" stroke="#ffffff" stroke-width="7"/>')
    return f'<g opacity="{op}">' + "".join(o) + "</g>"


KINDS = ("kart", "kart_flip", "chassis", "gear", "cones", "grid", "mixed")


def background(slug, kind="kart", w=BW, h=BH):
    sd = _seed(slug)
    out = [svg_open(w, h)]
    out.append(
        '<defs>'
        '<linearGradient id="bgg" x1="0" y1="0" x2="0.35" y2="1">'
        '<stop offset="0" stop-color="#232d38"/>'
        '<stop offset="0.5" stop-color="#19212a"/>'
        '<stop offset="1" stop-color="#0f151c"/></linearGradient>'
        '<pattern id="bgh" width="26" height="26" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)">'
        '<line x1="0" y1="0" x2="0" y2="26" stroke="#ffffff" stroke-width="3" '
        'opacity="0.045"/></pattern>'
        '</defs>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#bgg)"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#bgh)"/>')
    out.append(grid(w, h, step=w / 16, color="#ffffff", op=0.07, bold_every=4,
                    bw=2.6))

    # Diagonalband in Rot - gibt beim Scrollen eine klare Kante
    ang = 18 + (sd % 10)
    out.append(f'<g opacity="0.20" transform="rotate({ang} {w*0.5} {h*0.5})">'
               f'<rect x="{-w*0.2}" y="{h*(0.20 + 0.06*(sd%5)):.0f}" '
               f'width="{w*1.5}" height="26" fill="#e22718"/>'
               f'<rect x="{-w*0.2}" y="{h*(0.20 + 0.06*(sd%5)) + 54:.0f}" '
               f'width="{w*1.5}" height="10" fill="#f0432f"/></g>')

    if kind in ("kart", "kart_flip", "mixed"):
        s = (w * (0.74 + 0.10 * ((sd >> 3) % 3))) / K.LEN
        ox = w * (0.08 + 0.05 * (sd % 3))
        oy = h * (0.80 + 0.05 * ((sd >> 5) % 2))
        out.append(f'<g opacity="0.13">'
                   + _kart_outline(s, ox, oy, flip=(kind == "kart_flip"))
                   + '</g>')
    if kind in ("gear", "mixed"):
        out.append(_gear(w * 0.80, h * 0.26, 210, 18, op=0.10))
        out.append(_gear(w * 0.92, h * 0.58, 120, 14, op=0.08))
    if kind == "chassis":
        out.append(_chassis_outline(w, h))
    if kind in ("cones",):
        out.append(_cone_field(w, h, 9))
        out.append(_chassis_outline(w, h, op=0.06))
    if kind == "grid":
        out.append(_gear(w * 0.18, h * 0.72, 260, 20, op=0.07))
        out.append(f'<g opacity="0.09">'
                   f'<circle cx="{w*0.74}" cy="{h*0.34}" r="{h*0.26}" '
                   f'fill="none" stroke="#ffffff" stroke-width="8"/>'
                   f'<circle cx="{w*0.74}" cy="{h*0.34}" r="{h*0.17}" '
                   f'fill="none" stroke="#ffffff" stroke-width="8"/></g>')

    out.append(corner_ticks(w, h, m=70, l=56, color="#ffffff", op=0.22, lw=4))
    out.append("</svg>")
    return "".join(out)
