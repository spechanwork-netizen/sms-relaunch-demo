# -*- coding: utf-8 -*-
"""Setzt die vom Kunden gelieferten Inhalte auf die vier Fertigungs-Unterseiten.

  python3 -I fertigung-inhalte.py <website-ordner>

Ersetzt alles unterhalb des Bildkopfs. Mehrfach ausfuehrbar.
"""
import sys, os, re, html

SITE = sys.argv[1]


def sek(inhalt, ton="canvas", oben=True):
    pad = "clamp(48px, 7vw, 80px)" if oben else "0"
    return (f'  <section style="padding: {pad} clamp(20px, 4vw, 32px) clamp(48px, 7vw, 80px)" '
            f'data-sec="float" data-tone="{ton}">\n'
            '    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; '
            'gap: clamp(28px, 3vw, 40px)">\n' + inhalt + '    </div>\n  </section>\n')


def titel(h, text=None, label=None):
    s = '      <div style="display: flex; flex-direction: column; gap: 12px; max-width: 820px">\n'
    if label:
        s += f'        <span class="t-label" style="color: var(--muted)">{label}</span>\n'
    s += f'        <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(26px, 3.4vw, 32px)">{h}</h2>\n'
    if text:
        s += f'        <p class="t-body-md" style="color: var(--body)">{text}</p>\n'
    return s + '      </div>\n'


def absatz(text, breite="820px", gross=False):
    fs = "; font-size: 18px" if gross else ""
    return f'      <p class="t-body-md" style="color: var(--body); max-width: {breite}{fs}">{text}</p>\n'


def kennzahlen(paare):
    s = ('      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); '
         'gap: clamp(16px, 2vw, 24px); border-top: 1px solid var(--hairline); '
         'border-bottom: 1px solid var(--hairline)">\n')
    for wert, einheit, label in paare:
        e = f'<span class="t-title-sm ds-spec__unit">{einheit}</span>' if einheit else ""
        s += ('        <div class="ds-spec"><span class="t-display-sm ds-spec__value">'
              f'{wert}{e}</span><span class="t-label ds-spec__label">{label}</span></div>\n')
    return s + '      </div>\n'


def kacheln(eintraege, minmax="280px"):
    s = (f'      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax({minmax}, 1fr)); '
         'gap: 1px; background: var(--hairline)">\n')
    for kopf, text in eintraege:
        s += ('        <div style="background: var(--canvas); padding: clamp(20px, 2.5vw, 28px); '
              'display: flex; flex-direction: column; gap: 10px">\n'
              f'          <h3 class="t-title-lg" style="color: var(--ink)">{kopf}</h3>\n'
              f'          <p class="t-body-sm" style="color: var(--body)">{text}</p>\n'
              '        </div>\n')
    return s + '      </div>\n'


def liste(punkte, spalten=True):
    gr = ('display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px'
          if spalten else 'display: flex; flex-direction: column; gap: 14px')
    s = f'      <ul style="list-style: none; padding: 0; {gr}">\n'
    for p in punkte:
        s += ('        <li style="display: grid; grid-template-columns: 6px 1fr; gap: 14px">'
              '<span style="width: 6px; height: 6px; background: var(--primary); margin-top: 9px"></span>'
              f'<span class="t-body-md" style="color: var(--body)">{p}</span></li>\n')
    return s + '      </ul>\n'


def bilder(liste_):
    s = ('      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); '
         'gap: clamp(12px, 1.5vw, 16px)">\n')
    for src, alt, w, h in liste_:
        s += (f'        <img loading="lazy" decoding="async" src="{src}" alt="{alt}" '
              'style="width: 100%; aspect-ratio: 3/2; object-fit: cover; display: block; '
              f'background: var(--surface-card)" width="{w}" height="{h}">\n')
    return s + '      </div>\n'


def knoepfe(thema):
    return ('      <div style="display: flex; flex-wrap: wrap; gap: 12px">\n'
            f'        <a class="ds-btn ds-btn--primary" href="kontakt.html?thema={thema}">Anfrage senden</a>\n'
            '        <a class="ds-btn ds-btn--secondary" href="fertigung.html">Zurück zur Fertigung</a>\n'
            '      </div>\n')


# ---------------------------------------------------------------- Inhalte
INHALT = {}

