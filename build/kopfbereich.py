# -*- coding: utf-8 -*-
"""Macht aus dem Kopfbereich einen reinen Bildkopf. Mehrfach ausfuehrbar.

  python3 -I build/kopfbereich.py .

Im Design hatte der Kopfbereich zwei Spalten: Text links, ein zweites Foto
rechts - und dahinter lief noch ein drittes Bild als Hintergrund. Drei Bilder
auf einmal sind unruhig. Jetzt traegt ein grosses Bild den Kopf, der Text
steht darauf. Das zweite Foto faellt weg; es kommt auf allen Seiten, wo es
inhaltlich zaehlt, ohnehin weiter unten noch einmal vor.
"""
import sys, os, re

SITE = sys.argv[1] if len(sys.argv) > 1 else "."
n_img = n_grid = n_label = 0

for f in sorted(os.listdir(SITE)):
    if not f.endswith(".html"):
        continue
    p = os.path.join(SITE, f)
    s = open(p, encoding="utf-8").read()
    if 'class="hero-parallax"' not in s:
        continue
    a = s.index('<section class="hero-parallax"')
    b = s.index("</section>", a)
    kopf, rest = s[a:b], s[b:]
    orig = kopf

    # zweites Foto entfernen
    kopf2 = re.sub(r'<img\b(?:(?!<img)[^>])*?>\s*(?=</div>)', "", kopf, count=1)
    if kopf2 != kopf:
        n_img += 1
        kopf = kopf2

    # Die kleine Zeile ueber der Ueberschrift stand auf --on-dark-soft und
    # kam auf dem hellen Bild nur auf 3,98:1 - zu wenig. Weiss statt grau.
    kopf3 = re.sub(r'(<span class="t-label" style="color: )var\(--on-dark-soft\)',
                   r'\1var(--on-dark)', kopf, count=1)
    if kopf3 != kopf:
        n_label += 1
        kopf = kopf3

    # zwei Spalten -> eine Textspalte
    if "repeat(auto-fit, minmax(320px, 1fr))" in kopf:
        kopf = kopf.replace("repeat(auto-fit, minmax(320px, 1fr))", "minmax(0, 860px)", 1)
        n_grid += 1

    if kopf != orig:
        open(p, "w", encoding="utf-8").write(s[:a] + kopf + rest)
print(f"{n_img} Zweitfotos entfernt, {n_grid} Kopfbereiche auf eine Spalte, "
      f"{n_label} Labelfarben aufgehellt")
