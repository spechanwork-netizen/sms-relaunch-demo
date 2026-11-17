# -*- coding: utf-8 -*-
"""Welches Foto kommt auf welchen Bildplatz.

(ziel, quelle, modus, fokus_x, fokus_y, zoom, hintergrund)
  modus   "cover"   fuellt den Rahmen, schneidet ueber
          "contain" passt vollstaendig hinein (Logos, Organigramm)
  fokus   0..1, wohin der Zuschnitt rutscht (0.5/0.5 = Mitte)
  zoom    1.0 = ganzes Bild, 0.6 = mittlere 60 % (fuer zweite Zuschnitte)
Was hier nicht steht, behaelt bewusst die Zeichnung - lieber eine ehrliche
Illustration als ein Foto, das nicht zum Text passt oder sich wiederholt.
"""

INHALT = [
    # --- Leistungen / Technik ------------------------------------------
    ("sms_konstruktion_entwicklung_01.png", "engineering.jpg",            "cover", .50, .50, 1.0),
    ("sms_fertigung_montage_01.png",        "Schweissen-01.png",          "cover", .46, .46, 1.0),
    ("sms_lehren-messmittelbau_01.png",     "messmittel_banner.jpg",      "cover", .42, .50, 1.0),
    ("engineering.jpg",                     "Fertigteil.jpg",             "cover", .50, .52, 1.0),
    ("Neue-Maschine-DMF-200-8-1-320x202.png", "Fraese-gross-02.png",      "cover", .50, .48, 1.0),
    ("sms_lehren-messmittelbau_03.png",     "Pressen-01-ohne-orange.png", "cover", .50, .50, 0.92),
    ("sms_konstruktion_entwicklung_02.png", "Drehen-03.png",              "cover", .50, .50, 0.90),
    ("sms_konstruktion_entwicklung_03.png", "Blechbearbeitung-neu.png",   "cover", .50, .52, 1.0),
    ("sms_lehren-messmittelbau_02.png",     "Blechbearbeitung-neu.png",   "cover", .28, .50, 0.58),
    ("sms_stuetzgestelle_02.jpg",           "sicherheitszellen_banner.jpg", "cover", .50, .50, 1.0),
    ("sms_stuetzgestelle.jpg",              "Rohrbiegen-neu.png",         "cover", .50, .50, 1.0),
    ("sms_stuetzgestelle_03.jpg",           "rastaurierung_banner.jpg",   "cover", .50, .50, 1.0),
    ("sms_emobilitaet.jpg",                 "emobility.jpg",              "cover", .50, .50, 1.0),
    ("Universal-Antriebsstrang-sms-engineering-320x202.png", "emobility.jpg", "cover", .40, .50, 0.70),
    # --- Karts ----------------------------------------------------------
    ("E-Kart-sms-engineering-2-1024x683.jpg", "E-Kart-sms-engineering.jpg", "cover", .50, .52, 1.0),
    ("IMG_2384-scaled.jpg",                 "E-Kart-sms-engineering.jpg", "cover", .44, .54, 0.62),
    ("Elektro-Slalom-Kart.jpg",             "E-Kart-sms-engineering.jpg", "cover", .60, .50, 0.78),
    ("sms-e-Kart-Training-1024x683.jpg",    "Hintergrund-leomax-01.png",  "cover", .50, .50, 1.0),
    ("sms-revo-SL-Hockenheimring-11-scaled.jpg", "Hintergrund-leomax-01.png", "cover", .34, .52, 0.68),
    ("revo-SL-@DKSM-Finale-320x202.png",    "revo-SL-@DKSM-Finale.png",   "cover", .50, .56, 1.0),
    ("sms-revo-SL-Hockenheimring-13-scaled-e1666783706334.jpg", "revo-SL-@DKSM-Finale.png", "cover", .50, .62, 0.82),
    ("revo-SL-@Bundesendlauf-320x202.png",  "20210813_DMSB_EKart-0258_50.jpg", "cover", .50, .50, 1.0),
    ("Inklusives-Kart-1024x683.jpg",        "20210813_DMSB_EKart-0258_50.jpg", "cover", .42, .54, 0.80),
    ("smsengineering_Website_Bild_Vertriebspartnerschaft_Beule.png", "Kart-Aufnahme.jpg", "cover", .50, .50, 1.0),
    ("Elektro-Slalom-Kart-Bad-Aibling.jpg", "Kart-Aufnahme.jpg",          "cover", .55, .48, 0.84),
    # --- Unternehmen ----------------------------------------------------
    ("Freigestellt-01-GUT-e1786614143161.png", "Freigestellt-01-GUT.png", "cover", .50, .46, 1.0, "#fafafa"),
    ("leomax-firmenstruktur_Zeichenflaeche-1.png", "leomax-firmenstruktur_Zeichenflaeche-1.png",
     "contain", .50, .50, 1.0, "#ffffff"),
]

