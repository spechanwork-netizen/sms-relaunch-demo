# -*- coding: utf-8 -*-
"""Leitet Anfrage-Aufforderungen auf das Kontaktformular statt auf mailto:.

  python3 -I build/anfragen.py .

Die reine E-Mail-Adresse als Knopfbeschriftung ist eine Sackgasse: sie
oeffnet ein Mailprogramm, das nicht jeder eingerichtet hat, und sie sagt
nicht, was danach passiert. Wo der Kunde zur Anfrage aufgefordert wird,
zeigt der Weg jetzt auf das Formular - mit passend vorgewaehltem Thema.

Unberuehrt bleiben die Adressen im Fussbereich und auf der Kontaktseite:
dort sind sie Kontaktangabe, keine Handlungsaufforderung.
"""
import sys, os

SITE = sys.argv[1] if len(sys.argv) > 1 else "."

ERSETZUNGEN = {
    "index.html": [(
        '<a class="ds-btn ds-btn--primary" href="mailto:info@sms.gmbh">info@sms.gmbh</a>',
        '<a class="ds-btn ds-btn--primary" href="kontakt.html">Anfrage senden</a>',
    )],
    "revo-x.html": [(
        'href="mailto:revo@sms.gmbh">Schnuppertag anfragen</a>',
        'href="kontakt.html?thema=revo-x">Schnuppertag anfragen</a>',
    )],
    "revo-sl.html": [(
        'Anfragen richten Sie direkt an <a href="mailto:revo@sms.gmbh">revo@sms.gmbh</a> '
        '\u2013 wir senden Infomaterial und aktuelle Angebote zu.',
        'Ihre Anfrage stellen Sie über das <a href="kontakt.html?thema=revo-sl">Kontaktformular</a> '
        '\u2013 wir senden Infomaterial und aktuelle Angebote zu.',
    )],
    "bestellformulare.html": [(
        'Offene Fragen? Schreiben Sie an <a href="mailto:revo@sms.gmbh">revo@sms.gmbh</a> '
        'oder rufen Sie an: <a href="tel:+499103918490">+49 9103 918490</a>.',
        'Offene Fragen? Stellen Sie sie über das '
        '<a href="kontakt.html?thema=angebot">Kontaktformular</a> oder rufen Sie an: '
        '<a href="tel:+499103918490">+49 9103 918490</a>.',
    )],
}

n = 0
offen = []
for seite, paare in ERSETZUNGEN.items():
    p = os.path.join(SITE, seite)
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    for alt, neu in paare:
        if neu in s:
            continue                      # schon umgestellt
        if alt not in s:
            offen.append(f"{seite}: Fundstelle nicht gefunden")
            continue
        s = s.replace(alt, neu, 1)
        n += 1
    open(p, "w", encoding="utf-8").write(s)
print(f"{n} Anfrage-Verweise auf das Kontaktformular gelegt")
for x in offen:
    print("  offen:", x)
