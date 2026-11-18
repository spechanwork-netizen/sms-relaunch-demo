#!/usr/bin/env python3
"""Teil 2: Rahmen (Kopf/Fuss), CSS, JS und das Schreiben der Seiten."""
import os, re, json, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_part1 import (PAGES, SLUG2FILE, VAR, DESCR, MARKS, IMG_USED,
                         transform, nav_html, mobile_html)

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | sms engineering GmbH</title>
<meta name="description" content="{descr}">
<meta name="theme-color" content="#1a2129">
<meta property="og:title" content="{title} | sms engineering GmbH">
<meta property="og:description" content="{descr}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/motion.css">
</head>
<body>
<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>
<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="sms engineering GmbH, zur Startseite">
      <img src="assets/img/sms-logo.png" alt="sms engineering GmbH" width="115" height="48">
    </a>
    <nav class="nav" aria-label="Hauptnavigation">{nav}</nav>
    <button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="mobilmenue">
      <span class="burger__bars" aria-hidden="true"></span>
    </button>
  </div>
</header>
<div class="mnav" id="mobilmenue" hidden><a class="ds-btn ds-btn--primary mnav__cta mnav__shop" href="https://shop.sms.gmbh" target="_blank" rel="noopener">Shop</a>{mnav}</div>
<main id="inhalt">
"""

FOOT = """</main>
<div class="ds-stripe" role="presentation"></div>
<footer class="site-footer">
  <div class="site-footer__inner">
    <div class="site-footer__cols">
      <div class="fcol">
        <h2 class="t-title-sm">Adresse</h2>
        <p class="t-body-sm">sms engineering GmbH<br>Seckendorfer Straße 6<br>90556 Cadolzburg</p>
      </div>
      <div class="fcol">
        <h2 class="t-title-sm">Kontakt</h2>
        <a class="t-body-sm" href="tel:+499103918490">Tel: +49 9103 91849 0</a>
        <a class="t-body-sm" href="mailto:info@sms.gmbh">E-Mail: info@sms.gmbh</a>
      </div>
      <div class="fcol">
        <h2 class="t-title-sm">Bereiche</h2>
        <a class="t-body-sm" href="engineering.html">Engineering</a>
        <a class="t-body-sm" href="fertigung.html">Fertigung</a>
        <a class="t-body-sm" href="messen.html">Messen &amp; Prüfen</a>
        <a class="t-body-sm" href="elektro-kart.html">Elektro-Kart</a>
      </div>
      <div class="fcol">
        <h2 class="t-title-sm">Links</h2>
        <a class="t-body-sm" href="https://shop.sms.gmbh" target="_blank" rel="noopener">Shop</a>
        <a class="t-body-sm" href="impressum.html">Impressum</a>
        <a class="t-body-sm" href="datenschutz.html">Datenschutz</a>
        <a class="t-body-sm" href="dokumente.html">Wichtige Dokumente</a>
        <a class="t-body-sm" href="kontakt.html">Kontakt</a>
      </div>
      <div class="fcol">
        <h2 class="t-title-sm">Zertifizierung</h2>
        <img class="fcert" src="assets/img/ZertLogo-9001-vektor.png"
             alt="Zertifiziert nach DIN EN ISO 9001" width="120" height="120" loading="lazy">
      </div>
    </div>
    <div class="site-footer__bar">
      <span class="t-body-sm">© 2026 sms engineering GmbH</span>
      <div class="site-footer__social">
        <a class="t-label" href="https://www.facebook.com/sms.engineering/" rel="noopener">Facebook</a>
        <a class="t-label" href="https://www.instagram.com/schmidtmotorsport_sms/" rel="noopener">Instagram</a>
        <a class="t-label" href="https://www.linkedin.com/company/sms-engineering-gmbh/" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </div>
