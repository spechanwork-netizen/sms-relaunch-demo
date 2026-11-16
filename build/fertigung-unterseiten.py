# -*- coding: utf-8 -*-
"""Legt die vier Fertigungs-Unterseiten an und setzt die Panels auf die
Hauptseite. Mehrfach ausfuehrbar - bestehende Seiten werden ueberschrieben.

  python3 -I fertigung-unterseiten.py <website-ordner>

Die Texte sind ein Entwurf aus dem, was auf der Website schon belegt ist.
Keine erfundenen Maschinendaten, Toleranzen oder Zertifikate.
"""
import sys, os, re, html

SITE = sys.argv[1]
VORLAGE = os.path.join(SITE, "fertigung.html")


def punkt(text):
    return ('<li style="display: grid; grid-template-columns: 6px 1fr; gap: 14px">'
            '<span style="width: 6px; height: 6px; background: var(--primary); margin-top: 9px"></span>'
            f'<span class="t-body-md" style="color: var(--body)">{text}</span></li>')


SEITEN = [
    dict(
        datei="fraesen.html", titel="CNC-Fräsen", kurz="CNC-Fräsen",
        beschreibung="CAM-gestützte Fräsbearbeitung komplexer Bauteile – vom Einzelstück bis zur Kleinserie.",
        absatz=("Gefräst wird CAM-gestützt, direkt aus Ihren CAD-Daten. Den Schwerpunkt bilden "
                "komplexe Einzelteile und Baugruppenkomponenten in kleinen bis mittleren Stückzahlen. "
                "Die benötigten Spannvorrichtungen entstehen im eigenen Vorrichtungs- und Betriebsmittelbau, "
                "sodass auch sperrige oder dünnwandige Teile prozesssicher bearbeitet werden."),
        liste=["CAM-gestützte Programmierung aus Ihren CAD-Daten",
               "4-Achs-Bearbeitung auf der DMG MORI DMF 200 | 8",
               "Bauteile bis 2.300 mm Länge, 850 mm Breite und 900 mm Höhe",
               "Eigener Vorrichtungs-, Betriebsmittel- und Formenbau",
               "Bearbeitung nahezu aller Werkstoffe, etwa hochfeste Stähle, Aluminium, Kunststoffe und Verbundwerkstoffe",
               "Auf Wunsch mit Express-Lieferzeit"],
        bild=("assets/img/Neue-Maschine-DMF-200-8-1-320x202.jpg", "CNC-Fräsmaschine DMG MORI DMF 200 | 8", 1600, 1000),
    ),
    dict(
        datei="drehen.html", titel="Drehen", kurz="Drehen",
        beschreibung="Drehteile für Prototypen und Kleinserien, einzeln oder als Teil einer Baugruppe.",
        absatz=("Drehteile entstehen bei uns meist im Verbund mit der Fräsbearbeitung und der Montage: "
                "Wellen, Buchsen, Flansche und Aufnahmen, die anschließend direkt in die Baugruppe gehen. "
                "Ab Losgröße 1 – vom Prototyp bis zur Kleinserie, in denselben Werkstoffen wie in der "
                "Fräsbearbeitung."),
        liste=["Dreharbeiten ab Losgröße 1, Prototyp bis Kleinserie",
               "Wellen, Buchsen, Flansche und Aufnahmen für eigene Baugruppen",
               "Kombinierte Dreh- und Fräsbearbeitung aus einer Hand",
               "Hochfeste Stähle, Aluminium und Kunststoffe",
               "Maßkontrolle über die eigene 3D-Koordinatenmesstechnik"],
        bild=None,
    ),
    dict(
        datei="schweissen.html", titel="Schweißen", kurz="Schweißen",
        beschreibung="Individuelle Schweißfertigung für Rahmen, Gestelle und komplexe Baugruppen.",
        absatz=("Geschweißt wird einzelstückbezogen: Rahmen, Gestelle, Stützkonstruktionen und "
                "Prüfstandsaufbauten. Die dafür nötigen Schweißvorrichtungen konstruieren und bauen wir "
                "selbst – das hält Verzug und Maßabweichung klein und macht auch Wiederholteile "
                "reproduzierbar."),
        liste=["Individuelle Schweißfertigung für Einzelteile und Baugruppen",
               "Rahmen, Gestelle, Stützkonstruktionen und Prüfstandsaufbauten",
               "Eigener Bau der Schweißvorrichtungen",
               "Anschließende Nachbearbeitung und Montage im Haus",
               "Maßkontrolle über die eigene 3D-Koordinatenmesstechnik"],
        bild=None,
    ),
    dict(
        datei="blechbearbeitung.html", titel="Blechbearbeitung", kurz="Blechbearbeitung",
        beschreibung="Biegen, Kanten und Anarbeiten von Blechteilen für eigene Baugruppen.",
        absatz=("Blechteile ergänzen bei uns die spanende Fertigung: Verkleidungen, Halter, Konsolen und "
                "Gehäuseteile, die zusammen mit gefrästen und gedrehten Komponenten zur fertigen Baugruppe "
                "werden. Zuschnitt, Biegen und Anarbeiten stimmen wir dabei auf die anschließende Montage ab."),
        liste=["Biegen und Kanten von Blechteilen",
               "Verkleidungen, Halter, Konsolen und Gehäuseteile",
               "Abstimmung auf die anschließende Schweiß- und Montagefolge",
               "Hochfeste Stähle, Aluminium und Kunststoffe",
               "Ab Losgröße 1, Prototyp bis Kleinserie"],
        bild=None,
    ),
]

