# -*- coding: utf-8 -*-
"""Schreibt Kopfmenue, Mobilmenue und die Fussleisten-Spalte "Bereiche" auf
allen Seiten neu. Ab dem Umbau vom 16.11.2026 ist das hier die massgebliche
Stelle fuer die Navigation - nicht mehr build_part1.py.

  python3 -I menue.py <website-ordner>

Mehrfach ausfuehrbar.
"""
import sys, os, re, glob

SITE = sys.argv[1]
SHOP = "https://shop.sms.gmbh"

# (Datei, Beschriftung, [Unterpunkte]) - Unterpunkte als (Datei, Beschriftung)
MENUE = [
    ("unternehmen.html", "Unternehmen", [("ueber-uns.html", "Über uns"),
                                         ("historie.html", "Schmidt Motorsport Historie")]),
    ("engineering.html", "Engineering", []),
    ("fertigung.html", "Fertigung", [("fraesen.html", "CNC-Fräsen"),
                                     ("drehen.html", "Drehen"),
                                     ("schweissen.html", "Schweißen"),
                                     ("blechbearbeitung.html", "Blechbearbeitung")]),
    ("messen.html", "Messen &amp; QM", []),
    ("elektro-kart.html", "Elektro-Kart", [("revo-sl.html", "sms revo SL"),
                                           ("revo-x.html", "sms revo X"),
                                           ("spacedrive.html", "sms revo SpaceDrive"),
                                           ("bestellformulare.html", "Bestellformulare"),
                                           ("dokumente.html", "Wichtige Dokumente")]),
]

BEREICHE = [("engineering.html", "Engineering"), ("fertigung.html", "Fertigung"),
            ("messen.html", "Messen &amp; QM"), ("elektro-kart.html", "Elektro-Kart")]


def kopf(aktiv):
    def cur(d):
        return ' aria-current="page"' if d == aktiv else ""
    teile = [f'<a class="ds-btn nav-shop" href="{SHOP}" target="_blank" rel="noopener">Kart-Shop</a>']
    for datei, text, kinder in MENUE:
        if kinder:
            drop = "".join(f'<a class="t-nav hv-primary-soft" href="{k}"{cur(k)}>{t}</a>' for k, t in kinder)
            teile.append(f'<div class="nav-group">'
                         f'<a class="t-nav hv-primary nav-group__top" href="{datei}"{cur(datei)}>'
                         f'{text}<span class="nav-group__chev" aria-hidden="true">›</span></a>'
                         f'<div class="nav-drop">{drop}</div></div>')
        else:
            teile.append(f'<a class="t-nav hv-primary" href="{datei}"{cur(datei)}>{text}</a>')
    teile.append('<a class="ds-btn ds-btn--primary nav-contact" href="kontakt.html"'
                 + cur("kontakt.html") + '>Kontakt</a>')
    return ('<nav class="nav" aria-label="Hauptnavigation">' + "".join(teile) + '</nav>')


def mobil(aktiv):
    def cur(d):
        return ' aria-current="page"' if d == aktiv else ""
    teile = [f'<a class="ds-btn mnav__cta mnav__shop" href="{SHOP}" target="_blank" rel="noopener">Kart-Shop</a>',
             f'<div class="mnav__block"><a class="t-title-md" href="index.html"{cur("index.html")}>Start</a></div>']
    for datei, text, kinder in MENUE:
        if kinder:
            zeilen = f'<a class="t-body-md" href="{datei}"{cur(datei)}>Übersicht</a>' + "".join(
                f'<a class="t-body-md" href="{k}"{cur(k)}>{t}</a>' for k, t in kinder)
            teile.append(f'<div class="mnav__block mnav__block--sub">'
                         f'<span class="t-label mnav__head">{text}</span>{zeilen}</div>')
        else:
            teile.append(f'<div class="mnav__block"><a class="t-title-md" href="{datei}"{cur(datei)}>{text}</a></div>')
    # Der Shop-Knopf steht oben, die Bloecke dazwischen kommen in einen
    # eigenen Container - der traegt auf dem Tablet den Mehrspaltensatz.
    shop, bloecke = teile[0], teile[1:]
    return ('<div class="mnav" id="mobilmenue" hidden>' + shop
            + '<div class="mnav__spalten">' + "".join(bloecke) + '</div>'
            + '<a class="ds-btn ds-btn--primary mnav__cta" href="kontakt.html">Kontakt aufnehmen</a></div>')


def bereiche():
    return "".join(f'\n        <a class="t-body-sm" href="{d}">{t}</a>' for d, t in BEREICHE)


n = 0
for pfad in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    datei = os.path.basename(pfad)
    s = alt = open(pfad, encoding="utf-8").read()
    s = re.sub(r'<nav class="nav" aria-label="Hauptnavigation">.*?</nav>', lambda m: kopf(datei), s, count=1, flags=re.S)
    s = re.sub(r'<div class="mnav" id="mobilmenue" hidden>.*?</div>\n<main', lambda m: mobil(datei) + "\n<main", s, count=1, flags=re.S)
    s = re.sub(r'(<h2 class="t-title-sm">Bereiche</h2>)(.*?)(\n      </div>)',
               lambda m: m.group(1) + bereiche() + m.group(3), s, count=1, flags=re.S)
    if s != alt:
        open(pfad, "w", encoding="utf-8").write(s)
        n += 1
print(f"Navigation neu geschrieben auf {n} Seiten")