</footer>
<script src="assets/jarallax.min.js" defer></script>
<script src="assets/site.js" defer></script>
<script src="assets/motion.js" defer></script>
</body>
</html>
"""

FONTFACE = """/* ---- Archivo, selbst gehostet ----\n   Der Export laedt Archivo von Google Fonts. Fuer den Livebetrieb ist das\n   zwei Probleme auf einmal: eine Abhaengigkeit von einem fremden Server und\n   ein Datenschutzthema (IP-Uebertragung ohne Einwilligung). Die Dateien\n   liegen deshalb unter assets/fonts/ und werden lokal eingebunden. */\n@font-face{font-family:"Archivo";font-style:normal;font-weight:300;font-display:swap;src:url("fonts/archivo-latin-300-normal.woff2") format("woff2"),url("fonts/archivo-latin-300-normal.woff") format("woff");}\n@font-face{font-family:"Archivo";font-style:normal;font-weight:400;font-display:swap;src:url("fonts/archivo-latin-400-normal.woff2") format("woff2"),url("fonts/archivo-latin-400-normal.woff") format("woff");}\n@font-face{font-family:"Archivo";font-style:normal;font-weight:700;font-display:swap;src:url("fonts/archivo-latin-700-normal.woff2") format("woff2"),url("fonts/archivo-latin-700-normal.woff") format("woff");}\n:root{--font-core:"Archivo",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;--font-display:var(--font-core);--font-body:var(--font-core)}\n"""

THEME = """
/* ---- Theme: Blau -> Rot (04.11.2026) ----
   Die Tokennamen des Design-Systems bleiben unveraendert, damit nichts bricht,
   was sie referenziert - nur die Werte wechseln. Die Kontrastwerte liegen
   dabei ueberall gleichauf mit dem blauen Original oder darueber:
   primary auf Weiss 5,44:1 (vorher 5,22), auf --surface-soft 5,08:1
   (vorher 4,88), auf --surface-strong 4,56:1.
   --accent-blue-* heissen weiter so, fuehren jetzt aber Rottoene - umbenennen
   wuerde das Design-System-Bundle brechen. Sprechende Aliase darunter. */
:root{
--primary:#cf1f14;--primary-active:#a3140c;
--accent-red-light:#f0432f;--accent-red-mid:#e22718;--accent-red-dark:#a3140c;
--accent-blue-light:var(--accent-red-light);
--accent-blue-dark:var(--accent-red-mid);
--accent-red:var(--accent-red-dark)}
"""

SITE_CSS = """/* ==========================================================================
   sms engineering — Website
   Tokens und Typo-Utilities stammen unveraendert aus dem Design-System
   "Kastel Industrial". Darunter nur das, was der Prototyp im Design-Runtime
   geloest hat und was hier als echtes CSS gebraucht wird.
   ========================================================================== */
@import url("tokens.css");

/* --- Grundlagen ---------------------------------------------------------- */
body { margin: 0; background: var(--canvas); }

/* Flaechenfarbe der Sektionen. Stand frueher als Inline-Stil im Markup und
   liegt seit dem Umbau in data-tone - so ist sie aus dem Stylesheet
   steuerbar, statt in 26 Dateien verteilt zu sein. */
main > section[data-tone="soft"]   { background: var(--surface-soft); }
main > section[data-tone="strong"] { background: var(--surface-strong); }
a { color: var(--primary); text-decoration: none; }
/* height:auto ist Pflicht, sobald die Bilder width/height-Attribute haben:
   sonst gilt die Pixelhoehe aus dem Attribut und aspect-ratio wird
   wirkungslos - die Bilder einer Reihe werden dann unterschiedlich hoch. */
img { max-width: 100%; height: auto; }
h1, h2, h3, h4, p, ul { margin: 0; }

.skip-link {
  position: absolute; left: -9999px; top: 0; z-index: 200;
  background: var(--primary); color: var(--on-primary);
  padding: 12px 20px; font-family: var(--font-display); font-weight: 700;
}
.skip-link:focus { left: 0; }
:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }

/* --- Kopfbereich --------------------------------------------------------- */
.site-header {
  position: sticky; top: 0; z-index: 60;
  background: var(--canvas); border-bottom: 1px solid var(--hairline);
}
.site-header__inner {
  max-width: var(--container-max); margin: 0 auto;
  padding: 0 clamp(16px, 3vw, 32px); min-height: 76px;
  display: flex; align-items: center; gap: clamp(16px, 2vw, 40px);
}
/* Keine Plakette mehr: das Logo ist die dunkle Fassung auf transparentem
   Grund und sitzt direkt auf der weissen Kopfleiste. */
.brand {
  display: flex; align-items: center; background: transparent;
  padding: 8px 0; flex: none;
}
.brand img { height: 48px; width: auto; display: block; }
@media (max-width: 480px) { .brand img { height: 38px; } }

.nav { display: flex; align-items: center; gap: clamp(14px, 1.8vw, 30px); margin-left: auto; }
/* Der Kontakt-Knopf ist hier ausgenommen: .nav > a ist spezifischer als
   .ds-btn--primary und hat ihm die dunkle Textfarbe aufgezwungen - dunkel
   auf Rot kam auf 2,5:1 und war nicht lesbar. */
