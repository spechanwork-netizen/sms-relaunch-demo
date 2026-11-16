# -*- coding: utf-8 -*-
"""Nimmt „Aktuelles" von der Website und setzt den Shop-Link an seine Stelle.

  python3 -I shop-und-aktuelles.py <website-ordner>

  * aktuelles.html und die sechs Beitragsseiten werden geloescht
  * der Menuepunkt „Aktuelles" verschwindet aus Kopf- und Mobilmenue
  * an erster Stelle im Kopfmenue steht ein Shop-Knopf im Stil des
    Kontakt-Knopfs, Ziel https://shop.sms.gmbh in einem neuen Tab
  * im Fussbereich steht „Shop" als erster Eintrag unter „Links"
  * der Aktuelles-Abschnitt der Startseite und der Beitragsverweis auf der
    Fertigungsseite fallen weg

Mehrfach ausfuehrbar.
"""
import sys, os, re, glob

SITE = sys.argv[1]
SHOP = "https://shop.sms.gmbh"
KNOPF = (f'<a class="ds-btn ds-btn--primary nav-shop" href="{SHOP}"'
         ' target="_blank" rel="noopener">Shop</a>')
MKNOPF = (f'<a class="ds-btn ds-btn--primary mnav__cta mnav__shop" href="{SHOP}"'
          ' target="_blank" rel="noopener">Shop</a>')
FUSS = (f'        <a class="t-body-sm" href="{SHOP}"'
        ' target="_blank" rel="noopener">Shop</a>\n')

# ------------------------------------------------------------- loeschen
weg = ["aktuelles.html"] + sorted(os.path.basename(p)
                                  for p in glob.glob(os.path.join(SITE, "beitrag-*.html")))
geloescht = []
for name in weg:
    p = os.path.join(SITE, name)
    if os.path.exists(p):
        os.remove(p)
        geloescht.append(name)

# ------------------------------------------------------------- umbauen
NAV_ALT = re.compile(r'<a class="t-nav hv-primary" href="aktuelles\.html"[^>]*>Aktuelles</a>')
MOB_ALT = re.compile(r'<a class="t-title-md" href="aktuelles\.html"[^>]*>Aktuelles</a>')

def aktuelles_abschnitt_raus(s):
    """Entfernt auf der Startseite die Sektion mit der Ueberschrift Aktuelles."""
    m = re.search(r'<h2[^>]*>Aktuelles</h2>', s)
    if not m:
        return s
    start = s.rfind("\n  <section", 0, m.start())
    ende = s.find("\n  </section>", m.end())
    if start == -1 or ende == -1:
        return s
    return s[:start] + s[ende + len("\n  </section>"):]

def tonwechsel(s):
    """Verhindert zwei gleich getoente Sektionen nebeneinander.

    Durch das Entfernen des Aktuelles-Abschnitts stossen auf der Startseite
    zwei weisse Sektionen aneinander und verschmelzen optisch zu einem Block.
    Die zweite bekommt dann den hellgrauen Ton.
    """
    stellen = [m for m in re.finditer(r'data-sec="[a-z]+" data-tone="([a-z]+)"', s)]
    vorher = None
    versatz = 0
    for m in stellen:
        ton = m.group(1)
        if ton == vorher == "canvas":
            a, b = m.start(1) + versatz, m.end(1) + versatz
            s = s[:a] + "soft" + s[b:]
            versatz += len("soft") - len(ton)
            ton = "soft"
        vorher = ton
    return s


bericht = []
for pfad in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    with open(pfad, encoding="utf-8") as f:
        s = alt = f.read()

    # Kopfmenue: Aktuelles raus, Shop-Knopf an dieselbe (erste) Stelle
    if NAV_ALT.search(s):
        s = NAV_ALT.sub(KNOPF, s, count=1)
    elif "nav-shop" not in s:
        s = s.replace('<nav class="nav" aria-label="Hauptnavigation">',
                      '<nav class="nav" aria-label="Hauptnavigation">' + KNOPF, 1)

    # Mobilmenue: Aktuelles raus, Shop-Knopf ganz nach oben
    s = MOB_ALT.sub("", s)
    if "mnav__shop" not in s:
        s = s.replace('<div class="mnav" id="mobilmenue" hidden>',
                      '<div class="mnav" id="mobilmenue" hidden>' + MKNOPF, 1)

    # Fussbereich: Shop als erster Eintrag unter „Links"
    if SHOP not in s.split('<h2 class="t-title-sm">Links</h2>')[-1][:400]:
        s = s.replace('        <h2 class="t-title-sm">Links</h2>\n',
                      '        <h2 class="t-title-sm">Links</h2>\n' + FUSS, 1)

    if os.path.basename(pfad) == "index.html":
        s = tonwechsel(aktuelles_abschnitt_raus(s))
    if os.path.basename(pfad) == "fertigung.html":
        s = re.sub(r'\n *<a class="ds-link" href="beitrag-[^"]*">.*?</a>', "", s)

    if s != alt:
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(s)
        bericht.append(os.path.basename(pfad))

print("geloescht:", ", ".join(geloescht) or "nichts")
print("umgebaut :", len(bericht), "Seiten")
rest = [p for p in glob.glob(os.path.join(SITE, "*.html"))
        if "aktuelles.html" in open(p, encoding="utf-8").read()
        or "beitrag-" in open(p, encoding="utf-8").read()]
print("Restverweise:", ", ".join(os.path.basename(p) for p in rest) or "keine")
