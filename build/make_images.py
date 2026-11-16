#!/usr/bin/env python3
"""Erzeugt alle Platzhalterbilder fuer den sms-Relaunch.

Zwei Sorten:
  * Inhaltsbilder  - helle Platte im Stil des Design-Systems (photo-plate:
    Flaeche --surface-card mit diagonaler Schraffur), Beschriftung aus dem
    Alt-Text. Dateiname = Dateiname des Originals, damit ein echtes Foto
    spaeter einfach darueber gelegt werden kann.
  * Hintergrundbilder - dunkle Platte je Seite, 1920x1280, fuer den
    Parallax-Kopfbereich. Liegt unter einem dunklen Overlay, deshalb
    mitteltonig statt schwarz.
"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def hatch(d, w, h, rgba, step=12, thick=1):
    for i in range(-h, w + h, step):
        d.line([(i, 0), (i + h, h)], fill=rgba, width=thick)


def plate(w, h, bg, hatch_rgba, label, sub, label_rgb, accent=None, big=False):
    im = Image.new("RGB", (w, h), bg)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    hatch(d, w, h, hatch_rgba, step=max(10, w // 150), thick=1)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)

    if accent:                                    # 4px Markenstreifen oben
        seg = w / 3.0
        for i, c in enumerate(accent):
            d.rectangle([i * seg, 0, (i + 1) * seg, max(3, h // 220)], fill=c)

    fs = max(13, int(w / (26 if big else 34)))
    f1 = font(FONT_B, fs)
    f2 = font(FONT_R, max(11, int(fs * 0.62)))

    t1 = label.upper()
    b1 = d.textbbox((0, 0), t1, font=f1)
    # Zeilenumbruch, wenn zu breit
    lines, cur = [], ""
    for word in t1.split():
        probe = (cur + " " + word).strip()
        if d.textbbox((0, 0), probe, font=f1)[2] > w * 0.82 and cur:
            lines.append(cur); cur = word
        else:
            cur = probe
    lines.append(cur)

    lh = (b1[3] - b1[1]) + int(fs * 0.45)
    total = lh * len(lines) + (int(fs * 1.5) if sub else 0)
    y = (h - total) // 2
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=f1)
        d.text(((w - (bb[2] - bb[0])) / 2, y), ln, font=f1, fill=label_rgb)
        y += lh
    if sub:
        bb = d.textbbox((0, 0), sub, font=f2)
        d.text(((w - (bb[2] - bb[0])) / 2, y + int(fs * 0.3)), sub,
               font=f2, fill=label_rgb)

    d.rectangle([0, 0, w - 1, h - 1], outline=(0, 0, 0, 40) if bg[0] > 128 else (255, 255, 255, 40))
    return im


def main(spec_path, out_dir):
    spec = json.load(open(spec_path, encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "bg"), exist_ok=True)
    accent = [(240, 67, 47), (226, 39, 24), (163, 20, 12)]   # Rot-Staffel
    n = 0

    # --- Inhaltsbilder: helle Platte ---------------------------------------
    for name, meta in spec["content"].items():
        w, h = meta.get("size", [1600, 1000])
        im = plate(w, h, (250, 250, 250), (38, 38, 38, 13),
                   meta["label"], "PLATZHALTER", (154, 154, 154))
        im.save(os.path.join(out_dir, name), quality=88)
        n += 1

    # --- Logos / Marken: dunkel mit Streifen --------------------------------
    for name, meta in spec["mark"].items():
        w, h = meta.get("size", [600, 200])
        im = plate(w, h, (26, 33, 41), (255, 255, 255, 16),
                   meta["label"], meta.get("sub", "PLATZHALTER"),
                   (235, 235, 235), accent=accent, big=True)
        im.save(os.path.join(out_dir, name))
        n += 1

    # --- Parallax-Hintergruende je Seite ------------------------------------
    # Bewusst texturiert statt flaechig: unter dem dunklen Overlay muss noch
    # Struktur erkennbar sein, sonst sieht man die Parallax-Bewegung nicht.
    # Beschriftung klein unten rechts, damit sie nicht mit der Ueberschrift
    # kollidiert.
    for slug, label in spec["bg"].items():
        w, h = 1920, 1280
        im = Image.new("RGB", (w, h), (45, 55, 66))
        d0 = ImageDraw.Draw(im)
        for y in range(h):                                  # weicher Verlauf
            t = y / h
            d0.line([(0, y), (w, y)],
                    fill=(int(38 + 36 * t), int(47 + 38 * t), int(57 + 40 * t)))
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        hatch(d, w, h, (255, 255, 255, 26), step=18, thick=2)
        for x in range(0, w, 160):                          # Raster
            d.line([(x, 0), (x, h)], fill=(255, 255, 255, 20), width=1)
        for y in range(0, h, 160):
            d.line([(0, y), (w, y)], fill=(255, 255, 255, 20), width=1)
        for i, c in enumerate([(240, 67, 47, 90), (226, 39, 24, 90), (163, 20, 12, 90)]):
            d.rectangle([i * w / 3, h - 10, (i + 1) * w / 3, h], fill=c)
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
        d = ImageDraw.Draw(im)
        f = font(FONT_R, 26)
        t = (label + "  ·  PLATZHALTER").upper()
        bb = d.textbbox((0, 0), t, font=f)
        d.text((w - (bb[2] - bb[0]) - 48, h - (bb[3] - bb[1]) - 54), t,
               font=f, fill=(255, 255, 255))
        im.save(os.path.join(out_dir, "bg", f"{slug}.jpg"), quality=84)
        n += 1

    print(f"{n} Platzhalter erzeugt in {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
