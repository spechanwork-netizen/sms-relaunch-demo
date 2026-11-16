# -*- coding: utf-8 -*-
"""Loest die Engineering-Unterseiten auf und holt sie als Panels auf eine Seite.

  python3 -I engineering-panels.py <website-ordner>

Aus drei Unterseiten werden drei Panels auf engineering.html. Die Seite
E-Mobilitaet entfaellt ersatzlos, "Sicherheitszellen und Stuetzgestelle"
heisst jetzt "Pruefstands- und Sonderanlagen".

Mehrfach ausfuehrbar: liegen die Unterseiten nicht mehr vor, passiert nichts.
"""
import sys, os, re

SITE = sys.argv[1]
WEG = ["e-mobilitaet.html"]
PANELS = [
    ("konstruktion.html",     "Konstruktion und Entwicklung", "canvas"),
    ("lehren.html",           "Lehren- und Messmittelbau",    "soft"),
    ("sicherheitszellen.html", "Prüfstands- und Sonderanlagen", "canvas"),
]


def lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def hauptteil(s):
    return s[s.index('<main id="inhalt">'):s.index("</main>")]


def kopfabsatz(m):
    """Der einleitende Satz aus dem Bildkopf der Unterseite."""
    t = re.search(r'<p class="t-body-md" style="color: var\(--on-dark-soft\)[^"]*">(.*?)</p>', m, re.S)
    return t.group(1) if t else ""


def inhalte(m):
    """Der Inhalt aller Sektionen ausser dem Bildkopf, eine Ebene tiefer."""
    teile = []
    for sek in re.finditer(r'<section (?!class="hero-parallax")[^>]*>(.*?)\n  </section>', m, re.S):
        inner = sek.group(1)
        # aeussere Hoehlung (max-width-Container) abstreifen
        d = re.match(r'\s*<div style="max-width: 1440px[^"]*">(.*)</div>\s*$', inner, re.S)
        if d:
            inner = d.group(1)
        # Ueberschriften eine Stufe tiefer: h3 zuerst, sonst wandert h2 zweimal
        inner = inner.replace("<h3 ", "<h4 ").replace("</h3>", "</h4>")
        inner = inner.replace("<h2 ", "<h3 ").replace("</h2>", "</h3>")
        teile.append(inner.strip("\n"))
    return teile


ziel = os.path.join(SITE, "engineering.html")
quellen = [p for p, _, _ in PANELS if os.path.exists(os.path.join(SITE, p))]
if not quellen:
    print("Unterseiten schon aufgeloest - nichts zu tun")
    raise SystemExit

panels = []
for datei, titel, ton in PANELS:
    pfad = os.path.join(SITE, datei)
    if not os.path.exists(pfad):
        continue
    m = hauptteil(lies(pfad))
    einleitung = kopfabsatz(m)
    block = "\n\n".join(inhalte(m))
    anker = datei.replace(".html", "")
    if datei == "sicherheitszellen.html":
        anker = "pruefstandsanlagen"
    panels.append(
        f'  <section id="{anker}" style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)" '
        f'data-sec="float" data-tone="{ton}">\n'
        f'    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: clamp(28px, 3vw, 40px)">\n'
        f'      <div style="display: flex; flex-direction: column; gap: 12px; max-width: 820px">\n'
        f'        <span class="t-label" style="color: var(--muted)">Engineering</span>\n'
        f'        <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(26px, 3.4vw, 32px)">{titel}</h2>\n'
        + (f'        <p class="t-body-md" style="color: var(--body)">{einleitung}</p>\n' if einleitung else "")
        + '      </div>\n'
        + block + "\n"
        + '    </div>\n  </section>'
    )

# Inhaltsverzeichnis ueber den Panels
nav = ('  <section style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px) 0" data-sec="float" data-tone="canvas">\n'
       '    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 12px">\n'
       + "".join(f'      <a class="ds-btn ds-btn--secondary" href="#{p[0].replace(".html","") if p[0] != "sicherheitszellen.html" else "pruefstandsanlagen"}">{p[1]}</a>\n'
                 for p in PANELS)
       + '    </div>\n  </section>')

s = lies(ziel)
vorher, nachher = s[:s.index("<main id=\"inhalt\">")], s[s.index("</main>"):]
m = hauptteil(s)
hero = re.search(r'  <section class="hero-parallax".*?\n  </section>', m, re.S).group(0)
neu = ('<main id="inhalt">\n\n' + hero + "\n" + nav + "\n" + "\n".join(panels) + "\n")
with open(ziel, "w", encoding="utf-8") as f:
    f.write(vorher + neu + nachher)

for datei, _, _ in PANELS:
    p = os.path.join(SITE, datei)
    if os.path.exists(p):
        os.remove(p)
for datei in WEG:
    p = os.path.join(SITE, datei)
    if os.path.exists(p):
        os.remove(p)
print("engineering.html: %d Panels, geloescht: %s" % (len(panels), ", ".join([d for d, _, _ in PANELS] + WEG)))
