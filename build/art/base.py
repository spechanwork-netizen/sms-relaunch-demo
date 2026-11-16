# -*- coding: utf-8 -*-
"""Grundbausteine fuer alle Illustrationen: Papier, Raster, Boden, Bemassung."""
import math, html as _html
from kart import INK, INK_SOFT, PAPER, RED, RED_L, STEEL, STEEL_D, TYRE, TYRE_L

PAPER_2 = "#e3e6ea"
DARK    = "#161c24"
DARK_2  = "#232c37"
ON_DARK = "#d8dde4"

FONT = "Archivo, 'Archivo', Arial, Helvetica, sans-serif"


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">')


def paper(w, h, tone=PAPER):
    """Heller Grund mit ganz leichtem Verlauf."""
    return (f'<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#f6f7f9"/>'
            f'<stop offset="1" stop-color="{tone}"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#pg)"/>')


def dark_ground(w, h):
    return (f'<defs><linearGradient id="dg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#1d2630"/>'
            f'<stop offset="0.55" stop-color="#151c25"/>'
            f'<stop offset="1" stop-color="#10161d"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#dg)"/>')


def grid(w, h, step=80, color="#8d97a4", op=0.18, bold_every=5, bw=2.2):
    o = []
    i = 0
    x = 0
    while x <= w:
        strong = (i % bold_every == 0)
        o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{color}" '
                 f'stroke-width="{bw if strong else 1}" '
                 f'opacity="{op * (1.5 if strong else 1):.3f}"/>')
        x += step; i += 1
    i = 0; y = 0
    while y <= h:
        strong = (i % bold_every == 0)
        o.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{color}" '
                 f'stroke-width="{bw if strong else 1}" '
                 f'opacity="{op * (1.5 if strong else 1):.3f}"/>')
        y += step; i += 1
    return "".join(o)


def hatch_defs(color="#8d97a4", op=0.16, step=14):
    return (f'<defs><pattern id="hx" width="{step}" height="{step}" '
            f'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="{step}" stroke="{color}" '
            f'stroke-width="2" opacity="{op}"/></pattern></defs>')


def ground_line(w, y, color=INK_SOFT, op=0.5, lw=3):
    return (f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{color}" '
            f'stroke-width="{lw}" opacity="{op}"/>')


def accent_rule(x, y, w=180, color=RED, h=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'


def corner_ticks(w, h, m=46, l=38, color=INK_SOFT, op=0.45, lw=3):
    o = []
    for (cx, cy, dx, dy) in ((m, m, 1, 1), (w - m, m, -1, 1),
                             (m, h - m, 1, -1), (w - m, h - m, -1, -1)):
        o.append(f'<path d="M{cx} {cy + dy*l} L{cx} {cy} L{cx + dx*l} {cy}" '
                 f'fill="none" stroke="{color}" stroke-width="{lw}" '
                 f'opacity="{op}"/>')
    return "".join(o)


def label(x, y, text, size=26, color=INK_SOFT, weight=600, anchor="start",
          track=2.0, op=1.0):
    text = _html.escape(str(text), quote=False)
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" '
            f'letter-spacing="{track}" opacity="{op}">{text}</text>')


def callout(x1, y1, x2, y2, text, side="right", color=INK_SOFT, size=24,
            dot=True):
    """Duenne Fuehrungslinie mit Beschriftung - gibt der Grafik den
    Charakter einer technischen Zeichnung."""
    anchor = "start" if side == "right" else "end"
    tx = x2 + (16 if side == "right" else -16)
    o = [f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2.4" '
         f'fill="none" opacity="0.85"/>']
    if dot:
        o.append(f'<circle cx="{x1}" cy="{y1}" r="5.5" fill="{color}"/>')
    o.append(label(tx, y2 + size * 0.34, text, size=size, color=color,
                   weight=600, anchor=anchor, track=1.2))
    return "".join(o)


def dim_h(x1, x2, y, text, color=INK_SOFT, size=23, tick=12):
    o = [f'<path d="M{x1} {y} L{x2} {y}" stroke="{color}" stroke-width="2.2"/>',
         f'<path d="M{x1} {y-tick} L{x1} {y+tick}" stroke="{color}" stroke-width="2.2"/>',
         f'<path d="M{x2} {y-tick} L{x2} {y+tick}" stroke="{color}" stroke-width="2.2"/>']
    o.append(f'<rect x="{(x1+x2)/2 - 46}" y="{y - size*0.78}" width="92" '
             f'height="{size*1.5}" fill="{PAPER}" opacity="0.92"/>')
    o.append(label((x1 + x2) / 2, y + size * 0.36, text, size=size,
                   color=color, anchor="middle", track=0.6))
    return "".join(o)


def cone(x, y, h=86, w=62, color=RED, dark=False):
    """Pylone. (x,y) = Fusspunkt Mitte."""
    base = INK if not dark else "#0f141a"
    return (f'<g>'
            f'<ellipse cx="{x}" cy="{y}" rx="{w*0.62}" ry="{w*0.19}" '
            f'fill="#000" opacity="0.14"/>'
            f'<path d="M{x - w*0.5} {y} L{x - w*0.17} {y - h} '
            f'L{x + w*0.17} {y - h} L{x + w*0.5} {y} Z" fill="{color}" '
            f'stroke="{base}" stroke-width="3"/>'
            f'<rect x="{x - w*0.62}" y="{y - w*0.20}" width="{w*1.24}" '
            f'height="{w*0.22}" rx="{w*0.07}" fill="{color}" stroke="{base}" '
            f'stroke-width="3"/>'
            f'<rect x="{x - w*0.30}" y="{y - h*0.62}" width="{w*0.60}" '
            f'height="{h*0.16}" fill="#ffffff" opacity="0.88"/>'
            f'</g>')


_HID = [0]


def helmet(x, y, r=52, color=RED, visor="#1f2630", face_left=True,
           stripe=None):
    """Helm: Schale, Visierband (an der Schale beschnitten), Lichtkante."""
    _HID[0] += 1
    cid = f"hv{_HID[0]}"
    d = -1 if face_left else 1
    lw = max(3.0, r * 0.085)
    vy = y - r * 0.10
    vh = r * 0.62
    vx = x - r if face_left else x - r * 0.12
    o = [f'<defs><clipPath id="{cid}"><circle cx="{x}" cy="{y}" r="{r}"/>'
         f'</clipPath></defs>',
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="{INK}" '
         f'stroke-width="{lw:.1f}"/>',
         f'<g clip-path="url(#{cid})">'
         f'<rect x="{(x - r*1.25) if face_left else (x - r*0.20):.1f}" '
         f'y="{vy - vh/2:.1f}" width="{r*1.45:.1f}" '
         f'height="{vh:.1f}" rx="{vh*0.26:.1f}" fill="{visor}"/></g>',
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK}" '
         f'stroke-width="{lw:.1f}"/>',
         f'<path d="M{x + d*0.78*r:.1f} {y - 0.52*r:.1f} '
         f'A{r*0.92:.1f} {r*0.92:.1f} 0 0 {0 if face_left else 1} '
         f'{x + d*0.12*r:.1f} {y - 0.94*r:.1f}" fill="none" stroke="#ffffff" '
         f'stroke-width="{max(3, r*0.11):.1f}" opacity="0.38"/>']
    if stripe:
        o.append(f'<g clip-path="url(#{cid})"><rect x="{x - r*0.16:.1f}" '
                 f'y="{y - r*1.1:.1f}" width="{r*0.26:.1f}" '
                 f'height="{r*1.0:.1f}" fill="{stripe}"/></g>')
    return "".join(o)
