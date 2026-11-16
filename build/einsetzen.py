# -*- coding: utf-8 -*-
"""Setzt die Fotos in die Bildplaetze der Website.

  python3 -I einsetzen.py <quellordner> <website-ordner>

Grundsaetze:
  * nie hochrechnen - lieber ein kleineres Bild als ein weiches
  * alle Metadaten fallen weg (die Originale tragen teils GPS-Koordinaten)
  * Fotos werden JPEG, Logos bleiben PNG mit Transparenz
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = 300_000_000
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zuordnung as Z

SRC, SITE = sys.argv[1], sys.argv[2]
# Optional: nur einen Teil laufen lassen, z. B. "marken"
NUR = sys.argv[3] if len(sys.argv) > 3 else ""
IMG = os.path.join(SITE, "assets", "img")
BG = os.path.join(IMG, "bg")

INHALT_W, INHALT_H = 1600, 1000
BG_W, BG_H = 1920, 1280


def finde(name):
    for root, d, fs in os.walk(SRC):
        if name in fs:
            return os.path.join(root, name)
    raise FileNotFoundError(name)


def lade(name, bg=None):
    im = ImageOps.exif_transpose(Image.open(finde(name)))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        if bg is not None:
            flat = Image.new("RGB", im.size, bg)
            flat.paste(im, (0, 0), im)
            im = flat
    elif im.mode != "RGB":
        im = im.convert("RGB")
    return im


def ausschnitt(im, zoom, fx, fy):
    if zoom >= 0.999:
        return im
    w, h = im.size
    nw, nh = int(w * zoom), int(h * zoom)
    x = int((w - nw) * fx)
    y = int((h - nh) * fy)
    return im.crop((x, y, x + nw, y + nh))


def cover(im, tw, th, fx, fy):
    w, h = im.size
    ziel = tw / th
    if w / h > ziel:                       # zu breit -> seitlich beschneiden
        nw = int(h * ziel)
        x = int((w - nw) * fx)
        im = im.crop((x, 0, x + nw, h))
    else:                                  # zu hoch -> oben/unten beschneiden
        nh = int(w / ziel)
        y = int((h - nh) * fy)
        im = im.crop((0, y, w, y + nh))
    w, h = im.size
    if w > tw:                             # nur verkleinern, nie vergroessern
        im = im.resize((tw, th), Image.LANCZOS)
    return im


def contain(im, tw, th):
    im = im.copy()
    im.thumbnail((tw, th), Image.LANCZOS)
    return im


def jpeg(im, pfad, q=80, sub=1):
    im.save(pfad, "JPEG", quality=q, optimize=True, progressive=True,
            subsampling=sub)


def png(im, pfad):
    im.save(pfad, "PNG", optimize=True)


def hell(im):
    """Macht aus der dunklen Logofassung die helle fuer dunklen Grund.

    Das Original ist schwarz auf weiss mit rotem Schmetterling und traegt ein
    blasses Wasserzeichen. Gefragt ist die Fassung, die der Kunde auch als
    kleines PNG geliefert hat: weiss auf transparent, Rot bleibt Rot. Die
    Deckkraft kommt also aus der Dunkelheit des Originals, nicht aus einem
    Alphakanal - den hat die Vorlage nicht.
    """
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    chroma = a.max(2) - a.min(2)
    L = 0.2126 * r + 0.7152 * g + 0.0722 * b
    rot = (r > g + 40) & (r > b + 40) & (chroma > 55)
    # 0,20 als Schwelle: darunter bleibt das Wasserzeichen als Schleier stehen,
    # darueber brechen die duennen Strichcode-Linien weg.
    deckung = np.where(rot, np.clip((chroma - 55) / 70.0, 0, 1),
                       np.clip((1 - L / 255.0 - 0.20) / 0.58, 0, 1))
    farbe = np.dstack([np.where(rot, 236, 255),
                       np.where(rot, 56, 255),
                       np.where(rot, 46, 255)])
    out = Image.fromarray(np.dstack([farbe, deckung * 255]).astype(np.uint8), "RGBA")
    kante = out.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    return out.crop(kante) if kante else out


bericht = {"ersetzt": [], "umbenannt": [], "uebersprungen": []}

# ---------------------------------------------------------------- Inhalt
for eintrag in [] if NUR and NUR != "inhalt" else Z.INHALT + Z.NEU:
    ziel, quelle, modus, fx, fy, zoom = eintrag[:6]
    flaeche = eintrag[6] if len(eintrag) > 6 else "#ffffff"
    try:
        im = lade(quelle, bg=flaeche)
    except FileNotFoundError:
        bericht["uebersprungen"].append((ziel, quelle, "Quelle fehlt"))
        continue
    im = ausschnitt(im, zoom, fx, fy)
    if modus == "voll":
        # Seitenverhaeltnis bleibt, nur die Breite wird begrenzt
        if im.size[0] > 1800:
            im = im.resize((1800, round(im.size[1] * 1800 / im.size[0])), Image.LANCZOS)
    elif modus == "cover":
        im = cover(im, INHALT_W, INHALT_H, fx, fy)
    else:
        im = contain(im, INHALT_W, INHALT_H)
    neu = os.path.splitext(ziel)[0] + ".jpg"
    jpeg(im, os.path.join(IMG, neu))
    if neu != ziel:
        bericht["umbenannt"].append((ziel, neu))
        alt = os.path.join(IMG, ziel)
        if os.path.exists(alt):
            os.remove(alt)
    bericht["ersetzt"].append((neu, quelle, f"{im.size[0]}x{im.size[1]}"))

# ---------------------------------------------------------------- Marken
for ziel, quelle, modus in [] if NUR and NUR != "marken" else Z.MARKEN:
    try:
        im = ImageOps.exif_transpose(Image.open(finde(quelle)))
    except FileNotFoundError:
        bericht["uebersprungen"].append((ziel, quelle, "Quelle fehlt"))
        continue
    if modus == "hell":
        im = hell(im)
    im = im.convert("RGBA")
    if modus == "trim":
        # weissen Rand wegschneiden, damit das Logo den Platz ausfuellt
        grau = im.convert("RGB").convert("L")
        maske = grau.point(lambda v: 255 if v < 244 else 0)
        box = maske.getbbox()
        if box:
            im = im.crop(box)
    if modus == "hell":
        # Anzeigehoehe im Kopf sind 48 px - 240 px reichen bis 3x Pixeldichte
        if im.size[1] > 240:
            im = im.resize((round(im.size[0] * 240 / im.size[1]), 240), Image.LANCZOS)
    elif im.size[0] > 1200:
        im.thumbnail((1200, 1200), Image.LANCZOS)
    png(im, os.path.join(IMG, ziel))
    bericht["ersetzt"].append((ziel, quelle, f"{im.size[0]}x{im.size[1]}"))

# --------------------------------------------------------- Hintergruende
for slug, (quelle, fx, fy, zoom) in ([] if NUR and NUR != "bg" else Z.HINTERGRUND.items()):
    try:
        im = lade(quelle, bg="#1a2129")
    except FileNotFoundError:
        bericht["uebersprungen"].append((slug, quelle, "Quelle fehlt"))
        continue
    im = ausschnitt(im, zoom, fx, fy)
    im = cover(im, BG_W, BG_H, fx, fy)
    # Die Hintergruende liegen unter 74-88 % dunklem Overlay -
    # dort ist jedes Kompressionsartefakt unsichtbar.
    jpeg(im, os.path.join(BG, slug + ".jpg"), q=62, sub=2)
    bericht["ersetzt"].append((f"bg/{slug}.jpg", quelle, f"{im.size[0]}x{im.size[1]}"))

print(json.dumps(bericht, ensure_ascii=False))
