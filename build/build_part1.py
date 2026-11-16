#!/usr/bin/env python3
"""Baut aus dem Claude-Design-Export eine statische, lauffaehige Website.

Eingabe : SMS Engineering Website.dc.html  (Prototyp in der Claude-Design-DSL)
Ausgabe : 18 echte HTML-Seiten + gemeinsames CSS/JS + Platzhalterbilder

Der Prototyp laeuft nur im Design-Runtime (support.js): Routing, Dropdowns und
Mobilmenue haengen an sc-if/{{ }}-Ausdruecken, die Komponenten an einem
React-Bundle. Dieses Skript loest all das in normales HTML/CSS/JS auf und
behebt dabei die gefundenen Fehler (siehe BUGFIXES unten).
"""
import json, os, re, shutil, sys, html

# --------------------------------------------------------------------------
# Seiten
# --------------------------------------------------------------------------
PAGES = [
    # slug,            datei,                 titel,                                              bg-beschriftung
    ("home",             "index.html",             "Engineering, Fertigung und Messtechnik aus Cadolzburg", "Fertigung · CNC-Bauteil"),
    ("unternehmen",      "unternehmen.html",       "Unternehmen",                                  "Unternehmen"),
    ("ueber-uns",        "ueber-uns.html",         "Über uns",                                     "sms engineering, Cadolzburg"),
    ("historie",         "historie.html",          "Schmidt Motorsport Historie",                  "Schmidt Motorsport · Rallyesport"),
    ("engineering",      "engineering.html",       "Engineering",                                  "Engineering · Konstruktion"),
    ("e-mobilitaet",     "e-mobilitaet.html",      "E-Mobilität",                                  "E-Mobilität · Antriebsstrang"),
    ("konstruktion",     "konstruktion.html",      "Konstruktion und Entwicklung",                 "Konstruktion · CAD"),
    ("lehren",           "lehren.html",            "Lehren- und Messmittelbau",                    "Messmittelbau · Vorrichtung"),
    ("sicherheitszellen","sicherheitszellen.html", "Sicherheitszellen und Stützgestelle",          "Sicherheitszelle · Stützgestell"),
    ("fertigung",        "fertigung.html",         "Fertigung",                                    "Fertigung · Maschinenpark"),
    ("messen",           "messen.html",            "Messen und Prüfen",                            "Messtechnik · COORD3"),
    ("elektro-kart",     "elektro-kart.html",      "Elektro-Kart",                                 "Elektro-Kart · Parcours"),
    ("revo-sl",          "revo-sl.html",           "sms revo SL",                                  "sms revo SL"),
    ("revo-x",           "revo-x.html",            "sms revo X",                                   "sms revo X · eBuggy"),
    ("spacedrive",       "spacedrive.html",        "sms revo SpaceDrive",                          "sms revo SpaceDrive"),
    ("bestellformulare", "bestellformulare.html",  "Bestellformular",                              "Bestellformular"),
    ("dokumente",        "dokumente.html",         "Wichtige Dokumente",                           "Dokumente"),
]
SLUG2FILE = {s: f for s, f, _, _ in PAGES}
SLUG2FILE[""] = "index.html"
VAR = {s: s.replace("-", "_") for s, _, _, _ in PAGES}

DESCR = {
    "home": "sms engineering GmbH in Cadolzburg: Konstruktion, Prototypenbau, CNC-Fertigung und Qualitätssicherung aus einer Hand.",
    "unternehmen": "Engineering-Dienstleister mit Motorsport-Wurzeln — aus Schmidt Motorsport wurde die sms engineering GmbH.",
    "ueber-uns": "Struktur, Kernkompetenzen und Einbindung in die leomax-Unternehmensgruppe.",
    "historie": "Vom Rallyesport der 1970er-Jahre zum Entwicklungspartner von Audi, VW und Opel.",
    "engineering": "Vier Kompetenzfelder für Serien- und Motorsportanwendungen — von der Konzeptphase bis zum abgesicherten Bauteil.",
    "e-mobilitaet": "Prototypenentwicklung, Packaging und Integration elektrischer Antriebe in bestehende Fahrzeuge.",
    "konstruktion": "Planungs-, Entwicklungs- und Konstruktionsprozesse für Serien- und Motorsportanwendungen.",
    "lehren": "Mechanische und elektronische Mess- und Prüfvorrichtungen nach kundenspezifischen Anforderungen.",
    "sicherheitszellen": "Umbaumaßnahmen an Vorserien- und Versuchsfahrzeugen für sichere und effiziente Versuchsreihen.",
    "fertigung": "Moderner Maschinenpark zur High-End-Produktion: CNC-Fertigung, Schweißfertigung und Montage.",
    "messen": "3D-Koordinatenmesstechnik für Maßkontrolle, Qualitätssicherung und Auftragsvermessung.",
    "elektro-kart": "sms revo: lautlose, emissionsfreie Karts und Buggys für den Motorsport-Nachwuchs.",
    "revo-sl": "Das Elektro-Slalom-Kart von sms engineering — entwickelt für die Einstiegsdisziplin im Kartsport.",
    "revo-x": "Der eBuggy für den Rallye-Nachwuchs, konzipiert für Kinder von sechs bis zwölf Jahren.",
    "spacedrive": "Elektro-Kart mit Space-Drive-Steuerung für den inklusiven Kartslalom.",
    "bestellformulare": "Ausstattungsoptionen und Vorteilspakete für das sms revo SL — zum Download.",
    "dokumente": "Betriebsanleitungen, Batteriehinweise und Wartungspläne zum sms revo SL.",
}

