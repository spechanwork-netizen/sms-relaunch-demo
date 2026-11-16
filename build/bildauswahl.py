# -*- coding: utf-8 -*-
"""Entfernt Bilder, fuer die kein geliefertes Foto vorliegt, und begrenzt
die Kart-Unterseiten auf hoechstens drei Bilder.

  python3 -I build/bildauswahl.py .

Grundsatz: lieber kein Bild als ein erfundenes. Wo eine Bildergalerie
dadurch leer zurueckbliebe, faellt die ganze Sektion weg - eine Ueberschrift
ueber einem leeren Raster sieht nach Fehler aus.
"""
import sys, os, re

SITE = sys.argv[1] if len(sys.argv) > 1 else "."

# Bilder, die aus dem Markup verschwinden (Dateiname ohne Pfad)
RAUS = {
    "revo-sl.html": [
        "sms-revo-SL-Hockenheimring-8-scaled.jpg",
        "sms-revo-SL-Hockenheimring-6-scaled.jpg",
        "sms-revo-SL-Hockenheimring-2-scaled.jpg",
    ],
    "revo-x.html": [
        "47B402AA-51B5-4940-AE7C-ABF2A3324C78-scaled.jpeg",
        "IMG_0132-scaled.jpeg",
        "IMG_8576-scaled.jpg",
    ],
    "spacedrive.html": [
        "United-in-Dreams-7-scaled.jpg",
        "Teilnehmer-United-in-Dreams_PARAVAN.jpg",
        "Gewinner-Finale-United-in-Dreams_PARAVAN.jpg",
        "United-in-Dreams-2.jpg",
    ],
    "elektro-kart.html": [
        "IMG_8576-scaled.jpg",
        "E-Kart-sms-engineering-2-1024x683.jpg",
        "Elektro-Slalom-Kart-Bad-Aibling.jpg",
    ],
}

n_img = n_sek = 0
for seite, namen in RAUS.items():
    p = os.path.join(SITE, seite)
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    for name in namen:
        muster = re.compile(r'<img\b[^>]*src="assets/img/' + re.escape(name) + r'"[^>]*>\s*')
        s, k = muster.subn("", s)
        n_img += k

    # Sektionen, die danach nur noch ein leeres Bildraster enthalten
    def leer(m):
        global n_sek
        t = m.group(0)
        if "<img" in t or "hero-parallax" in t or "ds-cta-band" in t:
            return t
        ohne = re.sub(r"<[^>]+>", "", t).strip()
        if ohne:
            return t
        n_sek += 1
        return ""
    s = re.sub(r'<section\b(?:(?!</section>).)*</section>\s*', leer, s, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)
print(f"{n_img} Bilder entfernt, {n_sek} leere Sektionen entfernt")