INHALT["fraesen.html"] = dict(
    untertitel=("In unserer CAM-gestützten CNC-Abteilung fertigen wir Frästeile für Einzel- und "
                "Sonderanfertigungen, Kleinserien, den Prototypenbau sowie den Motorsport."),
    main=(
        sek(titel("Maschinenpark", label="CNC-Fräsen")
            + '      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); '
              'gap: clamp(28px, 4vw, 48px); align-items: center">\n'
            + absatz("Moderne 3-, 4- und 5-Achs-CNC-Fräsmaschinen, unter anderem "
                     "<strong>DMG 63 V</strong>, <strong>DMF 200/8</strong> und <strong>CMX 70 U</strong>.",
                     gross=True)
            + '        <img loading="lazy" decoding="async" '
              'src="assets/img/Neue-Maschine-DMF-200-8-1-320x202.jpg" '
              'alt="CNC-Fräsmaschine DMG MORI DMF 200 | 8" style="width: 100%; aspect-ratio: 3/2; '
              'object-fit: cover; display: block; background: var(--surface-card)" '
              'width="1600" height="1000">\n'
            + '      </div>\n', "canvas")
        + sek(titel("Werkstoffe", label="CNC-Fräsen")
              + absatz("Verarbeitet werden unterschiedlichste Werkstoffe wie Stahl und Werkzeugstahl, "
                       "Edelstahl, Aluminium, Buntmetalle sowie technische Kunststoffe wie PA6, POM und PEEK.",
                       gross=True)
              + absatz("Je nach Maschine und Anforderung können auch größere Bauteile und komplexe "
                       "Geometrien bearbeitet werden. Die Bearbeitungsbereiche reichen dabei von kompakten "
                       "Bauteilen bis zu Fräsarbeiten mit folgenden Abmessungen:")
              + kennzahlen([("2.000", "mm", "Länge"), ("800", "mm", "Breite"), ("750", "mm", "Höhe")]),
              "soft")
        + sek(absatz("Die Programmierung der CNC-Bearbeitung erfolgt über moderne CAM-Software von "
                     "Mastercam, Siemens NX und Creo. Dadurch lassen sich auch anspruchsvolle Einzelteile, "
                     "Prototypen und Kleinserien präzise und effizient fertigen.", gross=True)
              + knoepfe("fertigung"), "canvas")
    ))

INHALT["drehen.html"] = dict(
    untertitel="Krumme Dinger drehen ist nicht unser Ding. Wir legen Wert auf Präzision.",
    main=(
        sek(absatz("Egal ob Prototyp, Einzelanfertigung oder Kleinserie – wir fertigen Präzisionsdrehteile "
                   "nach Ihrem Wunsch und für Ihren individuellen Anwendungsbereich.", gross=True), "canvas")
        + sek(titel("Maschine")
              + absatz("Konventionelle Drehmaschine vom Typ <strong>GDW L2400 VS1</strong>.", gross=True)
              + absatz("Für weiterführende CNC-Dreh- und Fräsarbeiten greifen wir auf ein Netzwerk "
                       "langjähriger regionaler Partner zurück. So können auch äußerst komplexe "
                       "Fertigungsanforderungen flexibel und bedarfsgerecht umgesetzt werden.")
              + knoepfe("fertigung"), "soft")
    ))

# Wert, Normnummer, Kurzkennzeichnung fuers Band, Erklaerung darunter
VERFAHREN = [
    ("WIG", "141", "Dünnes Blech, Alu, Edelstahl",
     "<strong>WIG (141)</strong> – Wolfram-Inertgas: sehr saubere, genau beherrschbare Nähte, "
     "vor allem an dünnen Blechen, Aluminium und Edelstahl."),
    ("MIG", "131", "Aluminium",
     "<strong>MIG (131)</strong> – Metall-Inertgas: zügiges Schweißen unter inertem Schutzgas, "
     "überwiegend für Aluminiumlegierungen."),
    ("MAG", "135", "Bau- und Vergütungsstahl",
     "<strong>MAG (135)</strong> – Metall-Aktivgas: hohe Abschmelzleistung für Baustähle und "
     "Vergütungsstähle, das Arbeitspferd der Stahlkonstruktion."),
    ("Punktschweißen", "21", "Überlappende Bleche",
     "<strong>Widerstandspunktschweißen (21)</strong> – verbindet überlappende Bleche punktweise "
     "ohne Zusatzwerkstoff."),
]

