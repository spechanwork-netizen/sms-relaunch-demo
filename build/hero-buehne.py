# -*- coding: utf-8 -*-
"""Bildkopf der Startseite auf den Entwurf "Buehne" umstellen (Entwurf A).

Nur die Startseite. Die Unterseiten behalten .hero-parallax mit
background-attachment: fixed. Hier traegt ein eigener Bildlayer das Motiv,
weil ein fixiertes Hintergrundbild sich nicht zoomen laesst - und der
langsame Zoom ist der Kern des Entwurfs.

Idempotent: laeuft das Skript zweimal, passiert beim zweiten Mal nichts.
"""
import io, re, sys

WURZEL = '/home/claude/sms-website'

HERO_NEU = '''  <section class="hero-buehne">
    <div class="hero-buehne__bild" style="background-image:url(&quot;assets/img/bg/home.jpg&quot;)"></div>
    <div class="hero-buehne__inhalt">
      <span class="hero-buehne__regel" aria-hidden="true"></span>
      <span class="t-label hero-buehne__kenn">FLY | HIGH | BUTTERFLY</span>
      <h1 class="t-display-xl hero-buehne__titel">
        <span class="hero-buehne__zeile"><span>Flexibilität.</span></span>
        <span class="hero-buehne__zeile"><span>Präzision.</span></span>
        <span class="hero-buehne__zeile"><span>Zuverlässigkeit.</span></span>
      </h1>
      <p class="t-body-md hero-buehne__text">Komplettfertiger und Engineering-Dienstleister für Prototypen, Kleinserien und komplexe Baugruppen.</p>
      <div class="hero-buehne__knoepfe">
        <a class="ds-btn ds-btn--primary hero-knopf" href="https://shop.sms.gmbh" target="_blank" rel="noopener"><span>Kart-Shop</span></a>
        <a class="ds-btn ds-btn--secondary-on-dark hero-knopf" href="kontakt.html"><span>Kontakt</span></a>
      </div>
    </div>
    <img class="hero-buehne__logo" src="assets/img/sms-logo-hell.png" alt="" loading="eager" decoding="async" width="568" height="240">
    <span class="hero-buehne__cue" aria-hidden="true"></span>
  </section>
'''

