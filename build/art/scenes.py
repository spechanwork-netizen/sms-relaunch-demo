# -*- coding: utf-8 -*-
"""Die einzelnen Bildmotive. Jede Funktion liefert ein fertiges SVG."""
import math, random
from base import *
import kart as K

W, H = 1600, 1000


def _wrap(body, w=W, h=H, dark=False):
    bg = dark_ground(w, h) if dark else paper(w, h)
    return svg_open(w, h) + bg + body + "</svg>"


def _stage(w=W, h=H, horizon=0.66):
    """Heller Studio-Hintergrund: Raster, Horizontband, Bodenlinie."""
    y = h * horizon
    return ("".join([
        grid(w, h, step=w / 20, op=0.13),
        f'<rect x="0" y="{y:.0f}" width="{w}" height="{h - y:.0f}" '
        f'fill="#dfe3e8" opacity="0.75"/>',
        ground_line(w, y, op=0.35),
        corner_ticks(w, h),
    ]), y)


# ---------------------------------------------------------------- Kart pur
def kart_studio(number=None, accent=K.RED, pod=None, flip=False,
                caption=None, w=W, h=H):
    stage, y = _stage(w, h, 0.70)
    s = (w * 0.78) / K.LEN
    ox = (w - K.LEN * s) / 2
    body = stage + K.kart_side(s, ox, y, accent=accent, pod=pod,
                               number=number, flip=flip)
    body += accent_rule(72, h - 104, 160)
    if caption:
        body += label(72, h - 56, caption, size=26, color=INK_SOFT, track=3)
    return _wrap(body, w, h)


