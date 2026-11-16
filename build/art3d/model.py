# -*- coding: utf-8 -*-
"""Das sms-Kart als 3D-Modell, Masse in Metern.

Nullpunkt: Nase am Boden. x laeuft nach hinten, y nach oben, z zur Seite.
Laenge 1,90 m · Radstand 1,12 m · Spur vorn 1,00 / hinten 1,24 m ·
Raeder 280 mm vorn, 300 mm hinten.
"""
import numpy as np
from r3d import (Mesh, mat, hexcol, box, rbox, lathe, extrude, tube, mat4, F32)

# ------------------------------------------------------------- Materialien
M_TYRE  = mat(hexcol("#15181c"), spec=0.16, shin=16)
M_RIM   = mat(hexcol("#aeb5bd"), spec=0.62, shin=96, metal=0.85)
M_HUB   = mat(hexcol("#5f6670"), spec=0.45, shin=60, metal=0.6)
M_FRAME = mat(hexcol("#23272d"), spec=0.26, shin=34)
M_ALU   = mat(hexcol("#9aa1a9"), spec=0.48, shin=74, metal=0.65)
M_SEAT  = mat(hexcol("#1d2026"), spec=0.22, shin=26)
M_DARK  = mat(hexcol("#121519"), spec=0.30, shin=40)
M_WHITE = mat(hexcol("#e8eaed"), spec=0.40, shin=60)

WB_F, WB_R = 0.40, 1.52          # Radmitten vorne / hinten
TR_F, TR_R = 0.50, 0.62          # halbe Spur
R_F, R_R = 0.14, 0.15
W_F, W_R = 0.135, 0.215


def _tyre_profile(r, w):
    """Reifen als Ring - innen offen, damit die Felge sichtbar bleibt."""
    h = w / 2
    ri = r * 0.60
    p = [(ri, -h), (r * 0.82, -h), (r * 0.95, -h * 0.90), (r * 0.995, -h * 0.58),
         (r, -h * 0.20), (r, h * 0.20), (r * 0.995, h * 0.58),
         (r * 0.95, h * 0.90), (r * 0.82, h), (ri, h), (ri, -h)]
    return p


def wheel(x, z, r, w, accent, outward=1, seg=44):
    """outward: +1 wenn die Felgenschuessel nach +z zeigt."""
    out = []
    h = w / 2
    out.append(lathe(_tyre_profile(r, w), seg, "z", (x, r, z), M_TYRE,
                     smooth=False))
    o = outward
    rim = [(0.0, o * h * 0.30), (r * 0.26, o * h * 0.42),
           (r * 0.46, o * h * 0.72), (r * 0.605, o * h * 0.90),
           (r * 0.615, o * h * 0.62), (r * 0.615, -o * h * 0.98),
           (r * 0.40, -o * h * 0.96), (0.0, -o * h * 0.70)]
    out.append(lathe(rim, seg, "z", (x, r, z), M_RIM, smooth=False))
    nut = [(0.0, o * h * 0.46), (r * 0.115, o * h * 0.46),
           (r * 0.125, o * h * 0.30), (0.0, o * h * 0.30)]
    out.append(lathe(nut, 20, "z", (x, r, z),
                     mat(accent, spec=0.55, shin=80), smooth=False))
    return out


