#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt alle Bilder der Website als eigene Vektorgrafiken.

Statt grauer Platzhalterflaechen steht jetzt in jedem Bild ein Motiv:
Karts, Baugruppen, Maschinen, Parcours - gezeichnet im Stil des
Design-Systems (Blueprint-Raster, Schiefergrau, roter Akzent).

  python3 make_art.py <imagespec.json> <ziel-ordner>

Was bewusst Platzhalter bleibt:
  * die drei Logo-/Zertifikatsflaechen - ein Logo kann man nicht erfinden
Das Organigramm zeigt nur, was auf der Seite selbst belegt ist.
"""
import os, sys, json, io

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "art"))
sys.path.insert(0, HERE)

import cairosvg
import scenes as S
import bg as BG
import kart as K
from make_images import plate

RED_L, RED_M, RED_D = "#f0432f", "#e22718", "#cf1f14"


def studio(**kw):
    return lambda: S.kart_studio(**kw)


# Dateiname -> Motiv.  Reihenfolge wie im Bildverzeichnis.
CONTENT = {
    "sms_konstruktion_entwicklung_01.png": lambda: S.chassis_top(),
    "sms_fertigung_montage_01.png":        lambda: S.workshop(title="FERTIGUNG"),
    "sms_lehren-messmittelbau_01.png":     lambda: S.measuring(title="MESSEN UND PRUEFEN"),
    "sms-e-Kart-Training-1024x683.jpg":    lambda: S.kart_slalom(number="12"),
    "revo-SL-@DKSM-Finale-320x202.png":    studio(number="23", accent=RED_D, caption="SMS REVO SL"),
    "revo-SL-@Bundesendlauf-320x202.png":  lambda: S.kart_lineup(),
    "E-Kart-sms-engineering-2-1024x683.jpg": studio(number="7", accent=RED_D, caption="SMS REVO SL"),
    "engineering.jpg":                     lambda: S.machined_part(title="GEFRAESTES BAUTEIL"),
    "smsengineering_Website_Bild_Vertriebspartnerschaft_Beule.png": lambda: S.paddock(),
    "Neue-Maschine-DMF-200-8-1-320x202.png": lambda: S.cnc_mill(),
    "Universal-Antriebsstrang-sms-engineering-320x202.png": lambda: S.drivetrain(),
    "Batterie-Leasing-eKart-320x202.png":  lambda: S.battery(),
    "sms_emobilitaet.jpg":                 lambda: S.charging(),
    "sms_lehren-messmittelbau_03.png":     lambda: S.gauge(title="LEHRENBAU"),
    "sms_stuetzgestelle_02.jpg":           lambda: S.safety_cell(title="SICHERHEITSZELLE"),
    "sms_konstruktion_entwicklung_02.png": lambda: S.components(title="KOMPONENTEN"),
    "sms_konstruktion_entwicklung_03.png": lambda: S.fixture(title="WERKZEUGE UND VORRICHTUNGEN"),
    "sms_lehren-messmittelbau_02.png":     lambda: S.fixture(title="PRUEFVORRICHTUNG"),
    "sms_stuetzgestelle.jpg":              lambda: S.safety_cell(title="STUETZGESTELL"),
    "sms_stuetzgestelle_03.jpg":           lambda: S.workshop(title="STUETZGESTELL IM EINSATZ"),
    "IMG_8576-scaled.jpg":                 studio(accent=RED_M, caption="SMS REVO X", flip=True),
    "Inklusives-Kart-1024x683.jpg":        lambda: S.kart_spacedrive(),
    "Elektro-Slalom-Kart.jpg":             studio(number="3", accent=RED_L, caption="ELEKTRO-SLALOM-KART"),
    "Elektro-Slalom-Kart-Bad-Aibling.jpg": lambda: S.kart_slalom(number="5", accent=RED_L),
    "sms-revo-SL-Hockenheimring-11-scaled.jpg": lambda: S.kart_slalom(number="9", accent=RED_M),
    "sms-revo-SL-Hockenheimring-13-scaled-e1666783706334.jpg": lambda: S.kart_lineup(),
    "sms-revo-SL-Hockenheimring-8-scaled.jpg":  lambda: S.track_map(),
    "sms-revo-SL-Hockenheimring-6-scaled.jpg":  lambda: S.paddock(),
    "sms-revo-SL-Hockenheimring-2-scaled.jpg":  studio(number="14", accent=RED_M, flip=True, caption="AUSSTELLUNG"),
    "IMG_2384-scaled.jpg":                 studio(number="7", accent=RED_D, flip=True, caption="SMS REVO SL"),
    "47B402AA-51B5-4940-AE7C-ABF2A3324C78-scaled.jpeg": lambda: S.kart_slalom(number="2", accent=RED_M),
    "IMG_0132-scaled.jpeg":                lambda: S.kart_front(accent=RED_M),
    "United-in-Dreams-6-scaled.jpg":       lambda: S.podium(),
    "United-in-Dreams-9.jpg":              lambda: S.kart_lineup(),
    "United-in-Dreams-7-scaled.jpg":       lambda: S.paddock(),
    "Teilnehmer-United-in-Dreams_PARAVAN.jpg": lambda: S.kart_slalom(number="18", accent=RED_L),
    "Gewinner-Finale-United-in-Dreams_PARAVAN.jpg": lambda: S.podium(),
    "United-in-Dreams-2.jpg":              lambda: S.kart_spacedrive(),
    # Organigramm: nur was auf der Seite selbst belegt ist
    "leomax-firmenstruktur_Zeichenflaeche-1.png": lambda: S.org_chart(
        root="leomax-Unternehmensgruppe",
        kids=("leomax engineering GmbH", "sms engineering GmbH"),
        title="UNTERNEHMENSGRUPPE · NACH ANGABEN DER WEBSITE"),
}

# Hintergrundmotiv je Seite
BG_KIND = {
    "home": "kart", "aktuelles": "grid", "unternehmen": "chassis",
    "ueber-uns": "mixed", "historie": "kart_flip", "engineering": "chassis",
    "e-mobilitaet": "gear", "konstruktion": "chassis", "lehren": "grid",
    "sicherheitszellen": "chassis", "fertigung": "gear", "messen": "grid",
    "elektro-kart": "cones", "revo-sl": "kart", "revo-x": "kart_flip",
    "spacedrive": "kart", "bestellformulare": "grid", "dokumente": "grid",
    "impressum": "chassis", "cta": "mixed",
}


def png(svg, path, w, h):
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=path,
                     output_width=w, output_height=h)


def save_png(src, target, colors=96):
    """Flachgrafik braucht keine 16 Mio. Farben - Palette spart ~80 %."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im = im.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    im.save(target, optimize=True)