# --------------------------------------------------------------------------
# Bilder: Originaldateiname -> Platzhalter-Beschriftung
# --------------------------------------------------------------------------
MARKS = {
    "sms-logo.png":            {"label": "sms engineering", "sub": "LOGO-PLATZHALTER", "size": [560, 150]},
    "SchmidtMotorsport.png":   {"label": "Schmidt Motorsport", "sub": "LOGO-PLATZHALTER", "size": [1200, 420]},
    "ZertLogo-9001-vektor.png":{"label": "DIN EN ISO 9001", "sub": "ZERTIFIKAT", "size": [480, 480]},
}

# --------------------------------------------------------------------------
# Komponenten des Design-Systems als HTML
# --------------------------------------------------------------------------
def esc(t):
    return t if t is None else t

def c_button(a, children):
    variant = a.get("variant", "primary")
    href = a.get("href", "#")
    return f'<a class="ds-btn ds-btn--{variant}" href="{href}">{children}</a>'

def c_textlink(a, children):
    return (f'<a class="ds-link" href="{a.get("href", "#")}">{children}'
            f'<span class="ds-link__chev" aria-hidden="true">›</span></a>')

def c_spec(a, children):
    unit = f'<span class="t-title-sm ds-spec__unit">{a["unit"]}</span>' if a.get("unit") else ""
    return ('<div class="ds-spec">'
            f'<span class="t-display-sm ds-spec__value">{a.get("value","")}{unit}</span>'
            f'<span class="t-label ds-spec__label">{a.get("label","")}</span></div>')

def c_model(a, children):
    return ('<article class="ds-card">'
            + img_tag(a.get("photo-src"), a.get("name", ""), "16/10", "ds-card__photo")
            + '<div class="ds-card__body">'
            f'<h3 class="t-title-md">{a.get("name","")}</h3>'
            + (f'<p class="t-body-sm">{a["tagline"]}</p>' if a.get("tagline") else "")
            + c_textlink({"href": a.get("href", "#")}, a.get("cta", "Mehr erfahren"))
            + '</div></article>')

def c_feature(a, children):
    return ('<article class="ds-card">'
            + img_tag(a.get("photo-src"), a.get("title", ""), "16/9", "ds-card__photo")
            + '<div class="ds-card__body">'
            + (f'<span class="t-caption ds-card__eyebrow">{a["eyebrow"]}</span>' if a.get("eyebrow") else "")
            + f'<h3 class="t-title-md">{a.get("title","")}</h3>'
            + (f'<p class="t-body-sm">{a["excerpt"]}</p>' if a.get("excerpt") else "")
            + (c_textlink({"href": a.get("href", "#")}, a["cta"]) if a.get("cta") else "")
            + '</div></article>')

def c_ctaband(a, children):
    return ('<section class="ds-cta-band" style="background-image:url(&quot;assets/img/bg/cta.jpg&quot;)">'
            '<div class="ds-cta-band__inner">'
            + (f'<span class="t-label ds-cta-band__eyebrow">{a["eyebrow"]}</span>' if a.get("eyebrow") else "")
            + f'<h2 class="t-display-md ds-cta-band__title">{a.get("title","")}</h2>'
            + (f'<p class="t-body-md ds-cta-band__body">{a["body"]}</p>' if a.get("body") else "")
            + (f'<div class="ds-cta-band__actions">{children}</div>' if children.strip() else "")
            + '</div></section>')

def c_stripe(a, children):
    return '<div class="ds-stripe" role="presentation"></div>'

COMPONENTS = {
    "Button": c_button, "TextLinkCta": c_textlink, "SpecCell": c_spec,
    "ModelCard": c_model, "FeaturePhotoCard": c_feature,
    "CtaBandPhoto": c_ctaband, "AccentStripe": c_stripe,
}

