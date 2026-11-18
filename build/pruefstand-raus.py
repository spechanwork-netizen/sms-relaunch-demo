# -*- coding: utf-8 -*-
"""Nimmt das Panel „Pruefstands- und Sonderanlagen" samt Video von der
Engineering-Seite und entfernt die Zwei-Klick-Loesung wieder.

  python3 -I pruefstand-raus.py <website-ordner>

Mehrfach ausfuehrbar.
"""
import sys, os, re

SITE = sys.argv[1]


def lies(d):
    return open(os.path.join(SITE, d), encoding="utf-8").read()


def schreib(d, s):
    open(os.path.join(SITE, d), "w", encoding="utf-8").write(s)


# ------------------------------------------------- Panel und Sprungknopf
s = lies("engineering.html")
if 'id="pruefstandsanlagen"' in s:
    a = s.index('  <section id="pruefstandsanlagen"')
    b = s.index("</main>", a)
    s = s[:a] + s[b:]
    s = re.sub(r'\s*<a class="ds-btn ds-btn--secondary" href="#pruefstandsanlagen">[^<]*</a>', "", s)
    print("engineering.html: Panel, Video und Sprungknopf entfernt")
else:
    print("engineering.html: Panel schon entfernt")

# Zaehlwort: es sind jetzt zwei Kompetenzfelder
s = s.replace("Drei Kompetenzfelder", "Zwei Kompetenzfelder")
s = s.replace("Vier Kompetenzfelder", "Zwei Kompetenzfelder")
schreib("engineering.html", s)

# ------------------------------------------------------ Zwei-Klick-Lösung
# CSS-Block
CSS_START = "/* --- Video mit Zwei-Klick-Loesung"
for d in ("assets/site.css", "build/build_part2.py"):
    s = lies(d)
    if CSS_START in s:
        a = s.index(CSS_START)
        b = s.index("/* --- Rechtsseiten", a)
        schreib(d, s[:a] + s[b:])
        print("CSS entfernt:", d)

# JS-Block
JS_START = "  /* --- Video mit Zwei-Klick-Loesung"
for d in ("assets/site.js", "build/build_part2.py"):
    s = lies(d)
    if JS_START in s:
        a = s.index(JS_START)
        b = s.index("  });", s.index("k.replaceWith(f);", a)) + len("  });\n")
        schreib(d, s[:a] + s[b:])
        print("JS entfernt:", d)

for weg in ("build/video-zweiklick.py",):
    p = os.path.join(SITE, weg)
    if os.path.exists(p):
        os.remove(p)
        print("geloescht:", weg)
