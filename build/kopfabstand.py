# -*- coding: utf-8 -*-
"""Nimmt dem Bildkopf die Polsterung aus dem style-Attribut.

  python3 -I kopfabstand.py <website-ordner>

Warum: Der Abstand zwischen Kopfleiste und Ueberschrift soll auf jeder Seite
gleich sein. Er stand bisher im style-Attribut jeder Seite und wurde vom
Stylesheet nicht erreicht - ein Inline-Stil gewinnt immer. Jetzt steht die
Polsterung in site.css (.hero-parallax), hier bleibt nur das Bild.

Mehrfach ausfuehrbar.
"""
import sys, os, glob

ALT = '; padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)"'
NEU = '"'

site = sys.argv[1]
geaendert = 0
for pfad in sorted(glob.glob(os.path.join(site, "*.html"))):
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    n = s.count('class="hero-parallax" style=')
    if not n:
        continue
    vorher = s
    # nur im Bildkopf, nicht im Anfrage-Band
    stelle = s.find('class="hero-parallax" style="')
    while stelle != -1:
        ende = s.find('"', stelle + len('class="hero-parallax" style="'))
        block = s[stelle:ende + 1]
        s = s[:stelle] + block.replace(ALT, NEU) + s[ende + 1:]
        stelle = s.find('class="hero-parallax" style="', stelle + 1)
    if s != vorher:
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(s)
        geaendert += 1
print(f"Bildkoepfe bereinigt: {geaendert}")