.nav > a:not(.nav-contact):not(.nav-shop), .nav__top { color: var(--ink); }
.hv-primary:hover, .hv-primary:focus-visible { color: var(--primary); }
.hv-primary-soft:hover, .hv-primary-soft:focus-visible { color: var(--primary); background: var(--surface-soft); }
.hv-contact:hover, .hv-contact:focus-visible { background: var(--primary-active); color: var(--on-primary); }
/* Aktive Seite in der Navigation: etwas kraeftiger und einen halben Punkt
   groesser - keine Linie. Vorher lagen hier zwei rote Striche uebereinander,
   einer aus diesem inset-Schatten und einer aus der Unterlinie in
   motion.css, die auch bei aria-current ausgefahren wurde. */
.nav [aria-current="page"],
.nav .nav-group:has([aria-current="page"]) .nav-group__top {
  color: var(--primary); font-weight: 600;
  font-size: calc(var(--nav-link-size) + 0.5px);
}

.nav-group { position: relative; display: flex; align-items: center; height: 76px; }
.nav-group__top { color: var(--ink); display: inline-flex; align-items: center; gap: 6px; }
.nav-group__chev { font-size: 15px; transform: rotate(90deg); display: inline-block; }
.nav-drop {
  position: absolute; top: 76px; left: -16px; min-width: 300px;
  background: var(--canvas); border: 1px solid var(--hairline);
  border-top: var(--border-selected-width) solid var(--primary);
  padding: 8px 0; display: flex; flex-direction: column;
  opacity: 0; visibility: hidden; transform: translateY(-4px);
  transition: opacity .14s ease, transform .14s ease, visibility .14s;
}
.nav-group:last-of-type .nav-drop { left: auto; right: -16px; }
/* Tastatur UND Maus - der Prototyp konnte nur Maus */
.nav-group:hover .nav-drop,
.nav-group:focus-within .nav-drop { opacity: 1; visibility: visible; transform: none; }
.nav-drop a { color: var(--ink); padding: 10px 20px; }
.nav-contact { height: auto; padding: 14px 22px; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase; }

/* Kontakt-Knopf: schwarz mit weisser Schrift, faehrt beim Ueberfahren
   weich auf Rot. Die Schrift bleibt dabei weiss. */
.ds-btn.nav-contact, .ds-btn.nav-shop, .ds-btn.mnav__cta {
  background: var(--surface-dark); color: var(--on-dark);
  transition: background-color .3s cubic-bezier(.22, .61, .36, 1),
              color .3s cubic-bezier(.22, .61, .36, 1);
}
.ds-btn.nav-contact:hover, .ds-btn.nav-contact:focus-visible,
.ds-btn.nav-shop:hover, .ds-btn.nav-shop:focus-visible,
.ds-btn.mnav__cta:hover, .ds-btn.mnav__cta:focus-visible {
  background: var(--primary); color: var(--on-dark);
}

.burger {
  display: none; margin-left: auto; width: 48px; height: 48px;
  background: var(--surface-dark); border: none; cursor: pointer;
  align-items: center; justify-content: center;
}
.burger__bars, .burger__bars::before, .burger__bars::after {
  display: block; width: 22px; height: 2px; background: var(--on-dark); content: "";
}
.burger__bars { position: relative; }
.burger__bars::before { position: absolute; top: -7px; }
.burger__bars::after  { position: absolute; top: 7px; }

/* Umschaltpunkt: unter 1160px passt die Leiste nicht mehr in eine Zeile.
   Auf Geraeten ohne Maus gilt dasselbe unabhaengig von der Breite: Die
   Untermenues klappen ueber :hover und :focus-within auf, und ein Tipp auf
   einen Elternpunkt springt dort auf dessen Seite, statt das Untermenue zu
   oeffnen. Ein grosses Tablet bekommt deshalb das Mobilmenue. */
@media (max-width: 1159px), (pointer: coarse) {
  .nav { display: none; }
  .burger { display: flex; }
}

/* --- Mobilmenue ---------------------------------------------------------- */
.mnav {
  position: fixed; inset: 76px 0 0 0; z-index: 55; background: var(--canvas);
  overflow-y: auto; padding: 24px clamp(20px, 5vw, 32px) 64px;
  display: flex; flex-direction: column; gap: 28px;
}
.mnav[hidden] { display: none; }
.mnav__block { display: flex; flex-direction: column; }
.mnav__block--sub { gap: 4px; }
.mnav__head { color: var(--muted); padding-bottom: 8px; }
.mnav__block > a { color: var(--ink); padding: 14px 0; border-bottom: 1px solid var(--hairline); }
.mnav__block--sub > a { padding: 12px 0; border-bottom: none; border-top: 1px solid var(--hairline); }
.mnav [aria-current="page"] { color: var(--primary); font-weight: 600; }
.mnav__cta { justify-content: center; }
body.mnav-open { overflow: hidden; }
/* Mobilmenue auf dem Tablet: zwei Spalten. In einer Spalte war die Liste
   1.358 px hoch und musste auch auf einem 1.024 px hohen Tablet gescrollt
   werden. Ein Raster taugt dafuer nicht - dort ist jede Zeile so hoch wie ihr
   groesster Block, und neben "Start" klaffte ein Loch von 300 px. Echter
   Mehrspaltensatz fuellt die Spalten dagegen fortlaufend. Er steht in einem
   eigenen Element, weil die Hoehe dort vom Inhalt kommt; auf dem scrollenden
   .mnav wuerde er seitlich auslaufen. */
