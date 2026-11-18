# -*- coding: utf-8 -*-
"""Textanpassungen vom 18.11.2026 auf Ueber uns, Historie, Fertigung, Engineering.

  python3 -I texte-18-11.py <website-ordner>

Mehrfach ausfuehrbar.
"""
import sys, os, re

SITE = sys.argv[1]


def lies(d):
    return open(os.path.join(SITE, d), encoding="utf-8").read()


def schreib(d, s):
    open(os.path.join(SITE, d), "w", encoding="utf-8").write(s)


def tausche(s, alt, neu, datei, pflicht=True):
    if alt not in s:
        if pflicht:
            raise SystemExit(f"nicht gefunden in {datei}: {alt[:70]}")
        return s
    return s.replace(alt, neu, 1)


def punkt(text):
    return ('<li style="display: grid; grid-template-columns: 6px 1fr; gap: 14px">'
            '<span style="width: 6px; height: 6px; background: var(--primary); margin-top: 9px"></span>'
            f'<span class="t-body-md" style="color: var(--body)">{text}</span></li>')


# ============================================ 1. Ueber uns: Band nach oben
s = lies("ueber-uns.html")
m = re.search(r'\n      <div style="display: flex; flex-direction: column; gap: 8px; '
              r'margin-top: clamp\(8px, 1\.5vw, 16px\)">.*?\n      </div>', s, re.S)
if m:
    band = m.group(0)
    s = s[:m.start()] + s[m.end():]
    # vor das Raster mit den drei Spalten setzen
    i = s.index('      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))')
    band = band.lstrip("\n").replace("margin-top: clamp(8px, 1.5vw, 16px)", "margin-bottom: clamp(8px, 1.5vw, 16px)")
    s = s[:i] + band + "\n" + s[i:]
    schreib("ueber-uns.html", s)
    print("ueber-uns.html: Stichwortband steht jetzt ueber den drei Kacheln")
else:
    print("ueber-uns.html: Band schon oben")

# ============================================== 2. Historie: Chronik 1992
s = lies("historie.html")
if "1993 / 1994" in s:
    i = s.index(">1993 / 1994<")
    a = s.rindex('        <div style="background: var(--canvas);', 0, i)
    b = s.index("        </div>\n", i) + len("        </div>\n")
    s = s[:a] + s[b:]
    print("historie.html: Kachel 1993 / 1994 entfernt")
if ">1992<" not in s:
    neu = ('        <div style="background: var(--canvas); padding: clamp(20px, 2.5vw, 28px); '
           'display: flex; flex-direction: column; gap: 12px">\n'
           '          <span class="t-display-sm" style="color: var(--primary)">1992</span>\n'
           '          <p class="t-body-sm" style="color: var(--body)">Entwicklung des legendären '
           'Golf A59 für die Rallye-Weltmeisterschaft im Auftrag von Volkswagen.</p>\n'
           '        </div>\n')
    i = s.index(">1993<")
    a = s.rindex('        <div style="background: var(--canvas);', 0, i)
    s = s[:a] + neu + s[a:]
    print("historie.html: Kachel 1992 vor 1993 eingefuegt")
schreib("historie.html", s)

# ================================================== 3. Fertigung
d = "fertigung.html"
s = lies(d)
s = tausche(s, ">Fertigung</h1>", ">Individuell. Präzise. Zuverlässig.</h1>", d)
s = tausche(s, "laufen bei uns im selben Haus zusammen", "laufen bei uns unter einem Dach zusammen", d)
# Stichpunkt mit der Messplatte
i = s.find("Messplatte mit mobilem Messarm")
if i != -1:
    a = s.rindex("<li ", 0, i)
    b = s.index("</li>", i) + len("</li>")
    vor = s.rindex("\n", 0, a)
    s = s[:vor] + s[b:]
    print("fertigung.html: Stichpunkt zur Messplatte entfernt")
# Ueberschrift Qualitaetskontrolle auf die Groesse von Montage
s = tausche(s, '<h3 class="t-title-lg" style="color: var(--ink)">Qualitätskontrolle</h3>',
            '<h3 class="t-display-md" style="color: var(--ink); font-size: clamp(24px, 3vw, 32px)">'
            'Qualitätskontrolle</h3>', d, pflicht=False)
