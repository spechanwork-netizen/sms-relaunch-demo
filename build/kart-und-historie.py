# -*- coding: utf-8 -*-
"""Inhaltsanpassungen vom 17.11.2026 auf Historie, Elektro-Kart, revo SL,
revo X und SpaceDrive.

  python3 -I kart-und-historie.py <website-ordner>

Mehrfach ausfuehrbar.
"""
import sys, os, re

SITE = sys.argv[1]


def lies(d):
    return open(os.path.join(SITE, d), encoding="utf-8").read()


def schreib(d, s):
    open(os.path.join(SITE, d), "w", encoding="utf-8").write(s)


def punkt(text):
    return ('<li style="display: grid; grid-template-columns: 6px 1fr; gap: 14px">'
            '<span style="width: 6px; height: 6px; background: var(--primary); margin-top: 9px"></span>'
            f'<span class="t-body-md" style="color: var(--body)">{text}</span></li>')


# ============================================================ 5 Historie
STICHPUNKTE = [
    "Ursprung als kleine Drei-Mann-Werkstatt in Nürnberg mit dem Ziel, hochwertige Produkte für den Motorsport zu entwickeln.",
    "Durch große Aufträge von Audi und Volkswagen wuchs das Unternehmen und entwickelte sich zu einem professionellen Motorsport- und Entwicklungsbetrieb.",
    "Der Rallyesport wurde zum wichtigsten Standbein, mit zahlreichen Einsätzen bei nationalen und internationalen Rallyes sowie bekannten Fahrern wie Walter Röhrl und Ari Vatanen.",
    "Schmidt Motorsport feierte zahlreiche Erfolge und Meistertitel, unter anderem mit dem Audi quattro, Porsche und Ford.",
    "Neben dem Rallyesport engagierte sich das Unternehmen auch in der DTM, im Tourenwagensport und in der Formel 1.",
    "Ein weiterer Schwerpunkt wurde die Entwicklung von Renn- und Rallyefahrzeugen, beispielsweise des legendären VW Golf A59 und des Opel Vectra STW.",
    "Durch die langjährige Zusammenarbeit mit Audi, Volkswagen und Opel etablierte sich Schmidt Motorsport als kompetenter Entwicklungs- und Fertigungspartner.",
    "Mit der Zeit zog sich das Unternehmen aus dem aktiven Motorsport zurück und konzentrierte sich zunehmend auf Fahrzeugentwicklung, Fertigung und weitere Projekte für die Industrie.",
]
s = lies("historie.html")
anfang = s.index('<ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 16px">')
ende = s.index("</ul>", anfang)
neu = ('<ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 16px">\n'
       + "".join("        " + punkt(t) + "\n" for t in STICHPUNKTE) + "      ")
schreib("historie.html", s[:anfang] + neu + s[ende:])
print("historie.html: 8 Stichpunkte ersetzt")

# ======================================================== 6 Elektro-Kart
s = lies("elektro-kart.html")
if "Bei Kart-Slalom-Veranstaltungen" not in s:
    print("elektro-kart.html / revo-sl.html: schon umgebaut")
