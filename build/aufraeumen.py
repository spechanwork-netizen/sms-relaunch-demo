# -*- coding: utf-8 -*-
"""Entfernt Bilddateien, auf die keine Seite mehr zeigt.

  python3 -I build/aufraeumen.py .

Achtung beim Suchmuster: die Parallax-Hintergruende stehen als
background-image:url(&quot;assets/img/bg/....jpg&quot;) im Markup. Ein
Ausdruck, der nur auf Anfuehrungszeichen achtet, uebersieht sie - und
loescht dann genau die Bilder, die noch gebraucht werden.
"""
import sys, os, re, html

SITE = sys.argv[1] if len(sys.argv) > 1 else "."
IMG = os.path.join(SITE, "assets", "img")

ref = set()
for f in os.listdir(SITE):
    if not f.endswith(".html"):
        continue
    s = html.unescape(open(os.path.join(SITE, f), encoding="utf-8").read())
    for m in re.findall(r'assets/img/([^"\')\s]+)', s):
        ref.add(m)

weg = []
for f in sorted(os.listdir(IMG)):
    if f != "bg" and f not in ref:
        weg.append(f)
bgref = {r.split("/", 1)[1] for r in ref if r.startswith("bg/")}
for f in sorted(os.listdir(os.path.join(IMG, "bg"))):
    if f not in bgref:
        weg.append("bg/" + f)

if "--trocken" in sys.argv:
    print("waeren entfernt:", weg or "nichts")
else:
    for f in weg:
        os.remove(os.path.join(IMG, f))
    print(f"{len(weg)} verwaiste Bilddateien entfernt:", weg or "keine")
