# -*- coding: utf-8 -*-
"""Zeichnet das sms-Kart als Vektorgrafik.

Alle Masse in Millimetern am echten Fahrzeug, Nullpunkt vorne am Boden,
y zeigt nach oben. place() rechnet in SVG-Koordinaten um. So bleiben die
Proportionen richtig, egal in welcher Bildgroesse die Szene spaeter liegt.
"""

# --- Farben -------------------------------------------------------------
INK      = "#1f2630"   # Linien, dunkles Schiefergrau
INK_SOFT = "#5b6675"
PAPER    = "#eceef1"
RED      = "#cf1f14"
RED_L    = "#e22718"
STEEL    = "#c3c8cf"
STEEL_D  = "#9aa2ad"
TYRE     = "#2b323c"
TYRE_L   = "#3c4450"

LEN = 1900.0   # Gesamtlaenge in mm


def xf(x, y, s, ox, oy):
    """mm -> SVG. s = px pro mm, (ox,oy) = Bodenpunkt vorne in SVG."""
    return ox + x * s, oy - y * s


class Pen:
    def __init__(self, s, ox, oy, flip=False):
        self.s, self.ox, self.oy, self.flip = s, ox, oy, flip
        self.out = []

    def p(self, x, y):
        if self.flip:
            x = LEN - x
        return xf(x, y, self.s, self.ox, self.oy)

    def path(self, d, fill="none", stroke=INK, w=6, extra=""):
        self.out.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{w * self.s:.2f}" stroke-linejoin="round" '
            f'stroke-linecap="round" {extra}/>')

    def circle(self, x, y, r, fill="none", stroke=INK, w=6):
        cx, cy = self.p(x, y)
        self.out.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * self.s:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{w * self.s:.2f}"/>')

    def M(self, x, y):
        a, b = self.p(x, y)
        return f"M{a:.1f} {b:.1f}"

    def L(self, x, y):
        a, b = self.p(x, y)
        return f"L{a:.1f} {b:.1f}"

    def Q(self, x1, y1, x2, y2):
        a, b = self.p(x1, y1)
        c, d = self.p(x2, y2)
        return f"Q{a:.1f} {b:.1f} {c:.1f} {d:.1f}"

    def C(self, x1, y1, x2, y2, x3, y3):
        a, b = self.p(x1, y1); c, d = self.p(x2, y2); e, f = self.p(x3, y3)
        return f"C{a:.1f} {b:.1f} {c:.1f} {d:.1f} {e:.1f} {f:.1f}"

    def svg(self):
        return "\n".join(self.out)


def wheel(pen, cx, cy, r, rim=RED):
    """Rad in Seitenansicht: Reifen, Felgenstern, Nabe."""
    pen.circle(cx, cy, r, fill=TYRE, stroke=INK, w=5)
    pen.circle(cx, cy, r * 0.70, fill=STEEL, stroke=INK, w=5)
    pen.circle(cx, cy, r * 0.30, fill=rim, stroke=INK, w=5)
    pen.circle(cx, cy, r * 0.10, fill=INK, stroke=INK, w=3)
    # Profilrillen
    import math
    for i in range(20):
        a = i * math.pi / 10
        x1 = cx + math.cos(a) * r * 0.845
        y1 = cy + math.sin(a) * r * 0.845
        x2 = cx + math.cos(a) * r * 0.955
        y2 = cy + math.sin(a) * r * 0.955
        pen.path(pen.M(x1, y1) + pen.L(x2, y2), stroke=TYRE_L, w=4)