else:
    s = re.sub(r'(<p class="t-body-md" style="color: var\(--on-dark-soft\)">).*?(</p>)',
               lambda m: m.group(1) + "Das eKart von sms engineering wurde speziell für den Kart-Slalom – die "
                         "Einstiegsdisziplin in den Motorsport – entwickelt. Unser sms revo SL ist ein "
                         "High-Quality-Produkt – Made in Germany." + m.group(2), s, count=1, flags=re.S)

    # Einleitungssektion neu
    a = s.index('<p class="t-body-md" style="color: var(--body)">Bei Kart-Slalom-Veranstaltungen')
    b = s.index("</p>", s.index("Beitrag zum langfristigen Erhalt des Kartsports")) + len("</p>")
    einleitung = (
        '<p class="t-body-md" style="color: var(--body)">Die Kart-Slalom-Disziplin befindet sich aktuell im '
        'Wandel. Kamen in der Vergangenheit überwiegend Karts mit Verbrennermotoren zum Einsatz, zieht seit '
        'einigen Jahren der Elektro-Antrieb im Kart-Slalom-Bereich ein. Ein Technologie-Vorreiter und das '
        'BESTE Kart für diese Disziplin: unser <a href="revo-sl.html">sms revo SL</a>. Die Entwicklung des '
        'Elektro-Slalom-Karts ist damit nicht nur ein Schritt in Richtung Nachhaltigkeit und Elektrifizierung '
        'des Motorsports, sondern auch ein Beitrag zum langfristigen Erhalt des Kartsports.</p>\n'
        '      <p class="t-body-md" style="color: var(--body)">Neben dem sms revo SL hat sms engineering noch '
        'zwei weitere elektrisch angetriebene Ableger im Portfolio – den Mini-Buggy '
        '<a href="revo-x.html">revo X</a> und das joystick-gesteuerte '
        '<a href="spacedrive.html">revo SpaceDrive</a>.</p>')
    s = s[:a] + einleitung + s[b:]

    # Vorteile-Sektion herausnehmen (zieht auf die revo-SL-Seite um)
    i = s.index(">Vorteile und technischer Aufbau</h2>")
    va = s.rindex("\n  <section", 0, i)
    vb = s.index("\n  </section>", i) + len("\n  </section>")
    VORTEILE = s[va:vb]
    s = s[:va] + s[vb:]

    # Modelle: die ersten beiden Karten bekommen vorerst dasselbe Bild
    BILD = ('<img class="ds-card__photo" src="assets/img/sms-e-Kart-Training-1024x683.jpg" alt="%s" '
            'loading="lazy" decoding="async" style="aspect-ratio:16/10;object-fit:cover" '
            'width="1600" height="1000">')
    for name in ("sms revo SL", "sms revo X"):
        marke = f'<article class="ds-card"><div class="ds-card__body"><h3 class="t-title-md">{name}</h3>'
        if marke in s:
            s = s.replace(marke, '<article class="ds-card">' + (BILD % name)
                          + f'<div class="ds-card__body"><h3 class="t-title-md">{name}</h3>', 1)
    schreib("elektro-kart.html", s)
    print("elektro-kart.html: Untertitel, Einleitung, Modellbilder; Vorteile ausgebaut")

    # =========================================================== 7 revo SL
    vor = VORTEILE
    vor = vor.replace(
        "Konzeption, Softwareentwicklung und Aufbau finden vollständig innerhalb der sms engineering GmbH statt.",
        "Konzeption, Entwicklung, Fertigung, Softwareentwicklung und Aufbau finden vollständig innerhalb der "
        "sms engineering GmbH statt.</p>\n          <p class=\"t-body-sm\" style=\"color: var(--body)\">"
        "<strong>Made in Germany</strong>")
    vor = vor.replace("hält die Leistung über die gesamte Laufzeit konstant",
                      "hält die Leistung über die gesamte Akku-Laufzeit konstant")
    vor = vor.replace("sorgt für bessere Gewichtsverteilung", "sorgt für optimale Gewichtsverteilung")

    NEUE_KACHELN = [
        ("Allwettertauglich", "Zuverlässig bei jedem Wetter – auch bei Regen und Nässe."),
        ("Höchste Qualität", "Robust, langlebig und professionell verarbeitet."),
        ("Top Preis-Leistungsverhältnis", "Das sms revo SL bietet die beste Performance zum fairen Preis."),
    ]
    kacheln = "".join(
        '        <div style="background: var(--canvas); padding: clamp(20px, 2.5vw, 28px); display: flex; '
        'flex-direction: column; gap: 10px">\n'
        f'          <h3 class="t-title-lg" style="color: var(--ink)">{k}</h3>\n'
        f'          <p class="t-body-sm" style="color: var(--body)">{t}</p>\n'
        '        </div>\n' for k, t in NEUE_KACHELN)
    ende_raster = vor.rindex("      </div>\n")
    vor = vor[:ende_raster] + kacheln + vor[ende_raster:]
    # auf der neuen Seite ist es nicht mehr die oberste Ueberschrift
    vor = vor.replace('data-tone="soft"', 'data-tone="soft"', 1)

    s = lies("revo-sl.html")
    a = s.index('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); '
                'gap: clamp(24px, 3vw, 40px)">')
    b = s.index("\n  </section>", a) + len("\n  </section>")
    oben = (
        '<div style="display: flex; flex-direction: column; gap: 12px; max-width: 820px">\n'
        '        <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(26px, 3.4vw, 32px)">'
        'DAS BESTE Elektro-Kart für den Kart-Slalom</h2>\n'
        '      </div>\n'
        '      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); '
        'gap: clamp(24px, 3vw, 40px)">\n'
        '        <p class="t-body-md" style="color: var(--body)">Die Sitzposition ist zentral, die '
        'Leistungsentfaltung des E-Antriebs kompromisslos und in verschiedenen Leistungsstufen einstellbar, '
        'die Fahreigenschaften dank des eigenständigen Konzepts außergewöhnlich. Kurzum: das perfekte '
        'Fahrgerät für jeden Slalom-Parcours.</p>\n'
        '        <p class="t-body-md" style="color: var(--body)">Alle Details und technischen Fakten stehen im '
        'technischen Datenblatt. Ihre Anfrage stellen Sie über das '
        '<a href="kontakt.html?thema=revo-sl">Kontaktformular</a> – wir senden Infomaterial und aktuelle '
        'Angebote zu.</p>\n'
        '      </div>\n'
        '    </div>\n  </section>')
    s = s[:a] + oben + vor + s[b:]
    # alles darunter (Kennzahlen, Premierentext, Profi-Sektion) entfaellt
    rest_a = s.index("\n  <section", s.index("Top Preis-Leistungsverhältnis"))
    schreib("revo-sl.html", s[:rest_a] + "\n" + s[s.index("</main>"):])
    print("revo-sl.html: Ueberschrift, neuer Text, Vorteile-Panel, Rest entfernt")