# --------------------------------------------------------------------------
IMG_USED = {}

def img_name(url):
    return url.rsplit("/", 1)[-1]

def img_tag(url, alt, ratio, cls=""):
    if not url:
        return (f'<div class="photo-plate" style="aspect-ratio:{ratio}">'
                f'<span class="photo-plate-label">{alt or "Bild"}</span></div>')
    name = img_name(url)
    IMG_USED.setdefault(name, alt or name)
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}" alt="{alt}" loading="lazy" '
            f'decoding="async" style="aspect-ratio:{ratio};object-fit:cover">')

# --------------------------------------------------------------------------
def parse_attrs(tag):
    return {m.group(1): html.unescape(m.group(2))
            for m in re.finditer(r'([a-zA-Z-]+)="([^"]*)"', tag)}

def render_components(s):
    """Loest <x-import> rekursiv auf (innerste zuerst)."""
    while True:
        start = s.find("<x-import")
        if start == -1:
            return s
        depth, i = 0, start
        while i < len(s):
            nxt_open = s.find("<x-import", i + 1)
            nxt_close = s.find("</x-import>", i)
            if nxt_close == -1:
                return s
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open
            else:
                if depth == 0:
                    end = nxt_close + len("</x-import>")
                    break
                depth -= 1
                i = nxt_close + 1
        else:
            return s
        whole = s[start:end]
        gt = whole.find(">")
        attrs = parse_attrs(whole[:gt])
        inner = render_components(whole[gt + 1:whole.rfind("</x-import>")])
        comp = attrs.get("component-from-global-scope", "").split(".")[-1]
        fn = COMPONENTS.get(comp)
        out = fn(attrs, inner) if fn else inner
        s = s[:start] + out + s[end:]

# --------------------------------------------------------------------------
HOVER = {
    "color: var(--primary)": "hv-primary",
    "color: var(--primary); background: var(--surface-soft)": "hv-primary-soft",
    "background: var(--primary-active); color: var(--on-primary)": "hv-contact",
}

def transform(body, slug):
    body = render_components(body)

    # --- Bilder ersetzen --------------------------------------------------
    def repl_img(m):
        tag = m.group(0)
        a = parse_attrs(tag)
        url = a.get("src", "")
        if not url.startswith("https://sms.gmbh/"):
            return tag
        name = img_name(url)
        IMG_USED.setdefault(name, a.get("alt", name))
        tag = tag.replace(url, f"assets/img/{name}")
        if "loading=" not in tag:
            tag = tag.replace("<img", '<img loading="lazy" decoding="async"', 1)
        return tag
    body = re.sub(r"<img\b[^>]*>", repl_img, body)

    # --- style-hover -> Klasse -------------------------------------------
    def repl_hover(m):
        cls = HOVER.get(m.group(1).strip())
        return f' class="{cls}"' if cls else ""
    body = re.sub(r'\s*style-hover="([^"]*)"', repl_hover, body)
    # doppelte class-Attribute im selben Tag zusammenfuehren
    def merge_class(m):
        tag = m.group(0)
        classes = re.findall(r'class="([^"]*)"', tag)
        if len(classes) < 2:
            return tag
        tag = re.sub(r'\s*class="[^"]*"', "", tag)
        joined = " ".join(classes)
        return tag[:tag.index(" ")] + f' class="{joined}"' + tag[tag.index(" "):]
    body = re.sub(r"<[a-zA-Z][^>]*>", merge_class, body)

    # --- interne Links ----------------------------------------------------
    body = re.sub(r'href="#/([a-z0-9-]*)"',
                  lambda m: f'href="{SLUG2FILE.get(m.group(1), "index.html")}"', body)

    # --- BUGFIX: doppeltes max-width im selben style-Attribut -------------
    def fix_dup_maxwidth(m):
        st = m.group(1)
        if st.count("max-width") < 2:
            return m.group(0)
        widths = re.findall(r"max-width:\s*([^;\"]+)", st)
        st = re.sub(r"max-width:\s*[^;\"]+;?\s*", "", st).strip().rstrip(";")
        inner = widths[-1].strip()
        return (f'style="{st}; max-width: {inner}"' if inner != "1440px"
                else f'style="{st}; max-width: 1440px"')
    body = re.sub(r'style="([^"]*max-width[^"]*)"', fix_dup_maxwidth, body)

    # --- BUGFIX: Telefonnummer (eine 0 zu viel) ---------------------------
    body = body.replace('tel:+4991039184900', 'tel:+499103918490')

    # --- BUGFIX: YouTube-Einbettung ---------------------------------------
    body = body.replace('allowFullScreen="{{ true }}"', "allowfullscreen")
    body = body.replace("https://www.youtube.com/embed/",
                        "https://www.youtube-nocookie.com/embed/")
    body = body.replace('<iframe src=', '<iframe loading="lazy" src=')

    # --- Parallax auf den Kopfbereich -------------------------------------
    body = re.sub(
        r'<section style="background: var\(--surface-dark\); padding:',
        f'<section class="hero-parallax" '
        f'style="background-image:url(&quot;assets/img/bg/{slug}.jpg&quot;); padding:',
        body, count=1)

    return body

