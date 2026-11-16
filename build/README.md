# Bauskripte

Erzeugen diese Website neu aus dem Claude-Design-Export. Reihenfolge:

```bash
python3 build_part2.py "<pfad>/SMS Engineering Website.dc.html" \
        "<pfad>/_ds/kastel-industrial-design-system-…" ../  ../assets/jarallax.min.js
python3 make_art.py imagespec.json ../assets/img   # Bilder zeichnen
python3 postprocess.py .. "<pfad>/SMS Engineering Website.dc.html"
node check.js            # Prüflauf, braucht einen Server auf Port 8971
```

* `build_part1.py` — Seitenliste, Komponenten des Design-Systems als HTML,
  die eigentliche Transformation samt Fehlerkorrekturen
* `build_part2.py` — Kopf-/Fußbereich, CSS, JS, schreibt die Seiten
* `make_art.py` — zeichnet alle Bilder als Vektorgrafik und legt fest,
  welches Motiv in welche Datei kommt (Tabelle `CONTENT`, Hintergründe
  `BG_KIND`)
* `art/kart.py` — das Kart selbst, in Millimetern am echten Fahrzeug
* `art/base.py` — Papier, Raster, Bemaßung, Führungslinien, Pylone, Helm
* `art/scenes.py` — die einzelnen Motive
* `art/bg.py` — die dunklen Parallax-Hintergründe
* `make_images.py` — die alten grauen Platzhalter; liefert nur noch die
  Flächen für Logos und Zertifikat
* `postprocess.py` — Platzhalter-PDFs, Beitragsseiten, tote Links umschreiben
* `check.js` — Playwright-Prüfung: Konsolenfehler, tote Links, Umbruchpunkte,
  Parallax, Mobilmenü
* `hygiene.py` — trägt `width`/`height` an jedes Bild nach und korrigiert
  Überschriftenstufen; mehrfach ausführbar
* `sektionen.py` — setzt `data-sec`/`data-tone` an die Sektionen und
  entscheidet, wo der Parallax unterbrochen wird (braucht
  `sektionshoehen.json`, erzeugt aus einem Playwright-Lauf)
* `kontaktseite.py` — erzeugt `kontakt.html` samt Themenliste
* `bildauswahl.py` — entfernt Bilder ohne geliefertes Foto und begrenzt die
  Kart-Unterseiten auf höchstens drei
* `kopfbereich.py` — macht aus dem Kopfbereich einen reinen Bildkopf
* `kontrast.js` + `kontrast.py` — messen den WCAG-Kontrast der
  Kopfbereich-Texte gegen das tatsächlich gerenderte Bild
* `audit.js` — misst Symmetrie, vertikalen Rhythmus, Containerbreiten,
  Überschriftenhierarchie, doppelte IDs, fehlende Bildmaße und Überläufe
* `check-nav.js` — prüft, dass Menüklicks oben auf der Zielseite landen und
  der Zurück-Knopf seine Position behält
* `check-motion.js` — zweiter Prüflauf nur für die Bewegung: scrollt jede
  Seite einmal komplett durch und prüft, dass danach nichts unsichtbar
  geblieben ist, dazu Mobilmenü, Kopfleiste und reduzierte Bewegung

`assets/motion.css` und `assets/motion.js` werden nicht erzeugt, sondern
liegen fest im Ordner `assets/`; `build_part2.py` bindet sie nur in Kopf- und
Fußbereich ein.

`check.js` legt seine Screenshots in `$SHOTS` ab (Vorgabe: das
Temp-Verzeichnis), damit der Website-Ordner sauber bleibt.