# ============================================================ 8 revo X
s = lies("revo-x.html")
if "Eigensichere Batterie" not in s:
    print("revo-x.html: schon erledigt")
else:
  i = s.index("Eigensichere Batterie")
  a = s.rindex("<li ", 0, i)
  b = s.index("</li>", i) + len("</li>")
  vorzeile = s.rindex("\n", 0, a)
  schreib("revo-x.html", s[:vorzeile] + s[b:])
  print("revo-x.html: Stichpunkt zur Batterie entfernt")

# ======================================================== 9 SpaceDrive
s = lies("spacedrive.html")
s = re.sub(r'(<p class="t-body-md" style="color: var\(--on-dark-soft\)">).*?(</p>)',
           lambda m: m.group(1) + "Das inklusive Elektro-Kart mit Steuerungselementen von PARAVAN: "
                     "Statt Lenkrad und Pedalen dienen Joysticks und / oder ein Gas-Brems-Schieber "
                     "der Bedienung." + m.group(2), s, count=1, flags=re.S)

hero_ende = s.index("\n  </section>", s.index('class="hero-parallax"')) + len("\n  </section>\n")
INHALT = '''  <section style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)" data-sec="float" data-tone="canvas">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: clamp(28px, 3vw, 40px)">
      <div style="display: flex; flex-direction: column; gap: 12px; max-width: 820px">
        <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(26px, 3.4vw, 32px)">Das Kart</h2>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: clamp(28px, 4vw, 48px); align-items: start">
        <div style="display: flex; flex-direction: column; gap: 20px">
          <p class="t-body-md" style="color: var(--body)">Beim sms revo SpaceDrive handelt es sich um ein innovatives Elektro-Kart, das mit Steuerungselementen von PARAVAN ausgestattet ist. Statt mit Lenkrad und Pedalen wird dieses Kart mit zwei 2-Wege-Joysticks oder einem 4-Wege-Joystick (für Einhandbedienung) gefahren. Die bewährte „Drive-by-Wire“-Technologie Space&nbsp;Drive&nbsp;II sorgt außerdem dafür, dass die Fahr- und Lenkbefehle ohne direkte mechanische Verbindung elektrisch übertragen werden.</p>
          <p class="t-body-md" style="color: var(--ink); font-size: 18px; border-left: 3px solid var(--primary); padding-left: 20px">Auf diese Weise können auch Menschen am E-Kart-Sport teilnehmen, denen normalerweise die körperlichen Möglichkeiten fehlen, eine herkömmliche Kart-Lenkung zu bedienen. Die E-Karts sind zudem so konzipiert, dass sie je nach Einschränkung individuell angepasst werden können.</p>
        </div>
        <img loading="lazy" decoding="async" src="assets/img/United-in-Dreams-6-scaled.jpg" alt="" style="width: 100%; aspect-ratio: 3/2; object-fit: cover; display: block; background: var(--surface-card)" width="1600" height="1000">
      </div>
    </div>
  </section>
  <section style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)" data-sec="float" data-tone="soft">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: clamp(28px, 3vw, 40px)">
      <div style="display: flex; flex-direction: column; gap: 12px; max-width: 820px">
        <h2 class="t-display-md" style="color: var(--ink); font-size: clamp(26px, 3.4vw, 32px)">Die Events</h2>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: clamp(24px, 3vw, 40px)">
        <p class="t-body-md" style="color: var(--body)">Zum Einsatz kommt das sms revo SpaceDrive in der dmsj – Deutsche Meisterschaft im inklusiven E-Kart-Slalom (iDKSM) sowie in der Inklusiven E-Kart-Slalom-Trophy. Bei diesen Veranstaltungen können sich Motorsporttalente mit und ohne körperliche Einschränkungen im gleichen Wettbewerb messen. Seit 2023 wird in der iDKSM der Titel des Deutschen Meisters im inklusiven E-Kart-Slalom mit sms revo SpaceDrive Karts ausgefahren.</p>
        <p class="t-body-md" style="color: var(--body)">Veranstalter der Events ist das Projekt <a href="https://www.unitedindreams.de/" target="_blank" rel="noopener">„United in Dreams“</a>, das vom gemeinnützigen Verein x4in – Experience for Innovation e.&nbsp;V. in Kooperation mit dem Deutschen Motorsport Bund (DMSB) initiiert wurde.</p>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 12px">
        <a class="ds-btn ds-btn--primary" href="kontakt.html?thema=spacedrive">Anfrage senden</a>
        <a class="ds-btn ds-btn--secondary" href="downloads/Flyer_sms-revo-SpaceDrive.pdf">Technisches Datenblatt</a>
      </div>
    </div>
  </section>
'''
schreib("spacedrive.html", s[:hero_ende] + INHALT + s[s.index("</main>"):])
print("spacedrive.html: zwei Panels, dekoratives Bild, Untertitel")