CSS_NEU = '''
/* --- Bildkopf der Startseite: Entwurf "Buehne" ---------------------------
   Gilt nur fuer index.html. Die Unterseiten behalten .hero-parallax mit
   background-attachment: fixed. Hier liegt das Motiv in einem eigenen
   Layer, weil ein fixierter Hintergrund sich nicht zoomen laesst - und der
   langsame Zoom ("das Bild atmet") ist der Kern des Entwurfs. */
.hero-buehne {
  position: relative; overflow: hidden;
  background-color: var(--surface-dark);
  min-height: min(88vh, 780px);
  display: grid; align-content: end;
  padding: clamp(120px, 18vw, 240px) clamp(20px, 4vw, 32px) clamp(44px, 6vw, 72px);
}
.hero-buehne__bild {
  position: absolute; inset: 0; z-index: 0;
  background-size: cover; background-position: center 58%;
  animation: heroZoom 24s ease-in-out infinite alternate;
}
@keyframes heroZoom { from { transform: scale(1.04); } to { transform: scale(1.16); } }
/* Dieselben zwei Verlaeufe wie bei .hero-parallax - der Entwurf aendert die
   Anordnung, nicht die Lesbarkeitsgrundlage. */
.hero-buehne::before {
  content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background:
    linear-gradient(90deg, rgba(14, 19, 25, .76) 0%, rgba(14, 19, 25, .38) 48%,
                           rgba(14, 19, 25, 0) 78%),
    linear-gradient(180deg, rgba(20, 26, 33, .26) 0%, rgba(20, 26, 33, .40) 34%,
                            rgba(14, 19, 25, .84) 76%, rgba(12, 17, 22, .93) 100%);
}
.hero-buehne::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 3px;
  background: var(--primary); z-index: 4;
}
.hero-buehne__inhalt {
  position: relative; z-index: 3; width: 100%; max-width: 1440px; margin: 0 auto;
  display: flex; flex-direction: column; align-items: flex-start; gap: 14px;
}
.hero-buehne__regel {
  display: block; height: 3px; width: 96px; background: var(--primary);
  transform: scaleX(0); transform-origin: left;
  animation: heroRegel .9s .15s cubic-bezier(.22, .61, .36, 1) forwards;
}
@keyframes heroRegel { to { transform: scaleX(1); } }
.hero-buehne__kenn { color: var(--on-dark); opacity: 0; animation: heroEin .7s .3s ease forwards; }
.hero-buehne__titel {
  color: var(--on-dark); font-size: clamp(36px, 6.4vw, 78px);
  line-height: 1.02; letter-spacing: -1.4px; margin: 2px 0 4px; max-width: 16ch;
}
/* Jede Zeile faehrt aus ihrem eigenen Fenster hoch. Das Fenster muss
   overflow: hidden haben, sonst sieht man die Schrift von unten kommen. */
.hero-buehne__zeile { display: block; overflow: hidden; }
.hero-buehne__zeile > span {
  display: block; transform: translateY(105%);
  animation: heroHoch .85s cubic-bezier(.16, 1, .3, 1) forwards;
}
.hero-buehne__zeile:nth-child(1) > span { animation-delay: .42s; }
.hero-buehne__zeile:nth-child(2) > span { animation-delay: .55s; }
.hero-buehne__zeile:nth-child(3) > span { animation-delay: .68s; }
@keyframes heroHoch { to { transform: translateY(0); } }
.hero-buehne__text {
  color: var(--on-dark-soft); max-width: 560px; margin: 0;
  opacity: 0; animation: heroEin .7s .95s ease forwards;
}
.hero-buehne__knoepfe {
  display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px;
  opacity: 0; animation: heroEin .7s 1.07s ease forwards;
}
@keyframes heroEin { to { opacity: 1; } }
.hero-buehne__logo {
  position: absolute; z-index: 3; right: clamp(20px, 4vw, 32px);
  bottom: clamp(34px, 5vw, 60px); width: clamp(150px, 17vw, 240px);
  height: auto; display: block; opacity: 0;
  animation: heroEin .8s 1.25s ease forwards;
}
/* Auf dem Handy laege das Logo auf den Knoepfen - die Kopfleiste zeigt es
   ohnehin. */
@media (max-width: 760px) { .hero-buehne__logo { display: none; } }
.hero-buehne__cue {
  position: absolute; z-index: 4; left: clamp(20px, 4vw, 32px); bottom: 14px;
  width: 1px; height: 46px; background: rgba(255, 255, 255, .18);
}
.hero-buehne__cue::after {
  content: ""; position: absolute; inset: 0; background: var(--primary);
  animation: heroCue 2.2s ease-in-out infinite;
}
@keyframes heroCue {
  0%   { transform: scaleY(0); transform-origin: top; }
  45%  { transform: scaleY(1); transform-origin: top; }
  55%  { transform: scaleY(1); transform-origin: bottom; }
  100% { transform: scaleY(0); transform-origin: bottom; }
}

/* Knoepfe im Bildkopf: die Farbe wischt von links herein statt umzuspringen.
   Die Beschriftung steckt in einem <span>, weil ein positioniertes ::before
   sonst ueber dem Text laege. */
.hero-knopf { position: relative; overflow: hidden; transition: transform .25s cubic-bezier(.22, .61, .36, 1); }
.hero-knopf > span { position: relative; z-index: 1; }
.hero-knopf::before {
  content: ""; position: absolute; inset: 0; z-index: 0;
  transform: scaleX(0); transform-origin: right;
  transition: transform .4s cubic-bezier(.76, 0, .24, 1);
}
.hero-knopf:hover, .hero-knopf:focus-visible { transform: translateY(-2px); }
.hero-knopf:hover::before, .hero-knopf:focus-visible::before { transform: scaleX(1); transform-origin: left; }
.ds-btn--primary.hero-knopf::before { background: var(--action-bg-active); }
.ds-btn--primary.hero-knopf:hover, .ds-btn--primary.hero-knopf:focus-visible { background: var(--action-bg); }
.ds-btn--secondary-on-dark.hero-knopf::before { background: var(--on-dark); }
.ds-btn--secondary-on-dark.hero-knopf { transition: transform .25s cubic-bezier(.22, .61, .36, 1), color .25s .12s ease; }
.ds-btn--secondary-on-dark.hero-knopf:hover,
.ds-btn--secondary-on-dark.hero-knopf:focus-visible { background: transparent; color: var(--surface-dark); }

@media (prefers-reduced-motion: reduce) {
  .hero-buehne__bild, .hero-buehne__regel, .hero-buehne__kenn,
  .hero-buehne__zeile > span, .hero-buehne__text, .hero-buehne__knoepfe,
  .hero-buehne__logo, .hero-buehne__cue::after { animation: none; }
  .hero-buehne__regel { transform: scaleX(1); }
  .hero-buehne__zeile > span { transform: none; }
  .hero-buehne__kenn, .hero-buehne__text, .hero-buehne__knoepfe,
  .hero-buehne__logo { opacity: 1; }
  /* Ohne Bewegung bleibt der schlichte Farbwechsel von frueher. */
  .hero-knopf, .hero-knopf::before { transition: none; }
  .hero-knopf:hover, .hero-knopf:focus-visible { transform: none; }
  .hero-knopf::before { display: none; }
  .ds-btn--primary.hero-knopf:hover,
  .ds-btn--primary.hero-knopf:focus-visible { background: var(--action-bg-active); }
  .ds-btn--secondary-on-dark.hero-knopf:hover,
  .ds-btn--secondary-on-dark.hero-knopf:focus-visible { background: var(--on-dark); color: var(--surface-dark); }
}
'''


def lies(p):
    return io.open(p, encoding='utf-8').read()


def schreib(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)


def hero_tauschen():
    p = WURZEL + '/index.html'
    s = lies(p)
    if 'hero-buehne' in s:
        return 'Startseite: schon umgestellt'
    m = re.search(r'  <section class="hero-parallax".*?\n  </section>\n', s, re.S)
    if not m:
        sys.exit('FEHLER: Bildkopf der Startseite nicht gefunden')
    schreib(p, s[:m.start()] + HERO_NEU + s[m.end():])
    return 'Startseite: Bildkopf ersetzt'


def css_ergaenzen():
    p = WURZEL + '/assets/site.css'
    s = lies(p)
    if '.hero-buehne' in s:
        return 'site.css: schon ergaenzt'
    schreib(p, s.rstrip('\n') + '\n' + CSS_NEU)
    return 'site.css: Entwurf Buehne ergaenzt'


def mirror():
    """Die Baukopie von site.css mitziehen, sonst laeuft sie auseinander."""
    p = WURZEL + '/build/build_part2.py'
    s = lies(p)
    if '.hero-buehne' in s:
        return 'build_part2.py: schon ergaenzt'
    marke = 'SITE_CSS = r"""'
    if marke not in s:
        return 'build_part2.py: SITE_CSS nicht gefunden, uebersprungen'
    ende = s.index('"""', s.index(marke) + len(marke))
    schreib(p, s[:ende] + CSS_NEU + s[ende:])
    return 'build_part2.py: Entwurf Buehne ergaenzt'


for meldung in (hero_tauschen(), css_ergaenzen(), mirror()):
    print(meldung)