def kart(accent="#cf1f14", pod=None, seat_col=None, driver=False):
    A = hexcol(accent)
    P = hexcol(pod) if pod else A
    M_BODY = mat(A, spec=0.72, shin=130)
    M_POD = mat(P, spec=0.70, shin=120)
    m = []

    # ---- Bodenblech ------------------------------------------------------
    m.append(box(0.86, 0.016, 0.50, (0.84, 0.052, 0.0), material=M_ALU))

    # ---- Rahmenrohre -----------------------------------------------------
    rail = [(0.30, 0.165, 0.0), (0.46, 0.082, 0.0), (1.22, 0.072, 0.0),
            (1.46, 0.092, 0.0), (1.62, 0.158, 0.0)]
    for sz in (-1, 1):
        pts = [(x, y, sz * (0.255 if i in (1, 2, 3) else 0.165))
               for i, (x, y, _) in enumerate(rail)]
        for a, b in zip(pts[:-1], pts[1:]):
            m.append(tube(a, b, 0.017, 14, M_FRAME))
    for x, y, zz in ((0.47, 0.085, 0.25), (0.96, 0.075, 0.25),
                     (1.30, 0.078, 0.25), (1.56, 0.12, 0.21)):
        m.append(tube((x, y, -zz), (x, y, zz), 0.015, 12, M_FRAME))
    # Achsrohre
    m.append(tube((WB_F, 0.148, -TR_F + 0.05), (WB_F, 0.148, TR_F - 0.05),
                  0.016, 14, M_FRAME))
    m.append(tube((WB_R, 0.150, -TR_R - 0.03), (WB_R, 0.150, TR_R + 0.03),
                  0.021, 16, M_HUB))
    # Achsschenkel vorne
    for sz in (-1, 1):
        m.append(tube((WB_F, 0.148, sz * (TR_F - 0.05)),
                      (WB_F, 0.14, sz * TR_F), 0.022, 10, M_FRAME))

    # ---- Nassau-Panel ----------------------------------------------------
    m.append(rbox(0.34, 0.155, 0.72, 0.030, (0.20, 0.205, 0.0), seg=10,
                  material=M_BODY))
    m.append(rbox(0.20, 0.05, 0.66, 0.016, (0.16, 0.132, 0.0), seg=6,
                  material=M_BODY))
    for sz in (-1, 1):
        m.append(tube((0.30, 0.165, sz * 0.165), (0.46, 0.14, sz * 0.30),
                      0.014, 10, M_FRAME))
    # Frontspoiler
    m.append(tube((0.13, 0.115, -0.33), (0.13, 0.115, 0.33), 0.016, 12, M_FRAME))
    for sz in (-1, 1):
        m.append(tube((0.13, 0.115, sz * 0.33), (0.40, 0.095, sz * 0.26),
                      0.015, 10, M_FRAME))

    # ---- Seitenkaesten ---------------------------------------------------
    for sz in (-1, 1):
        m.append(rbox(0.74, 0.145, 0.20, 0.028, (0.92, 0.122, sz * 0.325),
                      seg=9, material=M_POD))
        m.append(tube((0.62, 0.095, sz * 0.25), (0.70, 0.12, sz * 0.33),
                      0.012, 8, M_FRAME))
        m.append(tube((1.22, 0.095, sz * 0.25), (1.14, 0.12, sz * 0.33),
                      0.012, 8, M_FRAME))

    # ---- Sitz ------------------------------------------------------------
    prof = [(0.99, 0.108), (1.31, 0.098), (1.385, 0.150), (1.44, 0.33),
            (1.468, 0.55), (1.455, 0.608), (1.385, 0.612), (1.358, 0.545),
            (1.336, 0.37), (1.292, 0.225), (1.19, 0.188), (1.01, 0.182)]
    SC = mat(hexcol(seat_col), spec=0.3, shin=36) if seat_col else M_SEAT
    m.append(extrude(prof, 0.345, (0.0, 0.0, 0.0), SC, plane="xy"))
    for sz in (-1, 1):                       # Seitenwangen
        m.append(extrude([(1.01, 0.178), (1.29, 0.195), (1.345, 0.29),
                          (1.40, 0.545), (1.335, 0.552), (1.30, 0.30),
                          (1.25, 0.238), (1.01, 0.222)],
                         0.034, (0.0, 0.0, sz * 0.186), SC, plane="xy"))
    m.append(tube((1.42, 0.30, -0.16), (1.52, 0.17, -0.18), 0.012, 8, M_FRAME))
    m.append(tube((1.42, 0.30, 0.16), (1.52, 0.17, 0.18), 0.012, 8, M_FRAME))

    # ---- Lenkung ---------------------------------------------------------
    col_a, col_b = (0.56, 0.155, 0.0), (1.01, 0.60, 0.0)
    m.append(tube(col_a, col_b, 0.015, 12, M_FRAME))
    d = np.array(col_b, F32) - np.array(col_a, F32)
    d = d / np.linalg.norm(d)
    ry = float(np.arctan2(d[0], d[2]))
    rx = float(-np.arcsin(np.clip(d[1], -1, 1)))
    ring = lathe([(0.135 + 0.013 * np.cos(t), 0.013 * np.sin(t))
                  for t in np.linspace(0, 2 * np.pi, 13)], 32, "z",
                 (0, 0, 0), mat(hexcol("#1a1d22"), spec=0.4, shin=50))
    ring.transform(mat4(t=col_b, rx=rx, ry=ry))
    m.append(ring)
    hubp = lathe([(0, -0.012), (0.045, -0.012), (0.05, 0.004), (0, 0.004)],
                 20, "z", (0, 0, 0), mat(A, spec=0.5, shin=70))
    hubp.transform(mat4(t=col_b, rx=rx, ry=ry))
    m.append(hubp)

    # ---- Pedale ----------------------------------------------------------
    for sz, col in ((-1, M_DARK), (1, mat(A, spec=0.45, shin=60))):
        m.append(tube((0.50, 0.075, sz * 0.10), (0.56, 0.17, sz * 0.10),
                      0.010, 8, M_FRAME))
        m.append(box(0.055, 0.015, 0.05, (0.585, 0.185, sz * 0.10),
                     material=col))

    # ---- Antriebseinheit --------------------------------------------------
    m.append(rbox(0.33, 0.25, 0.40, 0.022, (1.53, 0.26, 0.0), seg=7,
                  material=M_DARK))
    m.append(box(0.30, 0.012, 0.36, (1.53, 0.392, 0.0),
                 material=mat(hexcol('#6e757e'), spec=0.4, shin=60, metal=0.5)))
    m.append(lathe([(0, -0.085), (0.075, -0.085), (0.082, -0.07),
                    (0.082, 0.07), (0.075, 0.085), (0, 0.085)], 28, "z",
                   (1.40, 0.175, 0.255), M_HUB))
    m.append(lathe([(0, -0.012), (0.075, -0.012), (0.075, 0.012), (0, 0.012)],
                   28, "z", (WB_R, 0.150, 0.29), M_RIM))
    m.append(tube((1.40, 0.175, 0.255), (WB_R, 0.150, 0.29), 0.010, 8, M_FRAME))
    m.append(lathe([(0, -0.018), (0.022, -0.018), (0.024, 0.0), (0, 0.0)],
                   16, "z", (1.695, 0.30, 0.0), mat(A, spec=0.5, shin=70)))

    # ---- Stossfaenger hinten ----------------------------------------------
    m.append(tube((1.62, 0.158, -0.33), (1.62, 0.158, 0.33), 0.016, 12, M_FRAME))
    m.append(tube((1.62, 0.158, -0.33), (1.84, 0.20, -0.30), 0.016, 12, M_FRAME))
    m.append(tube((1.62, 0.158, 0.33), (1.84, 0.20, 0.30), 0.016, 12, M_FRAME))
    m.append(tube((1.84, 0.20, -0.30), (1.84, 0.20, 0.30), 0.016, 12, M_FRAME))
    m.append(tube((1.84, 0.30, -0.28), (1.84, 0.30, 0.28), 0.014, 10, M_FRAME))
    for sz in (-1, 1):
        m.append(tube((1.84, 0.20, sz * 0.29), (1.84, 0.30, sz * 0.28),
                      0.012, 8, M_FRAME))

    # ---- Raeder ------------------------------------------------------------
    for sz in (-1, 1):
        m += wheel(WB_F, sz * TR_F, R_F, W_F, A, outward=sz)
        m += wheel(WB_R, sz * TR_R, R_R, W_R, A, outward=sz)

    if driver:
        m += _driver(A)
    return [x for x in m if x is not None]