.mnav__spalten { display: flex; flex-direction: column; gap: 28px; }
@media (min-width: 600px) {
  .mnav__spalten { display: block; columns: 2; column-gap: clamp(32px, 6vw, 72px); }
  .mnav__block { break-inside: avoid; margin-bottom: 28px; }
  .mnav__block:last-child { margin-bottom: 0; }
}


/* --- Parallax ------------------------------------------------------------ */
/* Ein Hintergrundbild je Seite. background-attachment:fixed erzeugt den
   Effekt ohne JavaScript; auf iOS rendert WebKit das nicht als Parallax,
   dort springt site.js mit jarallax ein. */
.hero-parallax {
  position: relative;
  background-color: var(--surface-dark);
  background-position: center center;
  background-size: cover;
  background-attachment: fixed;
  /* Der Bildkopf ist der einzige Ort mit Bildhintergrund. Er traegt die
     Seite, deshalb bekommt er eine Mindesthoehe und der Inhalt sitzt
     unten - darueber bleibt das Bild frei sichtbar. */
  /* Der Abstand von der Kopfleiste zur Ueberschrift ist fest - damit steht
     die H1 auf jeder Seite an derselben Stelle. Die Hoehe des Bildkopfs
     richtet sich danach nach dem Inhalt: unter dem Text bleiben immer
     dieselben 48-80 px. */
  min-height: clamp(360px, 44vh, 520px);
  display: grid; align-content: start;
  padding: clamp(140px, 20vw, 300px) clamp(20px, 4vw, 32px) clamp(48px, 7vw, 80px);
}
.hero-parallax::before {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  /* Zwei Verlaeufe: einer von unten, damit der Text auf dunklem Grund
     steht, einer von links, damit die Textspalte auch bei hellen Motiven
     traegt. Oben bleibt das Bild weitgehend frei. */
  background:
    linear-gradient(90deg, rgba(14, 19, 25, .76) 0%, rgba(14, 19, 25, .38) 48%,
                           rgba(14, 19, 25, 0) 78%),
    linear-gradient(180deg, rgba(20, 26, 33, .26) 0%, rgba(20, 26, 33, .40) 34%,
                            rgba(14, 19, 25, .84) 76%, rgba(12, 17, 22, .93) 100%);
}
/* Feine rote Kante am Fuss des Bildkopfs - die Marke sitzt an der Naht
   zwischen Bild und Inhalt. */
.hero-parallax::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 3px;
  background: var(--primary); z-index: 2;
}
.hero-parallax > * { position: relative; z-index: 1; }

.ds-cta-band {
  position: relative; overflow: hidden;
  background-color: var(--surface-dark); color: var(--on-dark);
  background-position: center center; background-size: cover;
  background-attachment: fixed;
  padding: var(--space-section) clamp(20px, 4vw, 32px);
}
.ds-cta-band::before {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: rgba(26,33,41,.88);
}
.ds-cta-band__inner {
  position: relative; z-index: 1; max-width: 760px; margin: 0 auto;
  display: flex; flex-direction: column; align-items: center;
  text-align: center; gap: var(--space-md);
}
.ds-cta-band__eyebrow { color: var(--on-dark-soft); }
.ds-cta-band__title { color: var(--on-dark); }
.ds-cta-band__body { color: var(--on-dark-soft); }
.ds-cta-band__actions { display: flex; gap: var(--space-sm); flex-wrap: wrap; justify-content: center; margin-top: var(--space-xs); }