def kart_side(s, ox, oy, accent=RED, pod=None, number=None, flip=False,
              shadow=True, driver=False):
    """Kart von der Seite. Nase links (bzw. rechts bei flip=True)."""
    pod = pod or accent
    pen = Pen(s, ox, oy, flip)

    if shadow:
        a, b = xf(60, 0, s, ox, oy)
        c, _ = xf(1840, 0, s, ox, oy)
        pen.out.append(
            f'<ellipse cx="{(a+c)/2:.1f}" cy="{b+6*s:.1f}" rx="{(c-a)/2:.1f}" '
            f'ry="{16*s:.1f}" fill="#0d131b" opacity="0.14"/>')

    # ---- Rahmenrohre ----------------------------------------------------
    pen.path(pen.M(250, 190) + pen.C(330, 120, 420, 95, 560, 92)
             + pen.L(1300, 92) + pen.C(1480, 92, 1570, 120, 1640, 190),
             stroke=INK, w=34)
    # Bodenblech
    pen.path(pen.M(430, 100) + pen.L(1120, 100) + pen.L(1120, 62)
             + pen.L(430, 62) + "Z", fill=STEEL, stroke=INK, w=5)
    # Achsrohr hinten
    pen.path(pen.M(1310, 150) + pen.L(1660, 150), stroke=INK, w=22)

    # ---- Pedale ----------------------------------------------------------
    pen.path(pen.M(470, 105) + pen.L(500, 215), stroke=INK, w=14)
    pen.path(pen.M(500, 215) + pen.L(566, 232), stroke=INK, w=20)
    pen.path(pen.M(560, 105) + pen.L(590, 205), stroke=INK_SOFT, w=14)
    pen.path(pen.M(590, 205) + pen.L(652, 220), stroke=INK_SOFT, w=20)

    # ---- Fahrer: Beine (vom Seitenkasten teilweise verdeckt) ---------------
    if driver:
        pen.path(pen.M(1248, 232) + pen.C(1140, 268, 1010, 318, 912, 338),
                 stroke=accent, w=112)
        pen.path(pen.M(912, 338) + pen.C(820, 330, 716, 292, 648, 258),
                 stroke=accent, w=92)
        pen.path(pen.M(648, 258) + pen.L(586, 222), stroke=INK, w=56)

    # ---- Seitenkasten -----------------------------------------------------
    pen.path(pen.M(640, 85) + pen.C(650, 250, 760, 312, 900, 312)
             + pen.C(1060, 312, 1160, 250, 1170, 85) + "Z",
             fill=pod, stroke=INK, w=6)
    pen.path(pen.M(716, 170) + pen.C(790, 252, 1020, 252, 1096, 170),
             stroke="#ffffff", w=7, extra='opacity="0.38"')

    # ---- Nassau-Panel ------------------------------------------------------
    pen.path(pen.M(360, 120) + pen.C(300, 96, 150, 96, 92, 132)
             + pen.C(48, 160, 46, 262, 88, 292)
             + pen.C(150, 334, 310, 326, 364, 296) + "Z",
             fill=accent, stroke=INK, w=6)
    pen.path(pen.M(110, 252) + pen.C(176, 276, 274, 274, 338, 254),
             stroke="#ffffff", w=8, extra='opacity="0.42"')
    # Frontbuegel zum Rahmen
    pen.path(pen.M(300, 184) + pen.L(470, 150), stroke=INK, w=18)

    # ---- Fahrer: Rumpf (wird vom Sitz teilweise verdeckt) --------------------
    if driver:
        pen.path(pen.M(1352, 300)
                 + pen.C(1326, 500, 1300, 672, 1282, 772)
                 + pen.C(1268, 848, 1142, 856, 1136, 782)
                 + pen.C(1144, 660, 1176, 460, 1202, 300) + "Z",
                 fill=accent, stroke=INK, w=6)

    # ---- Sitz ---------------------------------------------------------------
    # Eine geschlossene Schale: Sitzflaeche vorn, Lehne hinten, aussen die
    # Seitenwange - genau das sieht man am Kart von der Seite.
    pen.path(pen.M(996, 256)
             + pen.C(1080, 196, 1240, 150, 1332, 150)
             + pen.C(1408, 182, 1438, 404, 1426, 586)
             + pen.C(1422, 644, 1318, 652, 1306, 596)
             + pen.C(1316, 440, 1300, 352, 1252, 318)
             + pen.C(1180, 300, 1070, 306, 1004, 322) + "Z",
             fill=STEEL, stroke=INK, w=6)
    # Seitenwange als Kante angedeutet
    pen.path(pen.M(1040, 300) + pen.C(1140, 258, 1260, 218, 1338, 214),
             stroke=INK_SOFT, w=6)
    pen.path(pen.M(1352, 240) + pen.C(1392, 364, 1398, 474, 1380, 572),
             stroke=INK_SOFT, w=6)
    # Markenstreifen auf der Lehne
    pen.path(pen.M(1336, 470) + pen.C(1396, 470, 1404, 470, 1412, 470),
             stroke=accent, w=0)
    pen.out.append('')
    pen.path(pen.M(1330, 430) + pen.L(1420, 430), stroke=accent, w=26)
    # Sitzstrebe zum Achsrohr
    pen.path(pen.M(1380, 250) + pen.L(1488, 170), stroke=INK, w=14)

    # ---- Lenkung ------------------------------------------------------------
    pen.path(pen.M(560, 150) + pen.L(1000, 530), stroke=INK, w=24)
    cx, cy = pen.p(1010, 556)
    rx, ry = 92 * s, 34 * s
    rot = 34 if not flip else -34
    pen.out.append(
        f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})">'
        f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
        f'fill="none" stroke="{INK}" stroke-width="{24*s:.2f}"/>'
        f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx*0.26:.1f}" '
        f'ry="{ry*0.34:.1f}" fill="{accent}" stroke="{INK}" '
        f'stroke-width="{7*s:.2f}"/></g>')

    # ---- Fahrer: Arme und Helm ----------------------------------------------
    if driver:
        pen.path(pen.M(1206, 782) + pen.C(1160, 740, 1078, 644, 1042, 596),
                 stroke=accent, w=54)
        pen.circle(1042, 592, 34, fill=INK, stroke=INK, w=4)
        cx, cy = pen.p(1206, 944)
        r = 112 * s
        vx = -1 if not flip else 1
        pen.out.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#f2f4f6" '
            f'stroke="{INK}" stroke-width="{6*s:.2f}"/>')
        pen.out.append(
            f'<path d="M{cx + vx*r*0.96:.1f} {cy - r*0.04:.1f} '
            f'C{cx + vx*r*0.86:.1f} {cy - r*0.50:.1f} '
            f'{cx - vx*r*0.26:.1f} {cy - r*0.56:.1f} '
            f'{cx - vx*r*0.52:.1f} {cy - r*0.14:.1f} '
            f'L{cx - vx*r*0.48:.1f} {cy + r*0.20:.1f} '
            f'C{cx - vx*r*0.06:.1f} {cy + r*0.38:.1f} '
            f'{cx + vx*r*0.72:.1f} {cy + r*0.34:.1f} '
            f'{cx + vx*r*0.96:.1f} {cy - r*0.04:.1f} Z" fill="{INK}" '
            f'opacity="0.92"/>')
        pen.out.append(
            f'<path d="M{cx - vx*r*0.26:.1f} {cy - r*0.98:.1f} '
            f'L{cx - vx*r*0.46:.1f} {cy - r*0.16:.1f}" stroke="{accent}" '
            f'stroke-width="{20*s:.2f}" stroke-linecap="round"/>')
        pen.path(pen.M(1206, 836) + pen.C(1150, 812, 1150, 790, 1152, 776),
                 stroke=INK, w=8)

    # ---- Antriebseinheit hinten ---------------------------------------------
    pen.path(pen.M(1430, 120) + pen.L(1646, 120)
             + pen.C(1676, 120, 1692, 140, 1692, 168)
             + pen.L(1692, 344) + pen.C(1692, 372, 1676, 390, 1646, 390)
             + pen.L(1460, 390) + pen.C(1434, 390, 1422, 372, 1422, 344) + "Z",
             fill=INK, stroke=INK, w=6)
    for i in range(5):
        x = 1470 + i * 46
        pen.path(pen.M(x, 168) + pen.L(x, 342), stroke=INK_SOFT, w=10)
    pen.circle(1660, 346, 24, fill=accent, stroke=PAPER, w=7)

    # ---- Stossfaenger hinten --------------------------------------------------
    pen.path(pen.M(1660, 196) + pen.L(1858, 196), stroke=INK, w=28)
    pen.path(pen.M(1848, 196) + pen.L(1848, 306), stroke=INK, w=22)
    pen.path(pen.M(1660, 306) + pen.L(1858, 306), stroke=INK, w=22)
    pen.path(pen.M(1640, 150) + pen.L(1700, 232), stroke=INK, w=16)

    # ---- Raeder ---------------------------------------------------------------
    wheel(pen, 400, 140, 140, rim=accent)
    wheel(pen, 1490, 152, 152, rim=accent)

    # ---- Startnummer ------------------------------------------------------------
    if number:
        cx, cy = pen.p(900, 190)
        pen.out.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{74*s:.1f}" fill="#ffffff" '
            f'stroke="{INK}" stroke-width="{7*s:.2f}"/>'
            f'<text x="{cx:.1f}" y="{cy + 28*s:.1f}" text-anchor="middle" '
            f'font-family="Archivo, Arial, Helvetica, sans-serif" '
            f'font-weight="700" font-size="{82*s:.1f}" fill="{INK}">{number}</text>')

    return pen.svg()