def _driver(accent):
    """Fahrer als einfache, aber plausible Silhouette."""
    SUIT = mat(accent * 0.9, spec=0.22, shin=24)
    HELM = mat(hexcol("#e9ebee"), spec=0.65, shin=120)
    VIS = mat(hexcol("#101317"), spec=0.8, shin=160)
    m = []
    m.append(rbox(0.30, 0.46, 0.40, 0.12, (1.26, 0.44, 0.0), seg=6,
                  material=SUIT))                                   # Rumpf
    m.append(rbox(0.52, 0.20, 0.38, 0.09, (0.95, 0.26, 0.0), seg=6,
                  material=SUIT))                                   # Oberschenkel
    m.append(rbox(0.34, 0.16, 0.34, 0.07, (0.66, 0.22, 0.0), seg=5,
                  material=SUIT))                                   # Unterschenkel
    for sz in (-1, 1):                                              # Arme
        m.append(tube((1.22, 0.60, sz * 0.17), (1.03, 0.60, sz * 0.13),
                      0.045, 12, SUIT))
    m.append(lathe([(0, -0.115), (0.085, -0.115), (0.115, -0.07),
                    (0.125, 0.0), (0.115, 0.07), (0.085, 0.115), (0, 0.115)],
                   32, "z", (1.30, 0.80, 0.0), HELM))
    m.append(rbox(0.10, 0.11, 0.21, 0.035, (1.195, 0.805, 0.0), seg=5,
                  material=VIS))
    return m