/* --- Komponenten des Design-Systems -------------------------------------- */
.ds-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 10px;
  height: var(--control-height); padding: 14px 32px; border: none;
  border-radius: var(--radius-none); cursor: pointer; box-shadow: none;
  font-family: var(--font-display); font-size: var(--button-size); font-weight: 700;
  line-height: 1; letter-spacing: var(--button-tracking); white-space: nowrap;
  text-decoration: none;
}
.ds-btn--primary { background: var(--action-bg); color: var(--action-fg); }
.ds-btn--primary:hover, .ds-btn--primary:focus-visible { background: var(--action-bg-active); color: var(--action-fg); }
.ds-btn--secondary { background: var(--canvas); color: var(--ink); border: 1px solid var(--border-emphasis); }
.ds-btn--secondary-on-dark { background: transparent; color: var(--on-dark); border: 1px solid var(--on-dark); }
.ds-btn--secondary-on-dark:hover, .ds-btn--secondary-on-dark:focus-visible { background: var(--on-dark); color: var(--surface-dark); }

.ds-link {
  display: inline-flex; align-items: center; gap: 6px; color: var(--ink);
  font-family: var(--font-display); font-size: var(--label-uppercase-size);
  font-weight: 700; line-height: var(--label-uppercase-lh);
  letter-spacing: var(--label-uppercase-tracking); text-transform: uppercase;
}
.ds-link:hover, .ds-link:focus-visible { color: var(--primary); }
.ds-link__chev { font-weight: 400; font-size: 15px; line-height: 1; }

/* --- Kontaktformular ----------------------------------------------------- */
.kform { display: flex; flex-direction: column; gap: var(--space-md); }
.kform__hinweis { color: var(--muted); font-family: var(--font-body); font-size: 14px; margin: 0; }
.kform__raster {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-sm) var(--space-md);
}
.feld { display: flex; flex-direction: column; gap: 6px; }
.feld--breit { grid-column: 1 / -1; }
.feld label {
  font-family: var(--font-display); font-weight: 700; font-size: 13px;
  letter-spacing: 1.4px; text-transform: uppercase; color: var(--ink);
}
.feld input, .feld select, .feld textarea {
  font-family: var(--font-body); font-size: 16px; color: var(--ink);
  background: var(--canvas); border: 1px solid var(--border-emphasis);
  border-radius: 0; padding: 12px 14px; width: 100%; box-sizing: border-box;
  transition: border-color .2s ease, box-shadow .2s ease;
}
.feld textarea { resize: vertical; min-height: 150px; }
.feld select { appearance: none; background-image: none; cursor: pointer; }
.feld input:focus, .feld select:focus, .feld textarea:focus {
  outline: none; border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(207, 31, 20, .16);
}
.feld [aria-invalid="true"] { border-color: var(--primary); }
.feld__fehler { margin: 0; color: var(--primary); font-family: var(--font-body); font-size: 14px; }
.kform__zustimmung {
  display: grid; grid-template-columns: 20px 1fr; gap: 12px; align-items: start;
}
.kform__zustimmung input { width: 20px; height: 20px; margin-top: 2px; accent-color: var(--primary); }
.kform__zustimmung label { font-family: var(--font-body); font-size: 14px; color: var(--body); }
/* Honigtopf gegen Formular-Roboter: unsichtbar, aber im Fluss - die alte
   Variante mit left:-9999px laeuft aus dem Layout heraus. */
.kform { position: relative; }
.kform__fuellfeld {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0;
}
.kform__aktion { display: flex; flex-wrap: wrap; gap: var(--space-sm); align-items: center; }
.kform__status { margin: 0; font-family: var(--font-body); font-size: 14px; }
.kform__status--fehler { color: var(--primary); }
.kform__status--ok { color: var(--body); }
.kform__neben {
  display: flex; flex-direction: column; gap: var(--space-sm);
  background: var(--surface-soft); padding: var(--card-padding);
  border-top: 3px solid var(--primary);
}
.kform__neben p { margin: 0; color: var(--body); }

.ds-spec { display: flex; flex-direction: column; gap: var(--space-xs); padding: var(--space-md) 0; }
.ds-spec__value { color: var(--ink); }
.ds-spec__unit { margin-left: 4px; }
.ds-spec__label { color: var(--muted); }

.ds-card { background: var(--canvas); border-radius: var(--radius-none); box-shadow: none; display: flex; flex-direction: column; }
.ds-card__photo { width: 100%; display: block; background: var(--surface-card); }
.ds-card__body {
  padding: calc(var(--card-padding) + 12px) var(--card-padding) var(--card-padding);
  display: flex; flex-direction: column; gap: var(--space-sm); align-items: flex-start;
}
/* Kartenraster bekommen mehr Luft als die uebrigen Raster. Das !important
   ist noetig, weil der Abstand im Design als Inline-Stil steht. */
main div:has(> .ds-card) { gap: clamp(24px, 3.2vw, 44px) !important; }
.ds-card__body h3 { color: var(--ink); }
.ds-card__body p { margin: 0; color: var(--body); }
.ds-card__eyebrow { color: var(--muted); text-transform: uppercase; }