# --------------------------------------------------------------------------
def nav_html(active):
    def a(slug, text, extra=""):
        cur = ' aria-current="page"' if slug == active else ""
        return f'<a class="t-nav hv-primary" href="{SLUG2FILE[slug]}"{cur}{extra}>{text}</a>'

    def group(slug, text, items):
        cur = ' aria-current="page"' if slug == active else ""
        kids = "".join(
            f'<a class="t-nav hv-primary-soft" href="{SLUG2FILE[s]}"'
            + (' aria-current="page"' if s == active else "") + f'>{t}</a>'
            for s, t in items)
        return (f'<div class="nav-group">'
                f'<a class="t-nav hv-primary nav-group__top" href="{SLUG2FILE[slug]}"{cur}>'
                f'{text}<span class="nav-group__chev" aria-hidden="true">›</span></a>'
                f'<div class="nav-drop">{kids}</div></div>')

    return (
        '<a class="ds-btn ds-btn--primary nav-shop" href="https://shop.sms.gmbh" target="_blank" rel="noopener">Shop</a>'
        + group("unternehmen", "Unternehmen",
                [("ueber-uns", "Über uns"), ("historie", "Schmidt Motorsport Historie")])
        + group("engineering", "Engineering",
                [("e-mobilitaet", "E-Mobilität"),
                 ("konstruktion", "Konstruktion und Entwicklung"),
                 ("lehren", "Lehren- und Messmittelbau"),
                 ("sicherheitszellen", "Sicherheitszellen und Stützgestelle")])
        + a("fertigung", "Fertigung")
        + a("messen", "Messen &amp; Prüfen")
        + group("elektro-kart", "Elektro-Kart",
                [("revo-sl", "sms revo SL"), ("revo-x", "sms revo X"),
                 ("spacedrive", "sms revo SpaceDrive"),
                 ("bestellformulare", "Bestellformulare"),
                 ("dokumente", "Wichtige Dokumente")])
        + '<a class="ds-btn ds-btn--primary nav-contact" href="kontakt.html">Kontakt</a>')


def mobile_html(active):
    def row(slug, text, cls="t-title-md"):
        cur = ' aria-current="page"' if slug == active else ""
        return f'<a class="{cls}" href="{SLUG2FILE[slug]}"{cur}>{text}</a>'
    blocks = [
        f'<div class="mnav__block">{row("home", "Start")}</div>',
        '<div class="mnav__block mnav__block--sub"><span class="t-label mnav__head">Unternehmen</span>'
        + row("unternehmen", "Übersicht", "t-body-md") + row("ueber-uns", "Über uns", "t-body-md")
        + row("historie", "Schmidt Motorsport Historie", "t-body-md") + "</div>",
        '<div class="mnav__block mnav__block--sub"><span class="t-label mnav__head">Engineering</span>'
        + row("engineering", "Übersicht", "t-body-md") + row("e-mobilitaet", "E-Mobilität", "t-body-md")
        + row("konstruktion", "Konstruktion und Entwicklung", "t-body-md")
        + row("lehren", "Lehren- und Messmittelbau", "t-body-md")
        + row("sicherheitszellen", "Sicherheitszellen und Stützgestelle", "t-body-md") + "</div>",
        f'<div class="mnav__block">{row("fertigung", "Fertigung")}{row("messen", "Messen &amp; Prüfen")}</div>',
        '<div class="mnav__block mnav__block--sub"><span class="t-label mnav__head">Elektro-Kart</span>'
        + row("elektro-kart", "Übersicht", "t-body-md") + row("revo-sl", "sms revo SL", "t-body-md")
        + row("revo-x", "sms revo X", "t-body-md") + row("spacedrive", "sms revo SpaceDrive", "t-body-md")
        + row("bestellformulare", "Bestellformulare", "t-body-md")
        + row("dokumente", "Wichtige Dokumente", "t-body-md") + "</div>",
        '<a class="ds-btn ds-btn--primary mnav__cta" href="kontakt.html">Kontakt aufnehmen</a>',
    ]
    return "".join(blocks)