def main(spec_path, out_dir):
    spec = json.load(open(spec_path, encoding="utf-8"))
    os.makedirs(os.path.join(out_dir, "bg"), exist_ok=True)
    n_art = n_plate = 0

    for name, meta in spec["content"].items():
        w, h = meta.get("size", [1600, 1000])
        fn = CONTENT.get(name)
        target = os.path.join(out_dir, name)
        if fn is None:
            im = plate(w, h, (250, 250, 250), (38, 38, 38, 13),
                       meta["label"], "PLATZHALTER", (154, 154, 154))
            im.save(target, quality=88)
            n_plate += 1
            continue
        tmp = target + ".png.tmp"
        png(fn(), tmp, w, h)
        from PIL import Image
        if name.lower().endswith((".jpg", ".jpeg")):
            Image.open(tmp).convert("RGB").save(target, quality=84,
                                                optimize=True, progressive=True)
        else:
            save_png(tmp, target)
        os.remove(tmp)
        n_art += 1

    # Logos und Zertifikat bleiben Platzhalter - nicht erfindbar
    accent = [(240, 67, 47), (226, 39, 24), (163, 20, 12)]
    for name, meta in spec["mark"].items():
        w, h = meta.get("size", [600, 200])
        im = plate(w, h, (26, 33, 41), (255, 255, 255, 16), meta["label"],
                   meta.get("sub", "PLATZHALTER"), (235, 235, 235),
                   accent=accent, big=True)
        im.save(os.path.join(out_dir, name))
        n_plate += 1

    from PIL import Image
    for slug in spec["bg"]:
        kind = BG_KIND.get(slug, "kart")
        tmp = os.path.join(out_dir, "bg", slug + ".tmp.png")
        png(BG.background(slug, kind), tmp, BG.BW, BG.BH)
        Image.open(tmp).convert("RGB").save(
            os.path.join(out_dir, "bg", slug + ".jpg"), quality=74,
            optimize=True, progressive=True)
        os.remove(tmp)
        n_art += 1

    print(f"{n_art} Grafiken gezeichnet, {n_plate} Platzhalter "
          f"(Logos/Zertifikat) in {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
