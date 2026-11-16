# -*- coding: utf-8 -*-
"""Rechnet den WCAG-Kontrast der Kopfbereich-Texte gegen das echte Bild."""
import sys, os, json
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/kontrast"
ziele = json.load(open(os.path.join(OUT, "ziele.json"), encoding="utf-8"))


def lin(v):
    v /= 255.0
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def lum(r, g, b):
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


schlecht = []
for seite, liste in ziele.items():
    im = Image.open(os.path.join(OUT, seite + ".png")).convert("RGB")
    px = im.load()
    for z in liste:
        s, n = 0.0, 0
        for y in range(z["y"], min(z["y"] + z["h"], im.height), 2):
            for x in range(z["x"], min(z["x"] + z["w"], im.width), 2):
                s += lum(*px[x, y]); n += 1
        if not n:
            continue
        lb, lt = s / n, lum(*z["col"])
        k = (max(lb, lt) + .05) / (min(lb, lt) + .05)
        gross = z["size"] >= 24 or (z["size"] >= 18.66 and z["bold"])
        noetig = 3.0 if gross else 4.5
        if k < noetig:
            schlecht.append(f'{seite} | {z["tag"]} {z["size"]:.0f}px | {k:.2f}:1 (noetig {noetig})')
print("\n".join(schlecht) if schlecht else "Kontrast im Kopfbereich ueberall ausreichend")
