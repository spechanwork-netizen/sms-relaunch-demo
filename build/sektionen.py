# -*- coding: utf-8 -*-
"""Markiert die Sektionen fuer den Seitenhintergrund. Mehrfach ausfuehrbar.

  python3 -I build/sektionen.py . build/sektionshoehen.json

"float"  Sektion ist seitlich eingerueckt, links und rechts sieht man den
         festen Hintergrund - das ist der Parallax-Effekt beim Scrollen.
"solid"  Sektion laeuft von Rand zu Rand und unterbricht ihn. Gesetzt wird
         das nur, wenn seit der letzten Unterbrechung mehr als BRUCH Pixel
         Inhalt gelaufen sind - kurze Seiten bleiben durchgehend offen.

Die Hintergrundfarbe wandert dabei aus dem Inline-Stil in data-tone, damit
sie im Stylesheet steuerbar ist statt im Markup festzustehen.
"""
import sys, os, re, json

SITE = sys.argv[1]
HOEHEN = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {}
BRUCH = 2600          # Pixel Inhalt, nach denen unterbrochen wird

TON = {"var(--surface-soft)": "soft", "var(--surface-strong)": "strong"}


def tonart(stil):
    m = re.search(r'background:\s*(var\(--surface-(?:soft|strong)\));?\s*', stil)
    if not m:
        return "canvas", stil
    return TON[m.group(1)], stil.replace(m.group(0), "").strip()


n_f = n_s = 0
for f in sorted(os.listdir(SITE)):
    if not f.endswith(".html"):
        continue
    p = os.path.join(SITE, f)
    s = open(p, encoding="utf-8").read()
    a, b = s.index("<main"), s.index("</main>")
    main = s[a:b]
    hoehen = HOEHEN.get(f, [])

    teile, pos, idx, lauf = [], 0, 0, 0
    for m in re.finditer(r'<section\b[^>]*>', main):
        tag = m.group(0)
        teile.append(main[pos:m.start()])
        pos = m.end()
        if "hero-parallax" in tag or "ds-cta-band" in tag:
            teile.append(tag)
            idx += 1
            continue
        # Ein schon gesetztes data-tone gewinnt - beim zweiten Lauf steht
        # die Farbe nicht mehr im Inline-Stil.
        alt_ton = re.search(r'data-tone="([^"]*)"', tag)
        tag = re.sub(r'\sdata-(sec|tone)="[^"]*"', "", tag)
        stil = re.search(r'style="([^"]*)"', tag)
        ton, neu_stil = tonart(stil.group(1)) if stil else ("canvas", "")
        if alt_ton:
            ton = alt_ton.group(1)
        h = hoehen[idx] if idx < len(hoehen) else 900
        # Die letzte Inhaltssektion wird nie zur Unterbrechung - darunter
        # kommt ohnehin das dunkle Anfrage-Band.
        rest = main.count("<section", m.end())
        letzte = rest == 0 or (rest == 1 and "ds-cta-band" in main[m.end():])
        if lauf + h > BRUCH and lauf > 0 and not letzte:
            art, lauf = "solid", 0
            n_s += 1
        else:
            art = "float"
            lauf += h
            n_f += 1
        if stil:
            tag = tag.replace(f'style="{stil.group(1)}"',
                              f'style="{neu_stil}"' if neu_stil else "")
        tag = tag[:-1].rstrip() + f' data-sec="{art}" data-tone="{ton}">'
        tag = re.sub(r'\s{2,}', ' ', tag)
        teile.append(tag)
        idx += 1
    teile.append(main[pos:])
    s = s[:a] + "".join(teile) + s[b:]
    open(p, "w", encoding="utf-8").write(s)
print(f"{n_f} Sektionen offen (Parallax sichtbar), {n_s} als Unterbrechung")
