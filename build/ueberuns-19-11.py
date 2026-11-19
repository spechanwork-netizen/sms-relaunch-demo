# -*- coding: utf-8 -*-
"""Ueber uns: Stichwortband zwischen Teambild und Text, Ueberschrift ueber
die drei Spalten.

  python3 -I ueberuns-19-11.py <website-ordner>

Mehrfach ausfuehrbar.
"""
import sys, os, re

SITE = sys.argv[1]
p = os.path.join(SITE, "ueber-uns.html")
s = open(p, encoding="utf-8").read()

# --- Band herausloesen, wo immer es gerade steht -------------------------
# Die Einrueckung ist wichtig: '.*?\n *</div>' trifft sonst das Ende des
# inneren Rasters statt des Bandes - dann wandert nur ein Bruchstueck.
m = re.search(r'\n {6}<div style="display: flex; flex-direction: column; gap: 8px;[^"]*">.*?\n {6}</div>', s, re.S)
if not m:
    raise SystemExit("Stichwortband nicht gefunden")
band = m.group(0).strip("\n")
s = s[:m.start()] + s[m.end():]
band = re.sub(r'margin-(?:top|bottom): clamp\(8px, 1\.5vw, 16px\)', 'margin: 0', band)

# --- direkt an den Anfang der Sektion nach dem Teambild ------------------
# Das ist die Sektion, die mit dem Fliesstext beginnt.
i = s.index('<div style="display: flex; flex-direction: column; gap: 20px; max-width: 820px">')
einrueckung = "      "
s = s[:i] + band.strip() + "\n" + einrueckung + s[i:]

# --- Ueberschrift ueber die drei Spalten ---------------------------------
if "Was wir können" not in s:
    j = s.index('      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))')
    kopf = ('      <span class="t-label" style="color: var(--muted)">Was wir können</span>\n')
    s = s[:j] + kopf + s[j:]

open(p, "w", encoding="utf-8").write(s)
print("ueber-uns.html: Band zwischen Teambild und Text, Ueberschrift ueber den Spalten")
