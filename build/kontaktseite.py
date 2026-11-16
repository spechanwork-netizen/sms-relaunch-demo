# -*- coding: utf-8 -*-
"""Erzeugt kontakt.html aus Kopf- und Fussbereich einer bestehenden Seite.

  python3 -I build/kontaktseite.py .

Das Formular laeuft ohne Server: beim Absenden entsteht eine vorbereitete
E-Mail. Soll es spaeter ueber einen Dienst oder WordPress laufen, reicht es,
am <form> action und method zu setzen - das Skript haelt sich dann heraus.
"""
import sys, os, re

SITE = sys.argv[1] if len(sys.argv) > 1 else "."
VORLAGE = "impressum.html"

KATEGORIEN = [
    ("engineering", "Engineering und Konstruktion"),
    ("fertigung", "Fertigung und CNC-Bearbeitung"),
    ("messen", "Messen und Prüfen"),
    ("vorrichtungen", "Lehren-, Messmittel- und Vorrichtungsbau"),
    ("sicherheitszellen", "Sicherheitszellen und Stützgestelle"),
    ("revo-sl", "Elektro-Kart — sms revo SL"),
    ("revo-x", "Elektro-Kart — sms revo X"),
    ("spacedrive", "Elektro-Kart — sms revo SpaceDrive"),
    ("ersatzteile", "Ersatzteile, Akkus und Ladeinfrastruktur"),
    ("support", "Technische Rückfrage zu einem Produkt"),
    ("angebot", "Angebot oder Bestellung"),
    ("presse", "Presse und Medien"),
    ("bewerbung", "Bewerbung"),
    ("sonstiges", "Sonstiges"),
]

FELD = ('<div class="feld{breit}">\n'
        '          <label for="{id}">{label}{stern}</label>\n'
        '          {steuer}\n'
        '          <p class="feld__fehler" id="{id}-fehler" hidden></p>\n'
        '        </div>')


def feld(fid, label, steuer, pflicht=False, breit=False):
    return FELD.format(id=fid, label=label, steuer=steuer,
                       stern=' <span aria-hidden="true">*</span>' if pflicht else "",
                       breit=" feld--breit" if breit else "")


def bauen():
    optionen = "\n            ".join(
        f'<option value="{w}">{t}</option>' for w, t in KATEGORIEN)
    return f'''
  <section class="hero-parallax" style="background-image:url(&quot;assets/img/bg/kontakt.jpg&quot;); padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)">
    <div style="max-width: 1440px; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 860px); gap: clamp(32px, 4vw, 48px); align-items: center">
      <div style="display: flex; flex-direction: column; gap: 16px">
        <span class="t-label" style="color: var(--on-dark)">Kontakt</span>
        <h1 class="t-display-xl" style="color: var(--on-dark); font-size: clamp(32px, 4.6vw, 56px)">Wie können wir helfen?</h1>
        <p class="t-body-md" style="color: var(--on-dark-soft)">Wählen Sie das Thema, dann landet Ihre Anfrage direkt bei den richtigen Kolleginnen und Kollegen. Wir melden uns in der Regel innerhalb eines Arbeitstages.</p>
      </div>
    </div>
  </section>
  <section data-sec="float" data-tone="canvas" style="padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)">
    <div style="max-width: 1440px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: clamp(32px, 4vw, 48px); align-items: start">
      <form class="kform" id="kontaktformular" novalidate>
        <p class="kform__hinweis">Felder mit <span aria-hidden="true">*</span> sind Pflichtfelder.</p>
        <div class="kform__raster">
          {feld("thema", "Thema", f'<select id="thema" name="thema" required>\\n            <option value="">Bitte wählen</option>\\n            {optionen}\\n          </select>', True, True)}
          {feld("name", "Name", '<input id="name" name="name" type="text" autocomplete="name" required>', True)}
          {feld("firma", "Firma", '<input id="firma" name="firma" type="text" autocomplete="organization">')}
          {feld("email", "E-Mail", '<input id="email" name="email" type="email" autocomplete="email" required>', True)}
          {feld("telefon", "Telefon", '<input id="telefon" name="telefon" type="tel" autocomplete="tel">')}
          {feld("nachricht", "Ihre Nachricht", '<textarea id="nachricht" name="nachricht" rows="7" required></textarea>', True, True)}
        </div>
        <div class="kform__zustimmung">
          <input id="datenschutz" name="datenschutz" type="checkbox" required>
          <label for="datenschutz">Ich bin damit einverstanden, dass meine Angaben zur Bearbeitung der Anfrage gespeichert werden. <a href="datenschutz.html">Datenschutzerklärung</a> <span aria-hidden="true">*</span></label>
        </div>
        <p class="feld__fehler" id="datenschutz-fehler" hidden></p>
        <div class="kform__fuellfeld" aria-hidden="true">
          <label for="webseite">Dieses Feld bitte leer lassen</label>
          <input id="webseite" name="webseite" type="text" tabindex="-1" autocomplete="off">
        </div>
        <div class="kform__aktion">
          <button class="ds-btn ds-btn--primary" type="submit">Anfrage senden</button>
          <p class="kform__status" id="kform-status" role="status" aria-live="polite"></p>
        </div>
      </form>
      <aside class="kform__neben">
        <h2 class="t-title-md">Direkt erreichen</h2>
        <p class="t-body-sm">sms engineering GmbH<br>Seckendorfer Straße 6<br>90556 Cadolzburg</p>
        <p class="t-body-sm">Telefon: <a href="tel:+499103918490">+49 9103 91849 0</a><br>E-Mail: <a href="mailto:info@sms.gmbh">info@sms.gmbh</a></p>
        <p class="t-body-sm">Technische Rückfragen zum sms revo SL, zur Ladeinfrastruktur oder zu den Akkus: Thema <em>Technische Rückfrage</em> wählen oder direkt an <a href="mailto:revo@sms.gmbh">revo@sms.gmbh</a>.</p>
      </aside>
    </div>
  </section>'''


def main():
    v = open(os.path.join(SITE, VORLAGE), encoding="utf-8").read()
    kopf = v[:v.index("<main id=")]
    fuss = v[v.index("</main>"):]
    kopf = kopf.replace("<title>Impressum", "<title>Kontakt")
    kopf = re.sub(r'<meta name="description" content="[^"]*"',
                  '<meta name="description" content="Anfrage an die sms engineering GmbH: '
                  'Engineering, Fertigung, Messtechnik oder Elektro-Kart — Thema wählen und schreiben."', kopf)
    kopf = re.sub(r'<meta property="og:title" content="[^"]*"',
                  '<meta property="og:title" content="Kontakt | sms engineering GmbH"', kopf)
    kopf = re.sub(r'<meta property="og:description" content="[^"]*"',
                  '<meta property="og:description" content="Anfrage an die sms engineering GmbH."', kopf)
    # Die Skript-Tags stehen am Seitenende, nicht im Kopf.
    fuss = fuss.replace('<script src="assets/motion.js" defer></script>',
                        '<script src="assets/motion.js" defer></script>\n'
                        '<script src="assets/form.js" defer></script>')
    seite = kopf + '<main id="inhalt">' + bauen() + "\n" + fuss
    open(os.path.join(SITE, "kontakt.html"), "w", encoding="utf-8").write(seite)
    print("kontakt.html erzeugt,", len(KATEGORIEN), "Themen")


main()