# Logos und Siegel: Transparenz bleibt erhalten, nichts wird beschnitten
MARKEN = [
    # Die Kopfleiste traegt die vom Kunden gelieferte Fassung unveraendert:
    # dunkle Schrift, roter Schmetterling, transparenter Grund. Die frueher
    # hier erzeugte helle Fassung ("hell") wird nicht mehr gebraucht.
    ("sms-logo.png",            "sms-header-logo.png",           "keep"),
    # Helle Fassung fuer den dunklen Bildkopf der Startseite - aus der
    # grossen dunklen Vorlage gerechnet, weil es sie nicht geliefert gibt.
    ("sms-logo-hell.png",       "sms-logo-gross.png",            "hell"),
    ("SchmidtMotorsport.png",   "SchmidtMotorsport-1536x157.png", "keep"),
    ("ZertLogo-9001-vektor.png", "ZertLogo-9001-vektor.png",      "keep"),
]

# Neue Bildplaetze, die es vorher nicht gab
NEU = [
    ("schmidt-motorsport-historie.jpg", "sms_schmidt-motorsport_1981.jpg", "cover", .50, .50, 1.0),
    # Gruppenfoto im Panoramaformat - "voll" heisst: nicht beschneiden, nur
    # auf eine vernuenftige Breite bringen. Ein Beschnitt wuerde Leute
    # abschneiden.
    ("leomax-team.jpg",             "Leomaxbild-final_1.jpg",        "voll", .50, .50, 1.0),
]

# Parallax-Hintergruende, 3:2 - liegen unter 74-88 % dunklem Overlay
HINTERGRUND = {
    "home":             ("Fraese-gross-01.png",             .50, .52, 1.0),
    "aktuelles":        ("fertigung_banner.jpg",            .50, .50, 1.0),
    "unternehmen":      ("classic.jpg",                     .50, .50, 1.0),
    "ueber-uns":        ("Fraese-gross-01.png",             .50, .52, 1.0),
    "historie":         ("sms_schmidt-motorsport_1983.jpg", .50, .50, 1.0),
    "engineering":      ("engineering.jpg",                 .50, .50, 1.0),
    "e-mobilitaet":     ("emobility.jpg",                   .50, .50, 1.0),
    "konstruktion":     ("Drehen-03.png",                   .50, .50, 1.0),
    "lehren":           ("messmittel_banner.jpg",           .50, .50, 1.0),
    "sicherheitszellen": ("sicherheitszellen_banner.jpg",   .50, .50, 1.0),
    "fertigung":        ("Fraese-gross-01.png",             .40, .50, 0.80),
    "messen":           ("Fertigteil.jpg",                  .50, .50, 1.0),
    # gleiches Motiv wie die Unterseite sms revo SL
    "elektro-kart":     ("E-Kart-sms-engineering.jpg",      .50, .52, 1.0),
    "revo-sl":          ("E-Kart-sms-engineering.jpg",      .50, .52, 1.0),
    "revo-x":           ("Kart-Aufnahme.jpg",               .50, .50, 1.0),
    "spacedrive":       ("20210813_DMSB_EKart-0258_50.jpg", .50, .50, 1.0),
    "bestellformulare": ("Blechbearbeitung-neu.png",        .50, .50, 1.0),
    "dokumente":        ("Pressen-01-ohne-orange.png",      .50, .50, 1.0),
    "impressum":        ("service_banner.jpg",              .50, .50, 1.0),
    "cta":              ("Schweissen-01.png",               .55, .48, 1.0),
}