INHALT["schweissen.html"] = dict(
    untertitel=("Unsere Schweißerei bietet umfassende Möglichkeiten zur fachgerechten Verarbeitung "
                "unterschiedlichster Werkstoffe und zur Herstellung anspruchsvoller Schweißkonstruktionen."),
    main=(
        sek(titel("Werkstoffe")
            + absatz("Verarbeitet werden unter anderem alle gängigen Baustahllegierungen wie S235 und S355, "
                     "Chrom-Molybdän-Vergütungsstähle wie 25CrMo4, Aluminiumlegierungen sowie rostfreie "
                     "Stähle wie V2A und V4A.", gross=True), "canvas")
        + sek(titel("Schweißverfahren", "Für unterschiedliche Anforderungen stehen verschiedene "
                                        "Schweißverfahren zur Verfügung:")
              + kennzahlen([(v, f" ({n})" if n else "", k) for v, n, k, _ in VERFAHREN])
              + absatz("Dabei können Stahl in Materialstärken von 0,8 bis 20 mm, rostfreier Stahl von "
                       "1 bis 20 mm sowie Aluminium von 1 bis 10 mm verarbeitet werden. Weitere "
                       "Materialstärken sind auf Anfrage möglich."), "soft")
        + sek(titel("Präzise Schweißkonstruktionen")
              + absatz("Unsere geprüften Schweißer nach DIN EN ISO 9606-1 gewährleisten eine fachgerechte "
                       "und qualitätsorientierte Ausführung. Die Schweißaufsicht erfolgt durch einen "
                       "Internationalen Schweißfachmann (DVS-IIW/EWF).", gross=True), "canvas")
        + sek(titel("Spezialgebiet: Kombinierte Dreh-Fräs-Schweiß-Baugruppen")
              + absatz("Auch Schweißkonstruktionen mit engen Toleranzen und hohen Anforderungen an die "
                       "Maßgenauigkeit sind realisierbar. Für präzise Feinbearbeitungen, beispielsweise an "
                       "Passbohrungen, Buchsen oder Planflächen, besteht die Möglichkeit der CNC-Bearbeitung "
                       "auf einer 5-Achs-Fräsmaschine.")
              + absatz("Für komplexe Aufspannungen stehen zudem modern gehärtete Schweiß- und Spanntische "
                       "zur Verfügung, die Aufspannungen auf Grundflächen von bis zu 2 × 2 m bzw. "
                       "1 × 4 m ermöglichen."), "soft")
        + sek(titel("Halbzeuge und Bauformen")
              + absatz("Neben Blechen bis zu einer Stärke von 20 mm können sämtliche gängigen Profile "
                       "verarbeitet werden. Dazu zählen beispielsweise Rund- und Vierkantrohre, "
                       "Winkelprofile, U-Profile sowie Träger in verschiedenen Ausführungen wie HEB und IPE.",
                       gross=True), "canvas")
        + sek(titel("Nachbearbeitung")
              + absatz("Für die fachgerechte Nachbearbeitung stehen verschiedene Möglichkeiten zur "
                       "Verfügung. Schweißnähte auf rostfreiem Stahl können durch elektrolytisches Beizen "
                       "gereinigt und optisch sowie technisch aufbereitet werden.", gross=True)
              + knoepfe("fertigung"), "soft")
    ))

MASCHINEN = [
    ("Elektrohydraulische Presse", "160 Tonnen Presskraft."),
    ("Segmentierbare Schwenkbiegemaschine", "1.020 mm Arbeitsbreite."),
    ("Elektrische Schlagschere", "1.350 mm Arbeitsbreite."),
    ("Rundbiege- und Sickenmaschine", "Sickenmaschine mit verschiedenen Konturaufsätzen."),
]

INHALT["blechbearbeitung.html"] = dict(
    untertitel=("In der Blechbearbeitung verarbeiten wir unterschiedlichste Stahl-, Aluminium- und "
                "Edelstahlbleche für individuelle Fertigungsanforderungen."),
    main=(
        sek(titel("Werkstoffe")
            + absatz("Zum Einsatz kommen unter anderem gängige Stahlbleche wie DC01, S235 und S355, "
                     "hochfest legierte Vergütungsstähle wie 25CrMo4 und 1.7734 sowie verschiedene "
                     "Aluminiumlegierungen und rostfreie Bleche wie V2A und V4A.", gross=True)
            + absatz("Je nach Werkstoff sind folgende Materialstärken möglich:")
            + kennzahlen([("0,8 – 3", " mm", "Stahl"), ("1 – 2", " mm", "Rostfreier Stahl"),
                          ("1 – 5", " mm", "Aluminium")])
            + absatz("Weitere Materialstärken können auf Anfrage umgesetzt werden."), "canvas")
        + sek(titel("Maschinen") + kacheln(MASCHINEN), "soft")
        + sek(titel("Schnelle Verfügbarkeiten")
              + absatz("Durch einen umfangreichen Blechlagerbestand können verschiedene Werkstoffe und "
                       "Materialstärken kurzfristig verfügbar gemacht werden. Laser-, Wasserstrahl- und "
                       "Plasmazuschnitte können zudem über ein Netzwerk langjähriger Partnerbetriebe "
                       "realisiert werden.", gross=True)
              + knoepfe("fertigung"), "canvas")
    ))

for datei, d in INHALT.items():
    pfad = os.path.join(SITE, datei)
    s = open(pfad, encoding="utf-8").read()
    # Kopf des Dokuments (bis <main>) und alles ab </main> bleiben unangetastet
    vorher = s[:s.index('<main id="inhalt">')]
    rest = s[s.index("</main>"):]
    mitte = s[s.index('<main id="inhalt">'):s.index("</main>")]
    hero = re.search(r'  <section class="hero-parallax".*?\n  </section>\n', mitte, re.S).group(0)
    # Untertitel im Bildkopf
    hero_neu = re.sub(r'(<p class="t-body-md" style="color: var\(--on-dark-soft\)[^"]*">).*?(</p>)',
                      lambda m: m.group(1) + d["untertitel"] + m.group(2), hero, count=1, flags=re.S)
    neu = '<main id="inhalt">\n\n' + hero_neu + d["main"]
    open(pfad, "w", encoding="utf-8").write(vorher + neu + rest)
    print("fertig:", datei)
