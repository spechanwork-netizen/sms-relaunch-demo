# -*- coding: utf-8 -*-
"""Kopfbereich auf Entwurf B umstellen.

Die Leiste liegt ueber dem Bildkopf statt darueber zu stehen, wird beim
Scrollen dunkel und verschwindet beim Herunterscrollen ganz - bis man wieder
hochscrollt.

  python3 -I build/kopf-b.py

Mehrfach ausfuehrbar.
"""
import io, glob, os, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''
/* --- Kopfbereich: Entwurf B ----------------------------------------------
   Die Leiste liegt ueber dem Bildkopf (position: fixed) statt darueber zu
   stehen, ist dort durchsichtig und wird beim Scrollen dunkel. Beim
   Herunterscrollen faehrt sie ganz weg und kommt erst zurueck, wenn wieder
   nach oben gescrollt wird - das erledigt motion.js ueber .is-hidden.

   Grundzustand ist bewusst die dunkle Leiste: ohne JavaScript gibt es kein
   .js-motion und damit kein .is-scrolled. Eine durchsichtige Leiste stuende
   dann spaeter ueber weissem Inhalt und waere unlesbar. */
.site-header {
  position: fixed; left: 0; right: 0; top: 0; z-index: 60;
  background: var(--surface-dark);
  border-bottom: 1px solid rgba(255, 255, 255, .12);
}
.js-motion .site-header:not(.is-scrolled) {
  background: transparent; border-bottom-color: rgba(255, 255, 255, .20);
}
/* Schleier hinter der durchsichtigen Leiste. Weisse Schrift allein reicht
   auf einem Industriefoto nicht - auf den hellen Stellen der Maschine war
   die Navigation ohne diesen Verlauf nicht zu lesen. */
.site-header::before {
  content: ""; position: absolute; left: 0; right: 0; top: 0; bottom: -44px;
  z-index: -1; pointer-events: none; opacity: 0; transition: opacity .3s ease;
  background: linear-gradient(180deg, rgba(10, 14, 18, .74) 0%,
                                      rgba(10, 14, 18, .48) 56%,
                                      rgba(10, 14, 18, 0) 100%);
}
.js-motion .site-header:not(.is-scrolled)::before { opacity: 1; }

/* Sprungziele muessen unter der festen Leiste landen, nicht darunter. */
html { scroll-padding-top: 92px; }

/* Beschriftungen auf dunklem Grund. Rot als Schriftfarbe kaeme hier nur auf
   3:1 - deshalb bleibt die Schrift weiss, und der rote Strich aus motion.css
   uebernimmt die Rueckmeldung beim Ueberfahren. */
.nav > a:not(.nav-contact):not(.nav-shop), .nav__top, .nav-group__top { color: var(--on-dark); }
.hv-primary:hover, .hv-primary:focus-visible { color: var(--on-dark); }
.nav [aria-current="page"],
.nav .nav-group:has([aria-current="page"]) .nav-group__top { color: var(--on-dark); }

/* Klappmenues ebenfalls dunkel - ein weisses Feld unter einer dunklen
   Leiste sieht aus wie ein Fremdkoerper. */
.nav-drop {
  background: var(--surface-dark); border-color: rgba(255, 255, 255, .14);
  border-top-color: var(--primary);
}
.nav-drop a { color: var(--on-dark); }
.hv-primary-soft:hover, .hv-primary-soft:focus-visible {
  color: var(--on-dark); background: rgba(255, 255, 255, .09);
}

/* Kontakt gefuellt rot, Kart-Shop nur mit roter Kante und weisser Schrift. */
.ds-btn.nav-contact { background: var(--primary); color: var(--on-primary); }
.ds-btn.nav-contact:hover, .ds-btn.nav-contact:focus-visible { background: var(--primary-active); }
.ds-btn.nav-shop { color: var(--on-dark); }

/* Der Brennerknopf war eine dunkle Flaeche - auf der dunklen Leiste waere
   er unsichtbar. Jetzt nur noch eine feine Kante. */
.burger { background: transparent; border: 1px solid rgba(255, 255, 255, .38); }