.ds-stripe {
  width: 100%; height: var(--stripe-height);
  background: linear-gradient(90deg,
    var(--accent-blue-light) 0 33.34%,
    var(--accent-blue-dark) 33.34% 66.67%,
    var(--accent-red) 66.67% 100%);
}

/* --- Fussbereich --------------------------------------------------------- */
.site-footer { background: var(--surface-soft); padding: clamp(40px, 6vw, 64px) clamp(20px, 4vw, 32px); }
.site-footer__inner { max-width: var(--container-max); margin: 0 auto; display: flex; flex-direction: column; gap: clamp(32px, 4vw, 48px); }
.site-footer__cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: clamp(24px, 3vw, 32px); }
.fcol { display: flex; flex-direction: column; gap: 12px; }
.fcol h2 { color: var(--ink); }
.fcol p, .fcol a { color: var(--muted); }
.fcol a:hover { color: var(--primary); }
.fcert { width: 120px; height: auto; background: var(--canvas); padding: 10px; box-sizing: border-box; }
.site-footer__bar { border-top: 1px solid var(--hairline); padding-top: 24px; display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; align-items: center; }
.site-footer__bar span { color: var(--muted); }
.site-footer__social { display: flex; gap: 24px; flex-wrap: wrap; }
.site-footer__social a { color: var(--muted); }
.site-footer__social a:hover { color: var(--primary); }

/* --- Touch-Bedienung ------------------------------------------------------ */
/* Auf Geraeten ohne Maus muss jedes Ziel mit dem Daumen treffbar sein.
   Gemessen waren die Verweise im Fussbereich 17-22 px hoch und die
   Karten-Verweise 17 px - zu wenig fuer einen Daumen. 44 px ist der uebliche
   Richtwert. Verweise mitten im Fliesstext bleiben ausgenommen: Sie gehoeren
   in die Zeile, und die Richtlinie nimmt sie ausdruecklich aus. */
@media (max-width: 1159px), (pointer: coarse) {
  .fcol a,
  .site-footer__social a,
  main .ds-link {
    display: inline-flex; align-items: center; min-height: 44px;
  }
  .fcol { gap: 4px; }
  .fcol h2 { margin-bottom: 8px; }
  /* 13 px sind auf dem Handy zu klein zum Lesen */
  .site-footer__social a { font-size: 14px; }
  /* Telefon- und E-Mail-Verweise im Kontaktkasten stehen in der Zeile -
     die Polsterung vergroessert die Trefferflaeche, ohne den Zeilenfall
     zu veraendern. */
  main a[href^="tel:"], main a[href^="mailto:"] { padding: 12px 0; }
  /* Ankreuzfeld fuer die Zustimmung */
  .kform__zustimmung { grid-template-columns: 28px 1fr; }
  .kform__zustimmung input { width: 28px; height: 28px; margin-top: 0; }
}

/* --- Rechtsseiten -------------------------------------------------------- */
.legal { padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px); }
.legal__inner { max-width: 820px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }
.legal h2 { color: var(--ink); margin-top: 16px; }
.legal p, .legal li { color: var(--body); }