def kart_slalom(w=W, h=H, number="12", accent=K.RED):
    stage, y = _stage(w, h, 0.62)
    body = stage
    # Parcours: Pylonen in Flucht
    for i, (cx, cy, sc) in enumerate([(230, 0.00, 0.55), (560, 0.10, 0.70),
                                      (980, 0.055, 0.62), (1340, 0.20, 0.92),
                                      (1520, 0.40, 1.15)]):
        yy = y + (h - y) * cy
        body += cone(cx, yy, h=86 * sc * 1.5, w=62 * sc * 1.5,
                     color=K.RED if i % 2 == 0 else "#f0432f")
    # Fahrspur
    body += (f'<path d="M80 {y + (h-y)*0.52:.0f} C420 {y + (h-y)*0.30:.0f} '
             f'760 {y + (h-y)*0.54:.0f} 1100 {y + (h-y)*0.26:.0f} '
             f'C1300 {y + (h-y)*0.12:.0f} 1420 {y + (h-y)*0.10:.0f} '
             f'1560 {y + (h-y)*0.08:.0f}" fill="none" stroke="{K.RED}" '
             f'stroke-width="5" stroke-dasharray="22 18" opacity="0.5"/>')
    s = (w * 0.62) / K.LEN
    ox = w * 0.16
    body += K.kart_side(s, ox, y + (h - y) * 0.46, accent=accent,
                        number=number, driver=True)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def kart_lineup(w=W, h=H):
    """Drei Karts gestaffelt in die Tiefe, hinten klein, vorne gross."""
    stage, y = _stage(w, h, 0.52)
    body = stage
    conf = [(0.34, 0.33, 0.56, "#f0432f", "15"),
            (0.44, 0.50, 0.70, "#e22718", "11"),
            (0.56, 0.68, 0.88, "#cf1f14", "7")]
    for frac, cxf, cyf, acc, num in conf:
        s_ = (w * frac) / K.LEN
        body += K.kart_side(s_, w * cxf - K.LEN * s_ / 2, h * cyf,
                            accent=acc, number=num)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def kart_front(w=W, h=H, accent=K.RED):
    """Frontansicht: Nassau-Panel mit Nummernfeld, Raeder, Lenkrad, Helm."""
    stage, y = _stage(w, h, 0.78)
    body = stage
    cx = w / 2
    gy = y
    sc = h / 1000.0

    def tyre(x, half_w, hgt):
        o = (f'<ellipse cx="{x}" cy="{gy + 8*sc}" rx="{half_w*1.1}" '
             f'ry="{14*sc}" fill="#0d131b" opacity="0.14"/>')
        o += (f'<rect x="{x - half_w}" y="{gy - hgt}" width="{half_w*2}" '
              f'height="{hgt}" rx="{half_w*0.42}" fill="{K.TYRE}" '
              f'stroke="{K.INK}" stroke-width="5"/>')
        o += (f'<rect x="{x - half_w*0.78}" y="{gy - hgt*0.66}" '
              f'width="{half_w*1.56}" height="{hgt*0.34}" '
              f'rx="{half_w*0.26}" fill="{K.STEEL}" stroke="{K.INK}" '
              f'stroke-width="4"/>')
        return o

    # Hinterraeder (breiter, weiter aussen, dahinter)
    for sx in (-1, 1):
        body += tyre(cx + sx * 412 * sc, 74 * sc, 268 * sc)
    # Sitzlehne dahinter
    body += (f'<path d="M{cx - 150*sc} {gy - 190*sc} '
             f'C{cx - 160*sc} {gy - 470*sc} {cx + 160*sc} {gy - 470*sc} '
             f'{cx + 150*sc} {gy - 190*sc} Z" fill="{K.STEEL}" '
             f'stroke="{K.INK}" stroke-width="6"/>')
    # Vorderraeder
    for sx in (-1, 1):
        body += tyre(cx + sx * 330 * sc, 56 * sc, 248 * sc)
    # Achse
    body += (f'<rect x="{cx - 344*sc}" y="{gy - 152*sc}" width="{688*sc}" '
             f'height="{26*sc}" rx="{13*sc}" fill="{K.INK}"/>')
    # Nassau-Panel
    body += (f'<path d="M{cx - 296*sc} {gy - 166*sc} '
             f'C{cx - 326*sc} {gy - 300*sc} {cx - 190*sc} {gy - 352*sc} '
             f'{cx} {gy - 352*sc} '
             f'C{cx + 190*sc} {gy - 352*sc} {cx + 326*sc} {gy - 300*sc} '
             f'{cx + 296*sc} {gy - 166*sc} Z" fill="{accent}" '
             f'stroke="{K.INK}" stroke-width="6"/>')
    body += (f'<rect x="{cx - 86*sc}" y="{gy - 330*sc}" width="{172*sc}" '
             f'height="{128*sc}" rx="{14*sc}" fill="#ffffff" '
             f'stroke="{K.INK}" stroke-width="5"/>')
    body += label(cx, gy - 232 * sc, "7", size=96 * sc, color=K.INK,
                  weight=700, anchor="middle", track=0)
    body += (f'<path d="M{cx - 250*sc} {gy - 270*sc} '
             f'C{cx - 150*sc} {gy - 316*sc} {cx + 150*sc} {gy - 316*sc} '
             f'{cx + 250*sc} {gy - 270*sc}" fill="none" stroke="#ffffff" '
             f'stroke-width="8" opacity="0.38"/>')
    # Lenkrad + Saeule
    body += (f'<rect x="{cx - 13*sc}" y="{gy - 486*sc}" width="{26*sc}" '
             f'height="{140*sc}" fill="{K.INK}"/>')
    # Schultern des Fahrers hinter dem Lenkrad
    body += (f'<path d="M{cx - 176*sc} {gy - 470*sc} '
             f'C{cx - 170*sc} {gy - 580*sc} {cx + 170*sc} {gy - 580*sc} '
             f'{cx + 176*sc} {gy - 470*sc} Z" fill="{accent}" '
             f'stroke="{K.INK}" stroke-width="6"/>')
    body += (f'<ellipse cx="{cx}" cy="{gy - 486*sc}" rx="{152*sc}" '
             f'ry="{42*sc}" fill="none" stroke="{K.INK}" '
             f'stroke-width="{26*sc}"/>')
    body += (f'<circle cx="{cx}" cy="{gy - 486*sc}" r="{30*sc}" '
             f'fill="{accent}" stroke="{K.INK}" stroke-width="5"/>')
    # Helm
    body += helmet(cx, gy - 640 * sc, r=104 * sc, color="#f2f4f6")
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def kart_spacedrive(w=W, h=H):
    """Kart mit Handbedienung - Detailkreis mit Joystick."""
    stage, y = _stage(w, h, 0.70)
    s = (w * 0.66) / K.LEN
    ox = w * 0.04
    body = stage + K.kart_side(s, ox, y, accent="#cf1f14", number=None)
    # Detailkreis
    dcx, dcy, dr = w * 0.78, h * 0.34, h * 0.21
    body += (f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="#ffffff" '
             f'stroke="{K.INK}" stroke-width="5"/>')
    body += (f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="url(#hx)"/>')
    body = hatch_defs() + body
    # Joystick
    jx, jy = dcx, dcy + dr * 0.42
    body += (f'<rect x="{jx - dr*0.34}" y="{jy - dr*0.10}" width="{dr*0.68}" '
             f'height="{dr*0.22}" rx="{dr*0.07}" fill="{K.INK}"/>')
    body += (f'<rect x="{jx - dr*0.05}" y="{jy - dr*0.62}" width="{dr*0.10}" '
             f'height="{dr*0.56}" rx="{dr*0.05}" fill="{K.INK_SOFT}"/>')
    body += (f'<circle cx="{jx}" cy="{jy - dr*0.68}" r="{dr*0.17}" '
             f'fill="{K.RED}" stroke="{K.INK}" stroke-width="4"/>')
    # Verbindungslinie
    body += (f'<path d="M{ox + 1050*s:.0f} {y - 420*s:.0f} L{dcx - dr*0.80:.0f} '
             f'{dcy + dr*0.30:.0f}" stroke="{K.INK_SOFT}" stroke-width="2.6" '
             f'stroke-dasharray="10 8"/>')
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


# ------------------------------------------------------------- Technisches
def chassis_top(w=W, h=H):
    """Rahmen in Draufsicht mit Bemassung."""
    body, _ = _stage(w, h, 1.0)
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    cx, cy = w / 2, h * 0.50
    L, B = w * 0.66, h * 0.42
    x0, y0 = cx - L / 2, cy - B / 2
    tw = 15
    # Hauptrohre
    body += (f'<path d="M{x0 + L*0.10} {y0} L{x0 + L*0.86} {y0} '
             f'Q{x0 + L} {y0} {x0 + L} {y0 + B*0.14} L{x0 + L} {y0 + B*0.86} '
             f'Q{x0 + L} {y0 + B} {x0 + L*0.86} {y0 + B} L{x0 + L*0.10} {y0 + B} '
             f'Q{x0} {y0 + B} {x0} {y0 + B*0.80} L{x0} {y0 + B*0.20} '
             f'Q{x0} {y0} {x0 + L*0.10} {y0} Z" fill="none" stroke="{K.INK}" '
             f'stroke-width="{tw}" stroke-linejoin="round"/>')
    # Querrohre
    for fx in (0.22, 0.50, 0.78):
        body += (f'<line x1="{x0 + L*fx}" y1="{y0}" x2="{x0 + L*fx}" '
                 f'y2="{y0 + B}" stroke="{K.INK}" stroke-width="{tw*0.8}"/>')
    # Sitzflaeche
    body += (f'<rect x="{x0 + L*0.54}" y="{y0 + B*0.18}" width="{L*0.30}" '
             f'height="{B*0.64}" rx="{B*0.16}" fill="{K.STEEL}" '
             f'stroke="{K.INK}" stroke-width="5"/>')
    # Antrieb
    body += (f'<rect x="{x0 + L*0.86}" y="{y0 + B*0.28}" width="{L*0.16}" '
             f'height="{B*0.44}" rx="10" fill="{K.INK}"/>')
    # Raeder (Draufsicht)
    for fx, fw in ((0.06, 0.07), (0.92, 0.10)):
        for sy in (-1, 1):
            body += (f'<rect x="{x0 + L*fx - L*fw/2}" '
                     f'y="{cy + sy*B*0.62 - B*0.09}" width="{L*fw}" '
                     f'height="{B*0.18}" rx="8" fill="{K.TYRE}"/>')
    body += dim_h(x0, x0 + L, y0 + B + 118, "1 900 mm")
    body += dim_h(x0 + L * 0.06, x0 + L * 0.92, y0 - 96, "1 120 mm")
    body += label(72, h - 56, "RAHMEN · DRAUFSICHT", size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def drivetrain(w=W, h=H):
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    cy = h * 0.52
    # Motor
    mx = w * 0.26
    body += (f'<rect x="{mx - 150}" y="{cy - 130}" width="{300}" height="{260}" '
             f'rx="26" fill="{K.INK}"/>')
    for i in range(6):
        body += (f'<line x1="{mx - 110 + i*44}" y1="{cy - 96}" '
                 f'x2="{mx - 110 + i*44}" y2="{cy + 96}" stroke="{K.INK_SOFT}" '
                 f'stroke-width="9"/>')
    body += f'<circle cx="{mx + 150}" cy="{cy}" r="46" fill="{K.STEEL}" stroke="{K.INK}" stroke-width="5"/>'
    # Riemen
    ax = w * 0.70
    body += (f'<path d="M{mx + 150} {cy - 46} L{ax} {cy - 112} '
             f'M{mx + 150} {cy + 46} L{ax} {cy + 112}" stroke="{K.INK}" '
             f'stroke-width="18" stroke-linecap="round"/>')
    # Kettenrad / Achse
    body += f'<circle cx="{ax}" cy="{cy}" r="118" fill="none" stroke="{K.INK}" stroke-width="20"/>'
    for i in range(18):
        a = i * math.pi / 9
        body += (f'<line x1="{ax + math.cos(a)*118:.1f}" y1="{cy + math.sin(a)*118:.1f}" '
                 f'x2="{ax + math.cos(a)*140:.1f}" y2="{cy + math.sin(a)*140:.1f}" '
                 f'stroke="{K.INK}" stroke-width="9"/>')
    body += f'<circle cx="{ax}" cy="{cy}" r="40" fill="{K.RED}" stroke="{K.INK}" stroke-width="5"/>'
    # Achsrohr
    body += (f'<rect x="{ax - 20}" y="{cy - 300}" width="40" height="600" '
             f'rx="20" fill="{K.STEEL_D}" stroke="{K.INK}" stroke-width="5"/>')
    body += callout(mx, cy - 130, w * 0.20, h * 0.20, "ELEKTROMOTOR", side="right")
    body += callout(ax, cy - 140, w * 0.80, h * 0.22, "ACHSE + KETTENRAD", side="left")
    body += callout((mx + ax) / 2, cy - 80, w * 0.48, h * 0.84, "ZAHNRIEMEN", side="right")
    body += label(72, h - 56, "ANTRIEBSSTRANG", size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def battery(w=W, h=H):
    """Akkupack: Gehaeuse, Rundzellen, BMS-Platine, Pole."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    bx, by, bw, bh = w * 0.16, h * 0.26, w * 0.50, h * 0.48
    body += (f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" '
             f'fill="{K.STEEL}" stroke="{K.INK}" stroke-width="7"/>')
    body += (f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh*0.16}" '
             f'rx="26" fill="{K.INK}"/>')
    body += (f'<rect x="{bx + bw*0.06}" y="{by + bh*0.055}" '
             f'width="{bw*0.30}" height="{bh*0.05}" rx="6" fill="{K.RED}"/>')
    # Rundzellen
    cols, rows = 9, 4
    m = bw * 0.055
    gx = (bw - 2 * m) / cols
    gy = (bh * 0.72 - 2 * (bh * 0.05)) / rows
    r = min(gx, gy) * 0.40
    for rr in range(rows):
        for c in range(cols):
            ccx = bx + m + gx * (c + 0.5)
            ccy = by + bh * 0.26 + gy * (rr + 0.5)
            body += (f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{r:.1f}" '
                     f'fill="{K.INK_SOFT}" stroke="{K.INK}" stroke-width="3"/>')
            body += (f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{r*0.38:.1f}" '
                     f'fill="{K.STEEL_D}"/>')
    # Pole
    body += (f'<rect x="{bx + bw - 14}" y="{by + bh*0.28}" width="40" '
             f'height="{bh*0.12}" rx="9" fill="{K.RED}" stroke="{K.INK}" stroke-width="4"/>')
    body += (f'<rect x="{bx + bw - 14}" y="{by + bh*0.58}" width="40" '
             f'height="{bh*0.12}" rx="9" fill="{K.INK}"/>')
    # Blitz
    lx, ly = w * 0.80, h * 0.46
    body += (f'<path d="M{lx+26} {ly-160} L{lx-56} {ly+14} L{lx-6} {ly+14} '
             f'L{lx-32} {ly+160} L{lx+58} {ly-6} L{lx+2} {ly-6} Z" '
             f'fill="{K.RED}" stroke="{K.INK}" stroke-width="5" '
             f'stroke-linejoin="round"/>')
    body += callout(bx + bw * 0.52, by + bh * 0.10, w * 0.34, h * 0.14, "BMS-STEUERUNG")
    body += callout(bx + bw * 0.30, by + bh * 0.50, w * 0.13, h * 0.86,
                    "LITHIUM-RUNDZELLEN", side="right")
    body += callout(bx + bw + 26, by + bh * 0.34, w * 0.78, h * 0.80,
                    "LADEANSCHLUSS", side="left")
    body += label(72, h - 56, "ENERGIESPEICHER", size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def charging(w=W, h=H):
    stage, y = _stage(w, h, 0.74)
    body = stage
    s_ = (w * 0.52) / K.LEN
    ox = w * 0.03
    px = w * 0.80
    # Ladesaeule
    body += (f'<ellipse cx="{px}" cy="{y + 8}" rx="120" ry="18" fill="#0d131b" opacity="0.14"/>')
    body += (f'<rect x="{px - 84}" y="{y - 470}" width="168" height="470" '
             f'rx="24" fill="{K.INK}"/>')
    body += (f'<rect x="{px - 52}" y="{y - 430}" width="104" height="132" '
             f'rx="12" fill="{K.STEEL}" stroke="{K.INK}" stroke-width="4"/>')
    body += (f'<rect x="{px - 34}" y="{y - 404}" width="68" height="12" rx="6" fill="{K.INK_SOFT}"/>')
    body += (f'<rect x="{px - 34}" y="{y - 376}" width="44" height="10" rx="5" fill="{K.INK_SOFT}"/>')
    body += (f'<circle cx="{px}" cy="{y - 236}" r="30" fill="{K.RED}"/>')
    body += accent_rule(px - 84, y - 496, 168, h=10)
    # Ladebuchse am Kart
    bx, by = ox + 1660 * s_, y - 346 * s_
    body += (f'<path d="M{px - 84} {y - 250} C{px - 260} {y - 150} '
             f'{bx + 190} {y - 40} {bx + 18} {by + 6}" fill="none" '
             f'stroke="{K.INK}" stroke-width="15" stroke-linecap="round"/>')
    body += K.kart_side(s_, ox, y, accent="#cf1f14")
    body += (f'<circle cx="{bx}" cy="{by}" r="16" fill="{K.RED}" '
             f'stroke="#ffffff" stroke-width="5"/>')
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def track_map(w=W, h=H):
    """Slalomkurs von oben, mit Start-Ziel-Tor und Kart-Marke."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    pts = [(180, 520), (380, 340), (580, 640), (790, 340), (1000, 640),
           (1200, 370), (1410, 540)]
    d = f"M{pts[0][0]} {pts[0][1]}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        d += f" C{(x0+x1)/2} {y0} {(x0+x1)/2} {y1} {x1} {y1}"
    body += (f'<path d="{d}" fill="none" stroke="{K.STEEL_D}" '
             f'stroke-width="58" stroke-linecap="round" opacity="0.55"/>')
    body += (f'<path d="{d}" fill="none" stroke="{K.RED}" stroke-width="5" '
             f'stroke-dasharray="26 20" opacity="0.8"/>')
    for (x, yy) in pts:
        body += (f'<circle cx="{x}" cy="{yy}" r="24" fill="{K.RED}" '
                 f'stroke="#ffffff" stroke-width="6"/>')
    # Start-Ziel
    body += (f'<rect x="96" y="440" width="22" height="170" fill="{K.INK}"/>')
    for r in range(5):
        for c in range(2):
            if (r + c) % 2 == 0:
                body += (f'<rect x="{96 + c*11}" y="{440 + r*34}" width="11" '
                         f'height="34" fill="#ffffff"/>')
    body += label(96, 420, "START / ZIEL", size=23, color=INK_SOFT, track=2)
    # Kart als Draufsicht-Marke
    kx, ky = 1000, 640
    body += (f'<g transform="translate({kx} {ky}) rotate(-28)">'
             f'<rect x="-68" y="-40" width="136" height="80" rx="16" '
             f'fill="{K.INK}"/>'
             f'<rect x="-50" y="-52" width="30" height="22" rx="6" fill="{K.TYRE}"/>'
             f'<rect x="-50" y="30" width="30" height="22" rx="6" fill="{K.TYRE}"/>'
             f'<rect x="26" y="-56" width="34" height="26" rx="6" fill="{K.TYRE}"/>'
             f'<rect x="26" y="30" width="34" height="26" rx="6" fill="{K.TYRE}"/>'
             f'<circle cx="0" cy="0" r="17" fill="{K.RED}"/></g>')
    body += label(72, h - 56, "SLALOM-PARCOURS", size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


# ----------------------------------------------------------- Fertigung etc.
def cnc_mill(w=W, h=H):
    """4-Achs-Fraesmaschine: Portal, Spindel, Tisch, Werkstueck."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    x0, y0, bw, bh = w * 0.20, h * 0.16, w * 0.60, h * 0.64
    # Maschinenbett
    body += (f'<rect x="{x0}" y="{y0 + bh*0.72}" width="{bw}" '
             f'height="{bh*0.28}" rx="14" fill="{K.INK}"/>')
    # Staender links/rechts
    for fx in (0.0, 0.86):
        body += (f'<rect x="{x0 + bw*fx}" y="{y0}" width="{bw*0.14}" '
                 f'height="{bh*0.76}" rx="12" fill="{K.STEEL_D}" '
                 f'stroke="{K.INK}" stroke-width="6"/>')
    # Querbalken
    body += (f'<rect x="{x0}" y="{y0}" width="{bw}" height="{bh*0.16}" '
             f'rx="12" fill="{K.INK}"/>')
    body += (f'<rect x="{x0 + bw*0.06}" y="{y0 + bh*0.045}" '
             f'width="{bw*0.22}" height="{bh*0.07}" rx="6" fill="{K.RED}"/>')
    # Spindelschlitten
    sx = x0 + bw * 0.46
    body += (f'<rect x="{sx - bw*0.09}" y="{y0 + bh*0.16}" width="{bw*0.18}" '
             f'height="{bh*0.22}" rx="10" fill="{K.STEEL}" stroke="{K.INK}" '
             f'stroke-width="6"/>')
    body += (f'<rect x="{sx - bw*0.035}" y="{y0 + bh*0.38}" width="{bw*0.07}" '
             f'height="{bh*0.16}" rx="8" fill="{K.INK}"/>')
    # Fraeser
    body += (f'<path d="M{sx - bw*0.022} {y0 + bh*0.54} '
             f'L{sx + bw*0.022} {y0 + bh*0.54} L{sx + bw*0.012} {y0 + bh*0.63} '
             f'L{sx - bw*0.012} {y0 + bh*0.63} Z" fill="{K.RED}" '
             f'stroke="{K.INK}" stroke-width="4"/>')
    # Rundtisch (4. Achse)
    body += (f'<rect x="{x0 + bw*0.24}" y="{y0 + bh*0.64}" width="{bw*0.52}" '
             f'height="{bh*0.09}" rx="8" fill="{K.STEEL_D}" stroke="{K.INK}" '
             f'stroke-width="5"/>')
    body += (f'<circle cx="{x0 + bw*0.28}" cy="{y0 + bh*0.685}" r="{bh*0.055}" '
             f'fill="{K.STEEL}" stroke="{K.INK}" stroke-width="5"/>')
    # Werkstueck
    body += (f'<rect x="{sx - bw*0.08}" y="{y0 + bh*0.575}" width="{bw*0.16}" '
             f'height="{bh*0.065}" rx="5" fill="{K.STEEL}" stroke="{K.INK}" '
             f'stroke-width="5"/>')
    # Spaene
    for i, (dx, dy) in enumerate([(-34, 20), (28, 26), (-14, 38), (44, 14)]):
        body += (f'<circle cx="{sx + dx}" cy="{y0 + bh*0.66 + dy}" r="5" '
                 f'fill="{K.INK_SOFT}" opacity="0.8"/>')
    body += callout(sx, y0 + bh * 0.58, w * 0.80, h * 0.30, "WERKZEUG", side="left")
    body += callout(x0 + bw * 0.28, y0 + bh * 0.685, w * 0.20, h * 0.86,
                    "4. ACHSE · RUNDTISCH", side="right")
    body += label(72, h - 56, "CNC-BEARBEITUNG", size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def machined_part(w=W, h=H, title="GEFRAESTES BAUTEIL"):
    """Alu-Bauteil mit Bohrbild und Bemassung."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    body = hatch_defs() + body
    x0, y0 = w * 0.26, h * 0.26
    pw, ph = w * 0.44, h * 0.42
    body += (f'<path d="M{x0} {y0 + ph*0.22} Q{x0} {y0} {x0 + pw*0.20} {y0} '
             f'L{x0 + pw*0.74} {y0} Q{x0 + pw} {y0} {x0 + pw} {y0 + ph*0.26} '
             f'L{x0 + pw} {y0 + ph*0.70} Q{x0 + pw} {y0 + ph} '
             f'{x0 + pw*0.72} {y0 + ph} L{x0 + pw*0.34} {y0 + ph} '
             f'Q{x0 + pw*0.20} {y0 + ph} {x0 + pw*0.18} {y0 + ph*0.74} '
             f'L{x0 + pw*0.16} {y0 + ph*0.44} Q{x0 + pw*0.14} {y0 + ph*0.26} '
             f'{x0} {y0 + ph*0.22} Z" fill="{K.STEEL}" stroke="{K.INK}" '
             f'stroke-width="7"/>')
    # Tasche
    body += (f'<rect x="{x0 + pw*0.34}" y="{y0 + ph*0.26}" width="{pw*0.40}" '
             f'height="{ph*0.40}" rx="{ph*0.09}" fill="{PAPER_2}" '
             f'stroke="{K.INK}" stroke-width="6"/>')
    body += (f'<rect x="{x0 + pw*0.34}" y="{y0 + ph*0.26}" width="{pw*0.40}" '
             f'height="{ph*0.40}" rx="{ph*0.09}" fill="url(#hx)"/>')
    # Bohrungen
    for fx, fy in ((0.09, 0.14), (0.86, 0.14), (0.86, 0.82), (0.26, 0.84)):
        body += (f'<circle cx="{x0 + pw*fx}" cy="{y0 + ph*fy}" r="{ph*0.075}" '
                 f'fill="{PAPER}" stroke="{K.INK}" stroke-width="6"/>')
        body += (f'<circle cx="{x0 + pw*fx}" cy="{y0 + ph*fy}" r="{ph*0.035}" '
                 f'fill="{K.RED}"/>')
    body += dim_h(x0, x0 + pw, y0 + ph + 96, "184,0 mm")
    body += callout(x0 + pw * 0.54, y0 + ph * 0.46, w * 0.80, h * 0.24,
                    "TASCHE · 6 mm", side="left")
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def measuring(w=W, h=H, title="MESSEN & PRUEFEN"):
    """Messmaschine: Saeule, Taster, Werkstueck auf Granitplatte."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    gy = h * 0.78
    # Granitplatte
    body += (f'<rect x="{w*0.14}" y="{gy}" width="{w*0.72}" height="{h*0.09}" '
             f'rx="10" fill="{K.INK}"/>')
    body += (f'<rect x="{w*0.14}" y="{gy}" width="{w*0.72}" height="{h*0.022}" '
             f'rx="6" fill="{K.INK_SOFT}"/>')
    # Portal
    body += (f'<rect x="{w*0.22}" y="{h*0.22}" width="{w*0.05}" '
             f'height="{gy - h*0.22}" fill="{K.STEEL_D}" stroke="{K.INK}" '
             f'stroke-width="6"/>')
    body += (f'<rect x="{w*0.70}" y="{h*0.22}" width="{w*0.05}" '
             f'height="{gy - h*0.22}" fill="{K.STEEL_D}" stroke="{K.INK}" '
             f'stroke-width="6"/>')
    body += (f'<rect x="{w*0.20}" y="{h*0.18}" width="{w*0.57}" '
             f'height="{h*0.06}" rx="8" fill="{K.INK}"/>')
    # Pinole + Taster
    px = w * 0.48
    body += (f'<rect x="{px - w*0.022}" y="{h*0.24}" width="{w*0.044}" '
             f'height="{h*0.22}" rx="8" fill="{K.STEEL}" stroke="{K.INK}" '
             f'stroke-width="6"/>')
    body += (f'<rect x="{px - 7}" y="{h*0.46}" width="14" height="{h*0.11}" '
             f'fill="{K.INK}"/>')
    body += (f'<circle cx="{px}" cy="{h*0.585}" r="17" fill="{K.RED}" '
             f'stroke="{K.INK}" stroke-width="5"/>')
    # Werkstueck
    body += (f'<path d="M{px - 170} {gy} L{px - 170} {h*0.665} '
             f'L{px - 40} {h*0.665} L{px - 40} {h*0.615} L{px + 60} {h*0.615} '
             f'L{px + 60} {h*0.70} L{px + 190} {h*0.70} L{px + 190} {gy} Z" '
             f'fill="{K.STEEL}" stroke="{K.INK}" stroke-width="7"/>')
    # Messlinien
    body += (f'<path d="M{px} {h*0.60} L{px} {h*0.615}" stroke="{K.RED}" stroke-width="4"/>')
    body += callout(px, h * 0.585, w * 0.80, h * 0.86, "MESSTASTER", side="left")
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def fixture(w=W, h=H, title="VORRICHTUNG"):
    """Aufspannvorrichtung mit Spannpratzen und Bauteil."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    body = hatch_defs() + body
    x0, y0 = w * 0.18, h * 0.40
    pw, ph = w * 0.64, h * 0.20
    # Grundplatte
    body += (f'<rect x="{x0}" y="{y0 + ph}" width="{pw}" height="{ph*0.62}" '
             f'rx="10" fill="{K.INK}"/>')
    # T-Nuten
    for i in range(5):
        nx = x0 + pw * (0.10 + i * 0.20)
        body += (f'<rect x="{nx}" y="{y0 + ph}" width="{pw*0.03}" '
                 f'height="{ph*0.62}" fill="{K.INK_SOFT}" opacity="0.6"/>')
    # Bauteil
    body += (f'<rect x="{x0 + pw*0.26}" y="{y0 + ph*0.22}" width="{pw*0.48}" '
             f'height="{ph*0.78}" rx="8" fill="{K.STEEL}" stroke="{K.INK}" '
             f'stroke-width="7"/>')
    body += (f'<rect x="{x0 + pw*0.26}" y="{y0 + ph*0.22}" width="{pw*0.48}" '
             f'height="{ph*0.78}" rx="8" fill="url(#hx)"/>')
    # Spannpratzen
    for fx in (0.18, 0.82):
        body += (f'<rect x="{x0 + pw*fx - pw*0.055}" y="{y0 + ph*0.08}" '
                 f'width="{pw*0.11}" height="{ph*0.26}" rx="6" fill="{K.RED}" '
                 f'stroke="{K.INK}" stroke-width="5"/>')
        body += (f'<rect x="{x0 + pw*fx - 9}" y="{y0 - ph*0.30}" width="18" '
                 f'height="{ph*0.42}" rx="8" fill="{K.INK}"/>')
        body += (f'<circle cx="{x0 + pw*fx}" cy="{y0 - ph*0.34}" r="26" '
                 f'fill="{K.INK}"/>')
    body += callout(x0 + pw * 0.18, y0 + ph * 0.20, w * 0.22, h * 0.20,
                    "SPANNPRATZE", side="right")
    body += callout(x0 + pw * 0.50, y0 + ph * 0.60, w * 0.80, h * 0.80,
                    "WERKSTUECK", side="left")
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def gauge(w=W, h=H, title="LEHRE"):
    """Pruef-/Messlehre mit Pruefstiften."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    cx, cy = w * 0.47, h * 0.50
    body += (f'<rect x="{cx - w*0.24}" y="{cy - h*0.17}" width="{w*0.48}" '
             f'height="{h*0.34}" rx="18" fill="{K.STEEL}" stroke="{K.INK}" '
             f'stroke-width="7"/>')
    body += (f'<rect x="{cx - w*0.24}" y="{cy - h*0.17}" width="{w*0.48}" '
             f'height="{h*0.07}" rx="18" fill="{K.INK}"/>')
    for i in range(5):
        px = cx - w * 0.19 + i * w * 0.095
        body += (f'<rect x="{px - 11}" y="{cy - h*0.02}" width="22" '
                 f'height="{h*0.26}" rx="11" fill="{K.INK}"/>')
        body += (f'<circle cx="{px}" cy="{cy + h*0.25}" r="17" '
                 f'fill="{K.RED if i % 2 == 0 else K.STEEL_D}" '
                 f'stroke="{K.INK}" stroke-width="4"/>')
    # Skala
    for i in range(13):
        tx = cx - w * 0.21 + i * w * 0.035
        long = (i % 3 == 0)
        body += (f'<line x1="{tx}" y1="{cy - h*0.055}" x2="{tx}" '
                 f'y2="{cy - h*0.055 + (26 if long else 14)}" '
                 f'stroke="{K.INK_SOFT}" stroke-width="3"/>')
    body += dim_h(cx - w * 0.24, cx + w * 0.24, cy + h * 0.33, "0,01 mm")
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def safety_cell(w=W, h=H, title="SICHERHEITSZELLE"):
    """Rohrrahmen-Struktur, isometrisch angedeutet."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    cx, cy = w * 0.50, h * 0.52
    sw, sh, dp = w * 0.30, h * 0.30, w * 0.10
    def P(x, y, z):
        return (cx + x + z * 0.52, cy + y - z * 0.34)
    pts = {}
    for i, (x, y) in enumerate([(-sw, -sh), (sw, -sh), (sw, sh), (-sw, sh)]):
        pts["f%d" % i] = P(x, y, 0)
        pts["b%d" % i] = P(x, y, dp * 2.4)
    def tube(a, b, wdt=16, col=K.INK):
        return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
                f'y2="{b[1]:.1f}" stroke="{col}" stroke-width="{wdt}" '
                f'stroke-linecap="round"/>')
    for i in range(4):
        body += tube(pts["b%d" % i], pts["b%d" % ((i + 1) % 4)], 14, K.INK_SOFT)
    for i in range(4):
        body += tube(pts["f%d" % i], pts["b%d" % i], 14, K.INK_SOFT)
    for i in range(4):
        body += tube(pts["f%d" % i], pts["f%d" % ((i + 1) % 4)], 18, K.INK)
    body += tube(pts["f0"], pts["b3"], 11, K.INK_SOFT)
    body += tube(pts["f1"], pts["b2"], 11, K.INK_SOFT)
    mid_l = ((pts["f0"][0] + pts["f3"][0]) / 2, (pts["f0"][1] + pts["f3"][1]) / 2)
    mid_r = ((pts["f1"][0] + pts["f2"][0]) / 2, (pts["f1"][1] + pts["f2"][1]) / 2)
    body += tube(mid_l, mid_r, 14, K.RED)
    for k in ("f0", "f1", "f2", "f3"):
        body += (f'<circle cx="{pts[k][0]:.1f}" cy="{pts[k][1]:.1f}" r="16" '
                 f'fill="{K.STEEL}" stroke="{K.INK}" stroke-width="5"/>')
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def components(w=W, h=H, title="KOMPONENTEN"):
    """Mehrere Bauteile im Raster - fuer Uebersichtsbilder."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    body = hatch_defs() + body
    cols, rows = 3, 2
    mx, my = w * 0.14, h * 0.20
    cw = (w - 2 * mx) / cols
    ch = (h - 2 * my) / rows
    for r in range(rows):
        for c in range(cols):
            x = mx + c * cw + cw * 0.12
            y = my + r * ch + ch * 0.12
            bw, bh = cw * 0.76, ch * 0.70
            i = r * cols + c
            if i % 3 == 0:
                body += (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" '
                         f'rx="{bh*0.22}" fill="{K.STEEL}" stroke="{K.INK}" '
                         f'stroke-width="6"/>')
                body += (f'<circle cx="{x + bw*0.5}" cy="{y + bh*0.5}" '
                         f'r="{bh*0.22}" fill="{PAPER}" stroke="{K.INK}" '
                         f'stroke-width="6"/>')
            elif i % 3 == 1:
                body += (f'<path d="M{x} {y + bh} L{x} {y + bh*0.30} '
                         f'Q{x} {y} {x + bw*0.30} {y} L{x + bw} {y} '
                         f'L{x + bw} {y + bh*0.30} L{x + bw*0.34} {y + bh*0.30} '
                         f'L{x + bw*0.34} {y + bh} Z" fill="{K.STEEL}" '
                         f'stroke="{K.INK}" stroke-width="6"/>')
            else:
                body += (f'<circle cx="{x + bw*0.5}" cy="{y + bh*0.5}" '
                         f'r="{bh*0.46}" fill="{K.STEEL}" stroke="{K.INK}" '
                         f'stroke-width="6"/>')
                for k in range(8):
                    a = k * math.pi / 4
                    body += (f'<circle cx="{x + bw*0.5 + math.cos(a)*bh*0.30:.1f}" '
                             f'cy="{y + bh*0.5 + math.sin(a)*bh*0.30:.1f}" r="{bh*0.07}" '
                             f'fill="{PAPER}" stroke="{K.INK}" stroke-width="4"/>')
            if i == 1:
                body += (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" '
                         f'fill="url(#hx)" opacity="0.5"/>')
    body += accent_rule(72, h - 104, 160)
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    return _wrap(body, w, h)


def podium(w=W, h=H):
    """Siegerehrung: drei Podestbloecke mit Helmen."""
    stage, y = _stage(w, h, 0.76)
    body = stage
    cx = w / 2
    blocks = [(-1, 0.62, "2"), (0, 0.92, "1"), (1, 0.46, "3")]
    bw = w * 0.17
    for sx, hf, num in blocks:
        bh = h * 0.30 * hf
        x = cx + sx * bw * 1.08 - bw / 2
        body += (f'<rect x="{x}" y="{y - bh}" width="{bw}" height="{bh}" '
                 f'rx="10" fill="{K.INK if sx == 0 else K.INK_SOFT}"/>')
        body += (f'<rect x="{x}" y="{y - bh}" width="{bw}" height="{14}" '
                 f'fill="{K.RED}"/>')
        body += label(x + bw / 2, y - bh * 0.42, num, size=74,
                      color="#ffffff", weight=700, anchor="middle", track=0)
        body += helmet(x + bw / 2, y - bh - 74, r=58,
                       color=["#f0432f", "#f2f4f6", "#e22718"][int(sx) + 1],
                       stripe=K.RED if sx == 0 else None)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def paddock(w=W, h=H):
    """Karts unter dem Zeltdach - Fahrerlager."""
    stage, y = _stage(w, h, 0.72)
    body = stage
    # Zeltdach
    body += (f'<path d="M{w*0.06} {h*0.30} L{w*0.50} {h*0.16} '
             f'L{w*0.94} {h*0.30} L{w*0.94} {h*0.345} L{w*0.50} {h*0.205} '
             f'L{w*0.06} {h*0.345} Z" fill="{K.INK}"/>')
    body += (f'<path d="M{w*0.06} {h*0.345} L{w*0.50} {h*0.205} '
             f'L{w*0.94} {h*0.345}" fill="none" stroke="{K.RED}" stroke-width="9"/>')
    for fx in (0.09, 0.91):
        body += (f'<rect x="{w*fx - 9}" y="{h*0.33}" width="18" '
                 f'height="{y - h*0.33}" fill="{K.INK_SOFT}"/>')
    s_ = (w * 0.34) / K.LEN
    body += K.kart_side(s_, w * 0.10, y - h * 0.02, accent="#f0432f", number="4")
    body += K.kart_side(s_, w * 0.52, y, accent="#cf1f14", number="9")
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def workshop(w=W, h=H, title="FERTIGUNG"):
    """Hallenschnitt: Maschinenreihe, Werkbank, Kart auf dem Bock."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    y = h * 0.74
    body += (f'<rect x="0" y="{y}" width="{w}" height="{h - y}" '
             f'fill="#dfe3e8" opacity="0.8"/>')
    body += ground_line(w, y, op=0.35)
    # Maschinen im Hintergrund
    for i, fx in enumerate((0.06, 0.26, 0.46)):
        mh = h * (0.26 + 0.03 * (i % 2))
        body += (f'<rect x="{w*fx}" y="{y - mh}" width="{w*0.15}" '
                 f'height="{mh}" rx="10" fill="{K.STEEL_D}" opacity="0.55"/>')
        body += (f'<rect x="{w*fx + w*0.02}" y="{y - mh + 20}" '
                 f'width="{w*0.055}" height="{h*0.05}" rx="6" fill="{K.INK}" '
                 f'opacity="0.5"/>')
    # Werkbank
    body += (f'<rect x="{w*0.64}" y="{y - h*0.17}" width="{w*0.30}" '
             f'height="{h*0.035}" rx="6" fill="{K.INK}"/>')
    for fx in (0.66, 0.90):
        body += (f'<rect x="{w*fx}" y="{y - h*0.135}" width="14" '
                 f'height="{h*0.135}" fill="{K.INK_SOFT}"/>')
    body += (f'<rect x="{w*0.70}" y="{y - h*0.215}" width="{w*0.06}" '
             f'height="{h*0.045}" rx="5" fill="{K.RED}"/>')
    # Kart auf Montagebock
    s_ = (w * 0.40) / K.LEN
    body += (f'<rect x="{w*0.14}" y="{y - h*0.10}" width="{w*0.30}" '
             f'height="{h*0.022}" rx="6" fill="{K.INK}"/>')
    body += K.kart_side(s_, w * 0.12, y - h * 0.10, accent="#cf1f14", shadow=False)
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)


def org_chart(w=W, h=H, title="UNTERNEHMENSGRUPPE", root="leomax", kids=()):
    """Organigramm aus echten Angaben - nichts erfunden."""
    body = grid(w, h, step=w / 20, op=0.13) + corner_ticks(w, h)
    rw, rh = w * 0.34, h * 0.13
    rx, ry = (w - rw) / 2, h * 0.16
    body += (f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="12" '
             f'fill="{K.INK}"/>')
    body += (f'<rect x="{rx}" y="{ry}" width="{rw}" height="10" fill="{K.RED}"/>')
    rs = min(36, (rw - 48) * 1.78 / max(1, len(root)))
    body += label(rx + rw / 2, ry + rh * 0.60 + rs * 0.18, root, size=rs,
                  color="#ffffff", weight=700, anchor="middle", track=0.4)
    if not kids:
        return _wrap(body + accent_rule(72, h - 104, 160)
                     + label(72, h - 56, title, size=26, color=INK_SOFT, track=3),
                     w, h)
    n = len(kids)
    cw = min(w * 0.22, (w * 0.86) / n - 24)
    ch = h * 0.12
    cy = h * 0.58
    total = n * cw + (n - 1) * 32
    x0 = (w - total) / 2
    body += (f'<line x1="{w/2}" y1="{ry + rh}" x2="{w/2}" y2="{cy - 60}" '
             f'stroke="{K.INK}" stroke-width="5"/>')
    body += (f'<line x1="{x0 + cw/2}" y1="{cy - 60}" '
             f'x2="{x0 + total - cw/2}" y2="{cy - 60}" stroke="{K.INK}" '
             f'stroke-width="5"/>')
    for i, name in enumerate(kids):
        x = x0 + i * (cw + 32)
        body += (f'<line x1="{x + cw/2}" y1="{cy - 60}" x2="{x + cw/2}" '
                 f'y2="{cy}" stroke="{K.INK}" stroke-width="5"/>')
        body += (f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="12" '
                 f'fill="{PAPER}" stroke="{K.INK}" stroke-width="6"/>')
        body += (f'<rect x="{x}" y="{cy}" width="{cw}" height="8" fill="{K.RED}"/>')
        cs = min(27, (cw - 36) * 1.82 / max(1, len(name)))
        body += label(x + cw / 2, cy + ch * 0.60 + cs * 0.18, name, size=cs,
                      color=K.INK, weight=600, anchor="middle", track=0.3)
    body += label(72, h - 56, title, size=26, color=INK_SOFT, track=3)
    body += accent_rule(72, h - 104, 160)
    return _wrap(body, w, h)