/* Bei offenem Mobilmenue muss die Leiste dunkel und voll hoch sein: das
   Menue beginnt bei 76 px, eine geschrumpfte Leiste liesse einen Spalt. */
.js-motion body.mnav-open .site-header,
body.mnav-open .site-header {
  background: var(--surface-dark); border-bottom-color: rgba(255, 255, 255, .12);
}
.js-motion body.mnav-open .site-header::before { opacity: 0; }
body.mnav-open .site-header__inner,
.js-motion body.mnav-open .site-header.is-scrolled .site-header__inner { min-height: 76px; }
'''


def lies(p):
    return io.open(p, encoding='utf-8').read()


def schreib(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)


def css():
    neu = []
    for p in ('assets/site.css', 'build/build_part2.py'):
        voll = os.path.join(WURZEL, p)
        s = lies(voll)
        if 'Kopfbereich: Entwurf B' in s:
            neu.append(p + ': schon da')
            continue
        if p.endswith('.py'):
            marke = 'SITE_CSS = """'
            ende = s.index('"""', s.index(marke) + len(marke))
            schreib(voll, s[:ende] + CSS + s[ende:])
        else:
            schreib(voll, s.rstrip('\n') + '\n' + CSS)
        neu.append(p + ': ergaenzt')
    return neu


def motion_css():
    """Die feste Leiste braucht position: fixed - motion.css setzt sticky."""
    p = os.path.join(WURZEL, 'assets/motion.css')
    s = lies(p)
    alt = '.js-motion .site-header { position: sticky; }'
    nv = '.js-motion .site-header { position: fixed; }'
    if nv in s:
        return 'motion.css: schon da'
    if alt not in s:
        sys.exit('FEHLER: sticky-Regel in motion.css nicht gefunden')
    schreib(p, s.replace(alt, nv))
    return 'motion.css: position fixed'


def motion_js():
    """Im ruhigen Modus steigt motion.js frueh aus. Ohne .is-scrolled bliebe
    die Leiste durchsichtig und stuende spaeter ueber weissem Inhalt."""
    p = os.path.join(WURZEL, 'assets/motion.js')
    s = lies(p)
    if 'ruhigen Modus' in s:
        return 'motion.js: schon da'
    alt = "  root.classList.add('js-motion');\n  if (reduced) { return; }"
    nv = """  root.classList.add('js-motion');

  // Im ruhigen Modus steigt der Rest aus. Die Leiste muss trotzdem dunkel
  // werden, sobald gescrollt wird - sonst bliebe sie durchsichtig und
  // stuende spaeter ueber weissem Inhalt. Weggefahren wird sie dort nicht:
  // das waere Bewegung, die ausdruecklich abbestellt wurde.
  if (reduced) {
    var ruhigerKopf = document.querySelector('.site-header');
    if (ruhigerKopf) {
      var ruhigPruefen = function () {
        ruhigerKopf.classList.toggle('is-scrolled', (window.pageYOffset || 0) > 10);
      };
      window.addEventListener('scroll', ruhigPruefen, { passive: true });
      ruhigPruefen();
    }
    return;
  }"""
    if alt not in s:
        sys.exit('FEHLER: Einstieg in motion.js nicht gefunden')
    schreib(p, s.replace(alt, nv))
    return 'motion.js: ruhiger Modus schaltet die Leiste dunkel'


def logo():
    """Helles Logo auf allen Seiten - die Leiste ist jetzt dunkel."""
    alt = '<img src="assets/img/sms-logo.png" alt="sms engineering GmbH" width="115" height="48">'
    nv = '<img src="assets/img/sms-logo-hell.png" alt="sms engineering GmbH" width="114" height="48">'
    n = 0
    for f in sorted(glob.glob(os.path.join(WURZEL, '*.html'))):
        if f.endswith('-optionen.html'):
            continue
        s = lies(f)
        if alt in s:
            schreib(f, s.replace(alt, nv))
            n += 1
    v = os.path.join(WURZEL, 'build/build_part2.py')
    s = lies(v)
    if alt in s:
        schreib(v, s.replace(alt, nv))
    return 'Logo hell auf %d Seiten' % n


for m in css() + [motion_css(), motion_js(), logo()]:
    print(m)