@media (prefers-reduced-motion: reduce) {
  .hero-parallax, .ds-cta-band { background-attachment: scroll; }
  * { transition-duration: .01ms !important; }
}
"""

SITE_JS = """/* sms engineering — Website
   1. Mobilmenue
   2. Parallax-Ersatz fuer iOS
   3. Menuelinks fuehren immer an den Seitenanfang
*/
(function () {
  'use strict';

  /* --- 1. Mobilmenue ---------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var mnav = document.getElementById('mobilmenue');
  var setOpen = null;
  if (burger && mnav) {
    setOpen = function (open) {
      mnav.hidden = !open;
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
      document.body.classList.toggle('mnav-open', open);
    };
    burger.addEventListener('click', function () {
      setOpen(mnav.hidden);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !mnav.hidden) { setOpen(false); burger.focus(); }
    });
    // Beim Wechsel auf Desktopbreite wieder schliessen, sonst bleibt der
    // Scroll-Lock am body haengen.
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1160 && !mnav.hidden) { setOpen(false); }
    });
  }

  /* --- 2. Parallax auf iOS ---------------------------------------------- */
  // WebKit auf iOS rendert background-attachment:fixed nicht als Parallax -
  // Absicht von Apple, kein Fehler. jarallax erzeugt dort stattdessen ein
  // echtes position:fixed-Kindelement. Alle anderen Browser bleiben bei CSS.
  function isIOS() {
    var ua = navigator.userAgent || '';
    if (/iP(hone|od|ad)/.test(ua)) { return true; }
    return navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1;
  }
  function reduced() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function initParallax() {
    if (!isIOS() || reduced() || typeof window.jarallax !== 'function') { return; }
    var els = document.querySelectorAll('.hero-parallax, .ds-cta-band');
    if (els.length) { window.jarallax(els, { speed: 0 }); }
  }
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    initParallax();
  } else {
    document.addEventListener('DOMContentLoaded', initParallax);
  }

  /* --- 3. Menuelinks fuehren an den Seitenanfang ------------------------- */
  // Zwei Faelle, die der Browser von sich aus nicht so loest, wie man es
  // erwartet: ein Klick auf die Seite, auf der man schon steht, tut nichts,
  // und beim Laden stellt der Browser die alte Scrollposition wieder her.
  // Beides wird hier nur fuer Klicks aus Kopf- und Fussbereich abgefangen -
  // der Zurueck-Knopf behaelt sein normales Verhalten.
  var TOP_KEY = 'sms:scroll-top';

  function reducedMotion() {
    return !!(window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function store(v) {
    try { if (v) { sessionStorage.setItem(TOP_KEY, '1'); }
          else { sessionStorage.removeItem(TOP_KEY); } } catch (e) {}
  }
  function wanted() {
    try { return sessionStorage.getItem(TOP_KEY) === '1'; } catch (e) { return false; }
  }
  function toTop(smooth) {
    try { window.scrollTo({ top: 0, left: 0, behavior: smooth ? 'smooth' : 'auto' }); }
    catch (e) { window.scrollTo(0, 0); }
  }
  function samePage(a) {
    return a.pathname === location.pathname && a.search === location.search;
  }

  function onMenuClick(e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || e.defaultPrevented || e.button !== 0) { return; }
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
    if (a.target && a.target !== '_self') { return; }
    if (a.origin !== location.origin) { return; }       // mailto:, tel:, extern
    if (a.hash) { return; }                             // Sprungmarken in Ruhe lassen

    if (samePage(a)) {
      // Schon auf dieser Seite: nicht neu laden, nur nach oben
      e.preventDefault();
      if (mnav && !mnav.hidden && typeof setOpen === 'function') { setOpen(false); }
      toTop(!reducedMotion());
      var main = document.getElementById('inhalt');
      if (main) {
        main.setAttribute('tabindex', '-1');
        try { main.focus({ preventScroll: true }); } catch (err) { main.focus(); }
      }
      return;
    }
    store(true);                                        // naechste Seite oben starten
  }

  ['.site-header', '.mnav', '.site-footer'].forEach(function (sel) {
    var box = document.querySelector(sel);
    if (box) { box.addEventListener('click', onMenuClick); }
  });

  // Beim Ankommen: der Browser stellt die alte Position wieder her, danach
  // sind wir dran. pageshow deckt auch den Vor-/Zurueck-Cache ab.
  function applyTop() {
    if (!wanted()) { return; }
    store(false);
    toTop(false);
    requestAnimationFrame(function () { toTop(false); });
  }

  window.addEventListener('pageshow', applyTop);
  applyTop();

})();
"""

LEGAL = """  <section class="hero-parallax" style="background-image:url('assets/img/bg/{slug}.jpg')">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px">
      <span class="t-label" style="color: var(--on-dark-soft)">Rechtliches</span>
      <h1 class="t-display-xl" style="color: var(--on-dark); font-size: clamp(32px, 4.6vw, 56px)">{title}</h1>
    </div>
  </section>
  <section class="legal">
    <div class="legal__inner">
      <p class="t-body-md"><strong>Platzhalter.</strong> {hint}</p>
      {body}
    </div>
  </section>