s = tausche(s, "bearbeitet Bauteile bis 2.300 mm Länge", "bearbeitet Bauteile bis 2.000 mm Länge", d, pflicht=False)
schreib(d, s)
print("fertigung.html: Titel, Text, Ueberschrift und Maschinenmass angepasst")

# ================================================= 4. Engineering
d = "engineering.html"
s = lies(d)
s = tausche(s, ">Entwickeln, auslegen, absichern</h1>", ">Entwicklung. Innovation. Qualität.</h1>", d, pflicht=False)
s = re.sub(r'(<p class="t-body-md" style="color: var\(--on-dark-soft\); max-width: 640px">).*?(</p>)',
           lambda m: m.group(1) + "Egal ob Einzelbauteil oder komplexe Baugruppe, wir finden für Sie die "
                     "perfekte Lösung und werden Sie begeistern – von der Konzeptphase bis zum "
                     "geprüften Bauteil." + m.group(2), s, count=1, flags=re.S)
# Sprungleiste raus
m = re.search(r'  <section style="padding: clamp\(48px, 7vw, 80px\) clamp\(20px, 4vw, 32px\) 0".*?\n  </section>\n', s, re.S)
if m:
    s = s[:m.start()] + s[m.end():]
    print("engineering.html: Sprungleiste entfernt")
s = s.replace("Serien- und Motorsportanwendungen", "Vorserien-, Anlagen- und Motorsportanwendungen")
# beide Kachelzeilen raus
for marke in ('alt="Gesamtfahrzeuge"', 'alt="Messvorrichtung"'):
    if marke in s:
        i = s.index(marke)
        a = s.rindex('      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))', 0, i)
        b = s.index("\n      </div>", s.index("</article>", i)) + len("\n      </div>")
        s = s[:a] + s[b:].lstrip("\n")
        print("engineering.html: Kachelzeile entfernt (" + marke + ")")
# Stichpunkte Konstruktion
NEU = ["Erarbeitung von Konzepten für Komponenten und Baugruppen",
       "Entwicklung an bestehenden Baugruppen",
       "Konstruktion mit branchenüblichen CAD-Systemen",
       "Auslegung der benötigten Vorrichtungen, Werkzeuge und Formen",
       "Streng vertrauliche Vorentwicklungsprojekte"]
i = s.index("Erarbeitung von Konzepten")
a = s.rindex("<ul ", 0, i)
b = s.index("</ul>", i) + len("</ul>")
kopf = s[a:s.index(">", a) + 1]
s = s[:a] + kopf + "\n" + "".join("        " + punkt(t) + "\n" for t in NEU) + "      </ul>" + s[b:]
print("engineering.html: Stichpunkte der Konstruktion ersetzt")
# Lehren: beide Spaltentexte
s = tausche(s, "Höchste Ansprüche an Qualität und Präzision entscheiden über den Kauf und sind "
               "Voraussetzung für eine erfolgreiche Geschäftsbeziehung. Anhand der Messaufgabe "
               "erarbeiten wir gemeinsam mit Ihnen die optimale messtechnische Lösung.",
            "Höchste Ansprüche an Qualität und Präzision sind der Grundstein für ein erfolgreiches "
            "Produkt und damit für wirtschaftlichen Erfolg. Gemeinsam erarbeiten wir mit Ihnen die "
            "optimale messtechnische Lösung für Ihr Projekt.", d, pflicht=False)
m = re.search(r'(<p class="t-body-md" style="color: var\(--body\)">)Unsere Mess- und Prüfvorrichtungen '
              r'arbeiten statisch.*?(</p>)', s, re.S)
if m:
    s = s[:m.start()] + m.group(1) + ("Unsere Mess- und Prüfvorrichtungen arbeiten statisch oder "
        "dynamisch, manuell oder automatisiert. Die Auswertung reicht von anzeigenden Messgeräten "
        "wie Messuhren bis zur automatischen Datenerfassung.") + m.group(2) + s[m.end():]
    print("engineering.html: Spaltentexte beim Messmittelbau ersetzt")
schreib(d, s)