vorlage = open(VORLAGE, encoding="utf-8").read()
kopf = vorlage[:vorlage.index('<main id="inhalt">')]
fuss = vorlage[vorlage.index("</main>"):]

for s in SEITEN:
    k = kopf
    k = re.sub(r"<title>.*?</title>", f'<title>{s["titel"]} | sms engineering GmbH</title>', k, count=1)
    k = re.sub(r'<meta name="description" content="[^"]*">',
               f'<meta name="description" content="{html.escape(s["beschreibung"], quote=True)}">', k, count=1)
    k = re.sub(r'<meta property="og:title" content="[^"]*">',
               f'<meta property="og:title" content="{s["titel"]} | sms engineering GmbH">', k, count=1)
    k = re.sub(r'<meta property="og:description" content="[^"]*">',
               f'<meta property="og:description" content="{html.escape(s["beschreibung"], quote=True)}">', k, count=1)

    bild = ""
    if s["bild"]:
        src, alt, w, h = s["bild"]
        bild = (f'\n      <img loading="lazy" decoding="async" src="{src}" alt="{alt}" '
                'style="width: 100%; aspect-ratio: 16/10; object-fit: cover; display: block; '
                f'background: var(--surface-card)" width="{w}" height="{h}">')

    main = f'''<main id="inhalt">

  <section class="hero-parallax" style="background-image:url(&quot;assets/img/bg/fertigung.jpg&quot;)">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px">
      <span class="t-label" style="color: var(--on-dark)">Fertigung</span>
      <h1 class="t-display-xl" style="color: var(--on-dark); font-size: clamp(32px, 4.6vw, 56px)">{s["titel"]}</h1>
      <p class="t-body-md" style="color: var(--on-dark-soft); max-width: 660px">{s["beschreibung"]}</p>
    </div>
  </section>
  <section style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)" data-sec="float" data-tone="canvas">
    <div style="max-width: 1440px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: clamp(32px, 4vw, 48px); align-items: start">
      <p class="t-body-md" style="color: var(--body); font-size: 18px">{s["absatz"]}</p>{bild}
    </div>
  </section>
  <section style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)" data-sec="float" data-tone="soft">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: 28px">
      <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(24px, 3vw, 32px)">Leistungen im Überblick</h2>
      <ul style="list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px">
        {"".join(punkt(t) for t in s["liste"])}
      </ul>
      <div style="display: flex; flex-wrap: wrap; gap: 12px">
        <a class="ds-btn ds-btn--primary" href="kontakt.html?thema=fertigung">Anfrage senden</a>
        <a class="ds-btn ds-btn--secondary" href="fertigung.html">Zurück zur Fertigung</a>
      </div>
    </div>
  </section>
'''
    open(os.path.join(SITE, s["datei"]), "w", encoding="utf-8").write(k + main + fuss)

# ---- Panels auf der Fertigungsseite -------------------------------------
panel = "".join(
    '        <div style="border-top: 2px solid var(--primary); padding-top: 20px; display: flex; '
    'flex-direction: column; gap: 12px; align-items: flex-start">\n'
    f'          <h3 class="t-title-lg" style="color: var(--ink)">{s["titel"]}</h3>\n'
    f'          <p class="t-body-sm" style="color: var(--body)">{s["beschreibung"]}</p>\n'
    f'          <a class="ds-link" href="{s["datei"]}">Mehr erfahren<span class="ds-link__chev" aria-hidden="true">›</span></a>\n'
    '        </div>\n' for s in SEITEN)

sektion = f'''  <section style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)" data-sec="float" data-tone="canvas">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: clamp(28px, 3vw, 40px)">
      <div style="display: flex; flex-direction: column; gap: 12px; max-width: 820px">
        <span class="t-label" style="color: var(--muted)">Verfahren</span>
        <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(26px, 3.4vw, 32px)">Vier Verfahren, eine Fertigung</h2>
        <p class="t-body-md" style="color: var(--body)">Fräsen, Drehen, Schweißen und Blechbearbeitung laufen bei uns im selben Haus zusammen – einschließlich Vorrichtungsbau, Montage und Maßkontrolle.</p>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: clamp(16px, 2vw, 24px)">
{panel}      </div>
    </div>
  </section>
'''

f = open(VORLAGE, encoding="utf-8").read()
anfang = f.index("\n  </section>", f.index('class="hero-parallax"')) + len("\n  </section>\n")
if 'Vier Verfahren, eine Fertigung' in f:
    a = f.rindex("\n  <section", 0, f.index("Vier Verfahren, eine Fertigung"))
    b = f.index("\n  </section>", f.index("Vier Verfahren, eine Fertigung")) + len("\n  </section>\n")
    f = f[:a + 1] + f[b:]
f = f[:anfang] + sektion + f[anfang:]
open(VORLAGE, "w", encoding="utf-8").write(f)
print("Vier Unterseiten angelegt, Panels auf fertigung.html gesetzt")
