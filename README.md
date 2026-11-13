# sms engineering — Website

Statische Website, gebaut aus dem Claude-Design-Export
`SMS Engineering Website.dc.html` (Design-System „Kastel Industrial").
Stand 04.11.2026.

## Starten

Einfach `index.html` im Browser öffnen. Für die korrekte Anzeige der
Schriften und der Parallax-Hintergründe besser über einen lokalen Server:

```bash
cd sms-website
python3 -m http.server 8000
# http://localhost:8000
```

## Inhalt

| | |
|---|---|
| 18 Inhaltsseiten | Start, Aktuelles, Unternehmen, Über uns, Historie, Engineering, E-Mobilität, Konstruktion, Lehren- und Messmittelbau, Sicherheitszellen, Fertigung, Messen und Prüfen, Elektro-Kart, revo SL, revo X, SpaceDrive, Bestellformular, Dokumente |
| 6 Beitragsseiten | `beitrag-*.html`, Platzhalter für die Blogbeiträge |
| 2 Rechtsseiten | Impressum, Datenschutz — beide als Platzhalter |
| `assets/` | CSS, JS, selbst gehostete Archivo-Schrift, Platzhalterbilder |
| `downloads/` | 13 Platzhalter-PDFs |

## Was aus dem Design übernommen ist

Alle Farben, Abstände, Schriftgrößen und Typo-Klassen stammen unverändert aus
dem Design-System (`assets/tokens.css`). Die sieben verwendeten Komponenten —
Button, TextLinkCta, SpecCell, ModelCard, FeaturePhotoCard, CtaBandPhoto,
AccentStripe — sind aus dem React-Bundle als normales CSS nachgebaut
(`assets/site.css`, Abschnitt „Komponenten des Design-Systems").

## Behobene Fehler

1. **Alle Bilder waren tot.** Sämtliche 43 Bilder lagen auf `sms.gmbh`; der
   Host antwortet nicht mehr. Ersetzt durch Platzhalter im Stil des
   Design-Systems, Dateinamen wie im Original.
2. **13 PDF-Links und 6 Beitragslinks waren tot.** Jetzt lokale Platzhalter
   unter `downloads/` bzw. eigene Beitragsseiten.
3. **`max-width` doppelt im selben `style`-Attribut** (Aktuelles,
   E-Mobilität, Dokumente). Die zweite Angabe überschrieb die erste, der
   Inhalt wurde mittig statt linksbündig gesetzt.
4. **Telefonnummer im `tel:`-Link hatte eine Null zu viel** —
   `+4991039184900` statt `+499103918490`, an zwei Stellen.
5. **Untermenüs waren nur mit der Maus erreichbar.** Jetzt zusätzlich per
   Tastatur über `:focus-within`.
6. **Kein `lang`, kein `<title>`, keine Beschreibung.** Jede Seite hat jetzt
   `lang="de"`, einen eigenen Titel, eine Meta-Beschreibung und Open-Graph-Angaben.
7. **`allowFullScreen="{{ true }}"`** im YouTube-Einbau war DSL-Syntax und
   wäre als Attribut im Browser gelandet. Korrigiert, zusätzlich
   `youtube-nocookie.com` und `loading="lazy"`.
8. **Archivo kam von Google Fonts.** Jetzt selbst gehostet unter
   `assets/fonts/` — eine Abhängigkeit weniger und ein Datenschutzthema weniger.
9. **Kein Sprung-Link, keine sichtbaren Fokus-Rahmen, kein aktiver
   Navigationszustand.** Ergänzt.
10. **Mobilmenü ließ den Seiteninhalt mitscrollen** und blieb beim Wechsel auf
    Desktopbreite offen. Jetzt Scroll-Sperre, Schließen per Esc und beim Resize.
11. **Favicon fehlte** — führte zu 404 im Log.
12. **Bilder ohne `width`/`height`.** 62 Stück. Ohne diese Angaben kennt
    der Browser das Seitenverhältnis erst, wenn das Bild geladen ist, und
    das Layout springt nach (CLS). `build/hygiene.py` trägt die echten
    Maße nach.
13. **Überschriftensprünge von h1 auf h3** auf sechs Seiten: Kartentitel
    waren h3, ohne dass eine h2 davor stand. Für Screenreader ist die
    Gliederung damit kaputt. Ebenfalls in `build/hygiene.py`.
14. **Textspalte sprang in der Unterbrechungs-Sektion** 173 px nach außen.
15. **Bilder richteten sich nach ihrer Pixelhöhe statt nach dem
    Seitenverhältnis.** Selbst verursacht: mit `width`/`height` am `<img>`
    gilt die Pixelhöhe als Vorgabe und `aspect-ratio` wird wirkungslos. In
    einer Reihe waren die Bilder dadurch unterschiedlich hoch — bis zu
    1 085 px statt 210 px. Ein `height: auto` im Stylesheet behebt es; die
    Attribute bleiben, denn sie verhindern den Layoutsprung.
16. **Formularmeldungen wären unsichtbar geblieben.** Die Einblend-Animation
    setzt `opacity: 0`, bis ein Element ins Bild scrollt. Fehlermeldungen
    sind beim Laden ausgeblendet, werden vom Beobachter nie gemeldet und
    wären damit dauerhaft unsichtbar gewesen. Formularteile und Elemente
    ohne Fläche sind jetzt von der Animation ausgenommen.
17. **Parallax-Hintergrund über CSS-Variable** löste den Bildpfad relativ zur
    CSS-Datei auf (`assets/assets/…`). Jetzt direkt am Element.

## Parallax

Jede Seite hat ein eigenes Hintergrundbild im Kopfbereich
(`assets/img/bg/<seite>.jpg`), dazu die Anfrage-Sektion auf der Startseite.
Umgesetzt mit `background-attachment: fixed` plus abgestuftem Overlay — kein
JavaScript nötig.

Zwei Sonderfälle sind berücksichtigt:

* **iOS** rendert `background-attachment: fixed` nicht als Parallax. Dort
  übernimmt jarallax (`assets/jarallax.min.js`, MIT), gesteuert von
  `assets/site.js`. Alle anderen Browser bleiben bei reinem CSS.
* **`prefers-reduced-motion`** schaltet den Effekt ab.

## Bilder

Die Seite zeigt **echte Fotos aus dem Haus**. Sie stammen aus dem Ordner
`sms gmbh bilder` und sind mit `build/einsetzen.py` eingesetzt worden; welches
Foto auf welchen Platz kommt, steht in `build/zuordnung.py`.

```bash
python3 -I build/einsetzen.py <quellordner> .
```

**Wie verarbeitet wird**

* **Nie hochgerechnet.** Ist eine Quelle kleiner als der Bildplatz, wird sie
  in ihrer eigenen Auflösung ausgegeben. Lieber ein kleineres Bild als ein
  weiches.
* **Alle Metadaten fallen weg.** Drei der Originale trugen GPS-Koordinaten im
  EXIF — die haben auf einer Website nichts verloren.
* **Zuschnitt** auf 16:10 für Inhaltsbilder, 3:2 für die Hintergründe, mit
  einem Fokuspunkt je Bild, damit nicht blind mittig geschnitten wird.
* **Fotos werden JPEG** (Qualität 80, progressiv), **Logos bleiben PNG** mit
  Transparenz. Die Hintergründe liegen unter 74–88 % dunklem Overlay und
  kommen deshalb mit Qualität 62 aus — sichtbar ist davon nichts.
* Dateien, deren Endung sich dadurch ändert (`.png` → `.jpg`), werden in allen
  Seiten mit umgeschrieben; die alten Zeichnungen sind gelöscht.

**Zwei Dinge, die dabei auffielen und mit geändert wurden**

1. Das **Logo** im Kopfbereich saß auf einer dunklen Plakette — das echte
   Logo ist dunkel auf hell und wäre darauf unsichtbar gewesen. Die Plakette
   ist jetzt weiß. Außerdem erzwangen die alten `width`/`height`-Angaben ein
   Seitenverhältnis von 5:1; das Logo hat 2,254:1 und wäre gestaucht worden.
2. Die Karte **„Schmidt Motorsport Historie"** zeigte das Firmenlogo in einem
   16:10-Rahmen mit `object-fit: cover` — beschnitten unbrauchbar. Dort steht
   jetzt ein Rallyefoto von 1981, das Logo nur noch auf der Historienseite.

**Was noch keine Fotos hat** und weiter als Zeichnung läuft: alles zum
**sms revo X** (4 Plätze), die sechs Bilder zu **United in Dreams** auf der
SpaceDrive-Seite, zwei weitere Kart-Motive auf der revo-SL-Seite und das
Batterie-Leasing. Dafür lagen keine passenden Aufnahmen bei — Fotos
nachzureichen ist der letzte Schritt.

### Eingesetzte Dateien

| Bildplatz | Quelle | Ausgabe |
|---|---|---|
| `E-Kart-sms-engineering-2-1024x683.jpg` | E-Kart-sms-engineering.jpg | 1600x1000 |
| `Elektro-Slalom-Kart-Bad-Aibling.jpg` | Kart-Aufnahme.jpg | 604x377 |
| `Elektro-Slalom-Kart.jpg` | E-Kart-sms-engineering.jpg | 1600x1000 |
| `Freigestellt-01-GUT-e1786614143161.jpg` | Freigestellt-01-GUT.png | 1600x1000 |
| `IMG_2384-scaled.jpg` | E-Kart-sms-engineering.jpg | 1600x1000 |
| `Inklusives-Kart-1024x683.jpg` | 20210813_DMSB_EKart-0258_50.jpg | 897x560 |
| `Neue-Maschine-DMF-200-8-1-320x202.jpg` | Fraese-gross-02.png | 1600x1000 |
| `SchmidtMotorsport.png` | SchmidtMotorsport-1536x157.png | 1200x123 |
| `Universal-Antriebsstrang-sms-engineering-320x202.jpg` | emobility.jpg | 1344x840 |
| `ZertLogo-9001-vektor.png` | ZertLogo-9001-vektor.png | 173x173 |
| `bg/aktuelles.jpg` | fertigung_banner.jpg | 960x640 |
| `bg/bestellformulare.jpg` | Blechbearbeitung-neu.png | 1920x1280 |
| `bg/cta.jpg` | Schweissen-01.png | 1920x1280 |
| `bg/dokumente.jpg` | Pressen-01-ohne-orange.png | 1920x1280 |
| `bg/e-mobilitaet.jpg` | emobility.jpg | 1920x1280 |
| `bg/elektro-kart.jpg` | Hintergrund-leomax-01.png | 1665x1110 |
| `bg/engineering.jpg` | engineering.jpg | 1920x1280 |
| `bg/fertigung.jpg` | Fraese-gross-01.png | 1920x1280 |
| `bg/historie.jpg` | sms_schmidt-motorsport_1983.jpg | 1920x1280 |
| `bg/home.jpg` | Landing-Page-Bild-neu.png | 1920x1280 |
| `bg/impressum.jpg` | service_banner.jpg | 960x640 |
| `bg/konstruktion.jpg` | Drehen-03.png | 1920x1280 |
| `bg/lehren.jpg` | messmittel_banner.jpg | 960x640 |
| `bg/messen.jpg` | Fertigteil.jpg | 1920x1280 |
| `bg/revo-sl.jpg` | E-Kart-sms-engineering.jpg | 1920x1280 |
| `bg/revo-x.jpg` | Kart-Aufnahme.jpg | 720x480 |
| `bg/sicherheitszellen.jpg` | sicherheitszellen_banner.jpg | 960x640 |
| `bg/spacedrive.jpg` | 20210813_DMSB_EKart-0258_50.jpg | 1122x748 |
| `bg/ueber-uns.jpg` | Fraese-gross-01.png | 1920x1280 |
| `bg/unternehmen.jpg` | classic.jpg | 1920x1280 |
| `engineering.jpg` | Fertigteil.jpg | 1600x1000 |
| `leomax-firmenstruktur_Zeichenflaeche-1.jpg` | leomax-firmenstruktur_Zeichenflaeche-1.png | 1600x605 |
| `revo-SL-@Bundesendlauf-320x202.jpg` | 20210813_DMSB_EKart-0258_50.jpg | 1122x701 |
| `revo-SL-@DKSM-Finale-320x202.jpg` | revo-SL-@DKSM-Finale.png | 900x562 |
| `schmidt-motorsport-historie.jpg` | sms_schmidt-motorsport_1981.jpg | 1600x1000 |
| `sms-e-Kart-Training-1024x683.jpg` | Hintergrund-leomax-01.png | 1600x1000 |
| `sms-logo.png` | sms-logo-gross.png | 1200x873 |
| `sms-revo-SL-Hockenheimring-11-scaled.jpg` | Hintergrund-leomax-01.png | 1206x754 |
| `sms-revo-SL-Hockenheimring-13-scaled-e1666783706334.jpg` | revo-SL-@DKSM-Finale.png | 738x461 |
| `sms_emobilitaet.jpg` | emobility.jpg | 1600x1000 |
| `sms_fertigung_montage_01.jpg` | Schweissen-01.png | 1600x1000 |
| `sms_konstruktion_entwicklung_01.jpg` | engineering.jpg | 1600x1000 |
| `sms_konstruktion_entwicklung_02.jpg` | Drehen-03.png | 1600x1000 |
| `sms_konstruktion_entwicklung_03.jpg` | Blechbearbeitung-neu.png | 1600x1000 |
| `sms_lehren-messmittelbau_01.jpg` | messmittel_banner.jpg | 1024x640 |
| `sms_lehren-messmittelbau_02.jpg` | Blechbearbeitung-neu.png | 1600x1000 |
| `sms_lehren-messmittelbau_03.jpg` | Pressen-01-ohne-orange.png | 1600x1000 |
| `sms_stuetzgestelle.jpg` | Rohrbiegen-neu.png | 1600x1000 |
| `sms_stuetzgestelle_02.jpg` | sicherheitszellen_banner.jpg | 1024x640 |
| `sms_stuetzgestelle_03.jpg` | rastaurierung_banner.jpg | 1024x640 |
| `smsengineering_Website_Bild_Vertriebspartnerschaft_Beule.jpg` | Kart-Aufnahme.jpg | 720x450 |

> **Achtung beim Neubauen:** `build/make_art.py` erzeugt die alten
> Zeichnungen und würde die Fotos überschreiben. Nach einem Lauf von
> `make_art.py` immer `build/einsetzen.py` hinterher laufen lassen.

## Was noch Platzhalter ist

* **13 PDFs** in `downloads/`.
* **6 Beitragstexte** — im Design standen nur die Anrisstexte.
* **Impressum und Datenschutz.** Beides muss juristisch geprüft werden; die
  Datenschutzseite listet die Punkte auf, die diese Seite tatsächlich betreffen.

## Farben

Das Theme führt Rot statt Blau (Stand 04.11.2026). Die Umstellung sitzt in
einem eigenen Block am Ende von `assets/tokens.css`; die Originalwerte des
Design-Systems stehen unverändert darüber, damit nachvollziehbar bleibt, was
getauscht wurde.

| Variable | vorher (blau) | jetzt (rot) |
|---|---|---|
| `--primary` | `#1c69d4` | `#cf1f14` |
| `--primary-active` | `#0653b6` | `#a3140c` |
| `--accent-blue-light` | `#0066b1` | `#f0432f` |
| `--accent-blue-dark` | `#1c69d4` | `#e22718` |

Die Variablennamen `--accent-blue-*` bleiben bestehen, weil sie an mehreren
Stellen im Design-System referenziert werden — sie führen jetzt Rottöne.

Kontrast nach WCAG, jeweils gegen den blauen Ausgangswert gemessen:
`--primary` auf Weiß 5,44:1 (vorher 5,22:1), auf `--surface-soft` 5,08:1
(vorher 4,88:1), `--primary-active` auf Weiß 7,89:1 (vorher 7,19:1). Alle
Werte liegen über 4,5:1, die Umstellung verschlechtert die Lesbarkeit also
an keiner Stelle.

Mit umgestellt: der Markenstreifen der Platzhalterbilder
(`build/make_images.py`), der Balken in den Platzhalter-PDFs
(`build/postprocess.py`) und das Favicon (`assets/favicon.svg`).

## Bewegung

Zwei zusätzliche Dateien, `assets/motion.css` und `assets/motion.js`, bringen
Animation und Parallax. Sie hängen an der Klasse `js-motion`, die das Skript
selbst an `<html>` setzt: ohne JavaScript ist die Seite vollständig sichtbar
und ruhig, nichts bleibt versteckt.

**Animiert wird**

* **Einblenden beim Scrollen** — Überschriften, Absätze, Karten, Bilder und
  Listen fahren 16 px hoch und blenden ein, 0,62 s, gestaffelt um 70 ms
  innerhalb einer Gruppe. Einmalig, danach meldet sich der Beobachter ab.
* **Die große Überschrift** jeder Seite wird über `clip-path` von unten
  aufgedeckt.
* **Kopfleiste** — schrumpft von 76 auf 64 px, bekommt einen Schatten und
  fährt beim Runterscrollen weg; beim Hochscrollen ist sie sofort wieder da.
  Bei offenem Mobilmenü bleibt sie stehen.
* **Lesefortschritt** als 2 px dünne rote Linie an der Unterkante der Leiste.
* **Zahlen** in den Kennzahlfeldern zählen hoch, wenn sie ins Bild kommen —
  mit deutscher Tausendertrennung, Zusätze wie „+" bleiben erhalten.
* **Kleinteile** — Karten zoomen ihr Bild beim Überfahren, Textlinks
  bekommen eine Unterlinie, die von links einläuft, und ihr Winkel wandert
  nach rechts, Buttons heben sich 2 px an, der Burger wird beim Öffnen
  zum Kreuz, Navigationspunkte bekommen eine rote Unterlinie.

**Parallax** liegt an fünf Stellen, nicht überall:

1. Das **Hintergrundbild** jeder Seite im Kopfbereich (`background-attachment:
   fixed`, auf iOS jarallax) — wie bisher.
2. Der **Inhalt des Kopfbereichs** läuft der Seite um bis zu 80 px nach und
   blendet beim Verlassen aus.
3. **Kartenbilder** wandern um ±18 px im eigenen, beschnittenen Rahmen.
4. **Großbilder** außerhalb der Karten bewegen sich um ±14 px.
5. Der **Inhalt des Anfrage-Bands** um ±26 px.

**Technik.** Bewegt werden ausschließlich `transform`, `scale`, `opacity` und
`clip-path` — alles im Compositor, kein Layout. Ein einziger
`requestAnimationFrame`-Takt, ein passiver Scroll-Listener, und gerechnet wird
nur für Elemente, die ein `IntersectionObserver` gerade als sichtbar meldet.

**`prefers-reduced-motion: reduce`** schaltet alles ab: Das Skript steigt nach
dem Setzen der Klasse aus, es wird kein Element versteckt, kein Parallax
berechnet, die Kopfleiste bleibt stehen.

Geprüft mit `build/check-motion.js`: alle 26 Seiten einmal komplett
durchgescrollt, danach darf kein animiertes Element unsichtbar geblieben sein;
dazu Mobilmenü, Burger-Kreuz, Kopfleisten-Verhalten und der Durchlauf mit
reduzierter Bewegung.

## Menuelinks fuehren an den Seitenanfang

Ein Klick auf einen Seitenlink im Kopf-, Mobil- oder Fußmenü landet immer
oben auf der Zielseite. Zwei Fälle löst der Browser von sich aus nicht so,
wie man es erwartet, und nur die fängt `assets/site.js` ab:

* **Klick auf die Seite, auf der man schon steht.** Der Browser tut dann
  nichts. Jetzt wird die Seite nicht neu geladen, sondern weich nach oben
  gescrollt; das Mobilmenü schließt sich dabei und der Fokus wandert auf den
  Hauptinhalt.
* **Wiederhergestellte Scrollposition.** Beim Verlassen setzt das Skript eine
  Marke in `sessionStorage`; auf der nächsten Seite wird nach dem `pageshow`
  einmal nach oben gesprungen und die Marke gelöscht. `pageshow` deckt auch
  den Vor-/Zurück-Cache ab.

Unberührt bleiben: der **Zurück-Knopf** (behält seine Scrollposition, das ist
so gewollt), Links im Seiteninhalt, Sprungmarken mit `#`, externe Ziele,
`mailto:` und `tel:`, Klicks mit gedrückter Strg-, Befehls-, Umschalt- oder
Alt-Taste und Links mit `target`. Ohne `sessionStorage` — etwa im privaten
Modus — fällt die Funktion still auf das normale Browserverhalten zurück.

Geprüft mit `build/check-nav.js`.

## Bildkopf

Jede Seite öffnet mit einem großen Bildkopf: ein Foto über die volle Breite,
am Fuß eine 3 px dünne rote Kante als Naht zum Inhalt. Darunter folgt der
Inhalt auf ruhigen hellen Flächen — **Bildhintergrund gibt es nur hier**,
nicht über die ganze Seite.

**Der Abstand zur Überschrift ist auf allen 27 Seiten gleich: 321 px** unter
der Kopfleiste (gemessen bei 1440 px Fensterbreite; bei 900 px sind es 213 px).
Vorher war es umgekehrt: Der Bildkopf hatte eine feste Höhe und der Text war
unten angeschlagen — damit hing die Lage der Überschrift an der Textlänge und
sprang von Seite zu Seite um bis zu **400 px** (148 px auf der Startseite,
543 px auf den Beitragsseiten). Jetzt steht die Polsterung oben fest
(`clamp(140px, 20vw, 300px)`), der Inhalt beginnt dort, und die Höhe des
Bildkopfs ergibt sich aus dem Text. Unter dem Textblock bleiben dadurch immer
dieselben 80 px bis zur roten Kante. Die Mindesthöhe
(`clamp(360px, 44vh, 520px)`) greift nur noch auf sehr kurzen Seiten.

Zwei Kleinigkeiten mussten dafür mit: Die Polsterung stand bisher im
`style`-Attribut jeder einzelnen Seite und war aus dem Stylesheet gar nicht
erreichbar — ein Inline-Stil gewinnt immer. `build/kopfabstand.py` holt sie
heraus, seitdem steht sie an einer Stelle. Und die Startseite hatte als
einzige 20 px Abstand zwischen Kennzeile und Überschrift statt 16 px; das
allein waren 4 px Unterschied.

**Was dafür weichen musste.** Im Design hatte der Kopfbereich zwei Spalten:
Text links, ein zweites Foto rechts — und dahinter lief noch ein drittes Bild
als Hintergrund. Drei Bilder auf einmal sind unruhig. Jetzt trägt ein Bild den
Kopf. Die 8 entfernten Zweitfotos kommen auf allen Seiten, wo sie inhaltlich
zählen, weiter unten ohnehin noch einmal vor. Erledigt von
`build/kopfbereich.py`.

**Der Verlauf über dem Bild** besteht aus zwei Teilen: einer von unten, damit
der Text auf dunklem Grund steht, einer von links, damit die Textspalte auch
bei hellen Motiven trägt. Oben bleibt das Bild weitgehend frei.

**Kontrast gemessen, nicht geschätzt.** `build/kontrast.js` fotografiert jeden
Kopfbereich mit unsichtbar geschaltetem Text, `build/kontrast.py` mittelt die
Helligkeit genau unter jedem Textrechteck und rechnet den WCAG-Kontrast gegen
die echte Textfarbe. Der erste Durchlauf fand eine Stelle unter dem Grenzwert
— die kleine Zeile über der Überschrift auf der Startseite mit 3,98:1 statt
4,5:1. Sie steht jetzt auf Weiß statt Grau. Zweiter Durchlauf: alles sauber.

**Die Startseite führt mit dem Kart**, nicht mit der Maschinenhalle — das
eKart ist das Aushängeschild, und die Halle steht ohnehin auf der
Fertigungsseite.

Die Flächenfarbe der Sektionen liegt seit dem Umbau in `data-tone` statt als
Inline-Stil im Markup, gesetzt von `build/sektionen.py`. Das bleibt so: die
Farbe ist damit an einer Stelle im Stylesheet steuerbar statt über 26 Dateien
verteilt.

## Kontaktformular

`kontakt.html` ersetzt das frühere „Ticketsystem", das in Wahrheit nur ein
`mailto:`-Link war. Die Seite entsteht aus `build/kontaktseite.py` und hat
**14 Themen** zur Auswahl — von Engineering über die drei Kart-Modelle bis
Bewerbung und Presse.

* **Pflichtfelder** Thema, Name, E-Mail, Nachricht und die
  Datenschutz-Zustimmung. Geprüft wird beim Verlassen des Feldes und beim
  Absenden, mit deutschen Meldungen, `aria-invalid`, `aria-describedby` und
  Sprung auf das erste beanstandete Feld.
* **Thema vorbelegen** über die Adresszeile: `kontakt.html?thema=support`.
  Genau so verlinkt die Dokumenten-Seite ihre technischen Rückfragen.
* **Zielabhängige Adresse:** Support und Ersatzteile gehen an
  `revo@sms.gmbh`, alles andere an `info@sms.gmbh`.
* **Honigtopf-Feld** gegen Formular-Roboter, für Menschen unsichtbar und
  nicht per Tabulator erreichbar.
* **Kein Server nötig:** Beim Absenden entsteht eine fertig ausgefüllte
  E-Mail. Soll das Formular später über einen Dienst oder über WordPress
  laufen, genügt `action` und `method` am `<form>` — `assets/form.js` hält
  sich dann heraus und der Browser sendet normal ab.

Der Kontakt-Knopf in der Kopfleiste, der Eintrag im Mobilmenü und ein neuer
Link im Fußbereich zeigen jetzt auf diese Seite statt auf einen
`mailto:`-Link.

## Das Logo in der Kopfleiste

Die Kopfleiste trägt das vom Kunden gelieferte Logo (`sms-header-logo.png`,
325 × 136 px, dunkle Schrift, roter Schmetterling, transparenter Grund)
unverändert — **ohne Plakette**, direkt auf der weißen Leiste. Anzeigehöhe
48 px, unter 480 px Fensterbreite 38 px.

Davor standen zwei verworfene Zwischenschritte: erst das dunkle Logo auf
weißer Plakette (zu klein, kaum zu erkennen), dann eine helle Fassung auf
schwarzer Plakette. Für die zweite musste die helle Fassung erst aus der
großen dunklen Vorlage gerechnet werden, weil es sie in hoher Auflösung nicht
gab. Der Weg ist als Modus `hell` in `build/einsetzen.py` erhalten, wird aber
nicht mehr verwendet — die Zuordnung in `build/zuordnung.py` zeigt jetzt auf
die gelieferte Kopfleisten-Fassung mit Modus `keep`.

## Shop statt Aktuelles

Die Seite „Aktuelles" und die sechs Beitragsseiten sind entfernt, mitsamt dem
Aktuelles-Abschnitt auf der Startseite und dem Beitragsverweis auf der
Fertigungsseite. An die erste Stelle des Kopfmenüs ist ein **Shop-Knopf**
gerückt: `https://shop.sms.gmbh`, neuer Tab, `rel="noopener"`, im selben Stil
wie der Kontakt-Knopf (schwarz, beim Überfahren rot, Schrift bleibt weiß). Im
Mobilmenü steht er ganz oben, im Fußbereich als normaler Link an erster
Stelle unter „Links".

Zwei Dinge, die dabei mitlaufen mussten:

* Die Regel `.nav > a { color: … }` ist spezifischer als `.ds-btn--primary`
  und hätte dem Shop-Knopf — wie zuvor schon dem Kontakt-Knopf — die dunkle
  Textfarbe aufgezwungen. Er ist jetzt ebenfalls ausgenommen.
* Auf der Startseite stießen nach dem Entfernen zwei weiße Sektionen
  aneinander und wären optisch zu einem Block verschmolzen. Die zweite steht
  jetzt auf dem hellgrauen Ton; `build/shop-und-aktuelles.py` prüft das
  generell und ist mehrfach ausführbar.

`build/postprocess.py` erzeugte die Beitragsseiten aus `aktuelles.html`. Es
überspringt diesen Teil jetzt, wenn die Datei fehlt — die Platzhalter-PDFs
entstehen weiterhin.

## Der Kontakt-Knopf

Schwarz mit weißer Schrift, beim Überfahren fährt er über 0,3 s weich auf
Rot — die Schrift bleibt weiß. Gilt für die Kopfleiste und den Knopf im
Mobilmenü; die übrigen Knöpfe auf den Seiten bleiben rot.

Dabei kam ein Kontrastfehler mit heraus: Die Regel `.nav > a { color: ... }`
ist spezifischer als `.ds-btn--primary` und hat dem Knopf die dunkle
Textfarbe aufgezwungen. Dunkelgrau auf Rot kam auf **2,78:1** — deutlich
unter den geforderten 4,5:1 und auf jeder Seite sichtbar. Der Knopf ist
jetzt von dieser Regel ausgenommen: weiß auf Schwarz sind 16,24:1, weiß auf
Rot 5,44:1.

## Navigation: die aktive Seite

Der aktive Menüpunkt steht in Rot, halbfett und einen halben Punkt größer —
**ohne Linie**. Vorher lagen dort zwei rote Striche übereinander: einer aus
einem `box-shadow: inset` in `site.css`, einer aus der Unterlinie in
`motion.css`, die auch bei `aria-current` ausgefahren wurde. Die Unterlinie
erscheint jetzt nur noch beim Überfahren mit der Maus.

Auf einer Unterseite war bisher **gar nichts** markiert: `aria-current="page"`
sitzt dort auf dem Link im zugeklappten Untermenü, den niemand sieht. Jetzt
wird zusätzlich der sichtbare Elternpunkt hervorgehoben:

```css
.nav .nav-group:has([aria-current="page"]) .nav-group__top { … }
```

Im Mobilmenü ist die aktive Seite ebenfalls rot und halbfett; dort sind alle
Ebenen offen, eine Elternmarkierung braucht es nicht.

## Anfragen führen auf das Formular

Abschnitte, die zu einer Anfrage auffordern, zeigen nicht mehr auf einen
`mailto:`-Link mit der Adresse als Knopfbeschriftung, sondern direkt auf das
Kontaktformular — mit vorgewähltem Thema über `?thema=`:

| Seite | vorher | jetzt |
|---|---|---|
| `index.html` (Band „Ihr Projekt, unsere Werkstatt") | `mailto:info@sms.gmbh`, Knopftext = Adresse | `kontakt.html`, Knopftext „Anfrage senden" |
| `revo-x.html` („Schnuppertag anfragen") | `mailto:revo@sms.gmbh` | `kontakt.html?thema=revo-x` |
| `revo-sl.html` (Fließtext) | „Anfragen richten Sie an revo@sms.gmbh" | „über das Kontaktformular" → `?thema=revo-sl` |
| `bestellformulare.html` | `mailto:revo@sms.gmbh` | `kontakt.html?thema=angebot` |

Geprüft durch Anklicken im Browser: alle vier landen auf `kontakt.html`, das
Themenfeld steht jeweils schon richtig („Elektro-Kart — sms revo X",
„Elektro-Kart — sms revo SL", „Angebot oder Bestellung"), und die Seite
beginnt oben.

Adressen stehen weiterhin dort, wo man sie erwartet: im Fußbereich und im
Kasten „Direkt erreichen" neben dem Formular. Nur die Handlungsaufforderungen
wurden umgehängt. Das Skript dazu ist `build/anfragen.py` und mehrfach
ausführbar.

## Geprüft

Alle 20 Seiten in Chromium: HTTP 200, keine JavaScript-Fehler, keine
Konsolenfehler, genau ein `<h1>`, kein horizontales Überlaufen bei 390, 900,
1159, 1160 und 1440 px, 903 interne Verweise ohne einen einzigen toten Link,
kein fehlendes Bild. Umschaltpunkt der Navigation und Mobilmenü inklusive
Esc-Taste und Scroll-Sperre geprüft.

Einzige verbleibende Meldung: die YouTube-Einbettung auf der Seite
„Sicherheitszellen" lässt sich aus der Testumgebung nicht laden — dort ist
ausgehender Verkehr gesperrt. Im Browser funktioniert sie.