"""


def main(src_path, ds_dir, out_dir, jarallax_path):
    src = open(src_path, encoding="utf-8").read()
    assets = os.path.join(out_dir, "assets")
    os.makedirs(assets, exist_ok=True)

    # Seitenkoerper herausschneiden
    bodies = {}
    for slug, *_ in PAGES:
        var = VAR[slug]
        m = re.search(r'<sc-if value="\{\{ p\.' + var + r' \}\}"[^>]*>\s*(<main>.*?</main>)\s*</sc-if>',
                      src, re.S)
        if not m:
            raise SystemExit("Seite nicht gefunden: " + slug)
        inner = m.group(1)
        inner = inner[len("<main>"):-len("</main>")]
        # CtaBandPhoto haengt in einem eigenen sc-if
        inner = re.sub(r'<sc-if value="\{\{ contactBand \}\}"[^>]*>(.*?)</sc-if>', r"\1", inner, flags=re.S)
        bodies[slug] = transform(inner, slug)

    # Seiten schreiben
    for slug, fname, title, _ in PAGES:
        page = (HEAD.format(title=title, descr=DESCR[slug],
                            nav=nav_html(slug), mnav=mobile_html(slug))
                + bodies[slug] + FOOT)
        open(os.path.join(out_dir, fname), "w", encoding="utf-8").write(page)

    # Impressum / Datenschutz als Platzhalterseiten
    for slug, title, hint, body in [
        ("impressum", "Impressum",
         "Die Pflichtangaben nach § 5 DDG gehören hier hinein — der Design-Export "
         "verwies auf die alte Domain, deren Inhalt nicht mehr erreichbar ist.",
         '<h2 class="t-title-lg">Angaben gemäß § 5 DDG</h2>'
         '<p class="t-body-md">sms engineering GmbH<br>Seckendorfer Straße 6<br>90556 Cadolzburg</p>'
         '<p class="t-body-md">Telefon: +49 9103 91849 0<br>E-Mail: info@sms.gmbh</p>'
         '<h2 class="t-title-lg">Noch zu ergänzen</h2>'
         '<ul class="t-body-md"><li>Vertretungsberechtigte Geschäftsführung</li>'
         '<li>Registergericht und Handelsregisternummer</li>'
         '<li>Umsatzsteuer-Identifikationsnummer</li>'
         '<li>Verantwortlich für den Inhalt</li></ul>'),
        ("datenschutz", "Datenschutz",
         "Eine vollständige Datenschutzerklärung muss juristisch geprüft werden.",
         '<h2 class="t-title-lg">Zu regeln</h2>'
         '<ul class="t-body-md"><li>Verantwortlicher und Kontaktdaten</li>'
         '<li>Hosting und Server-Logfiles</li>'
         '<li>Schriftarten: Archivo wird derzeit von Google Fonts geladen — '
         'für den Livebetrieb besser selbst hosten</li>'
         '<li>YouTube-Einbettung auf der Seite „Sicherheitszellen“ — aktuell über '
         'youtube-nocookie.com, eine Zwei-Klick-Lösung wäre sauberer</li>'
         '<li>Kontaktaufnahme per E-Mail</li>'
         '<li>Rechte der betroffenen Personen</li></ul>'),
    ]:
        page = (HEAD.format(title=title, descr=title + " der sms engineering GmbH.",
                            nav=nav_html(None), mnav=mobile_html(None))
                + LEGAL.format(slug="impressum", title=title, hint=hint, body=body)
                + FOOT)
        open(os.path.join(out_dir, slug + ".html"), "w", encoding="utf-8").write(page)

    # CSS: Tokens aus dem Design-System unveraendert uebernehmen
    tok = [FONTFACE]
    for f in ["tokens/colors.css", "tokens/typography.css",
              "tokens/spacing.css", "tokens/shape.css", "tokens/base.css"]:
        tok.append("/* ---- " + f + " ---- */\n" + open(os.path.join(ds_dir, f), encoding="utf-8").read())
    open(os.path.join(assets, "tokens.css"), "w", encoding="utf-8").write("\n".join(tok) + THEME)
    open(os.path.join(assets, "site.css"), "w", encoding="utf-8").write(SITE_CSS)
    open(os.path.join(assets, "site.js"), "w", encoding="utf-8").write(SITE_JS)
    shutil.copy(jarallax_path, os.path.join(assets, "jarallax.min.js"))

    # Bildliste fuer den Platzhalter-Generator
    spec = {"content": {}, "mark": {}, "bg": {}}
    for name, label in IMG_USED.items():
        if name in MARKS:
            spec["mark"][name] = MARKS[name]
        else:
            spec["content"][name] = {"label": label, "size": [1600, 1000]}
    for name, meta in MARKS.items():
        spec["mark"].setdefault(name, meta)
    for slug, _, _, bglabel in PAGES:
        spec["bg"][slug] = bglabel
    spec["bg"]["impressum"] = "Rechtliches"
    spec["bg"]["cta"] = "sms engineering, Cadolzburg"
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagespec.json"),
         "w", encoding="utf-8").write(json.dumps(spec, ensure_ascii=False, indent=1))

    print(f"{len(PAGES)} Seiten + 2 Rechtsseiten geschrieben nach {out_dir}")
    print(f"{len(spec['content'])} Inhaltsbilder, {len(spec['mark'])} Marken, {len(spec['bg'])} Hintergründe")


if __name__ == "__main__":
    main(*sys.argv[1:5])
