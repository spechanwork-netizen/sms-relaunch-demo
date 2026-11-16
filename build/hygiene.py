# -*- coding: utf-8 -*-
"""Mechanische Korrekturen an den fertigen Seiten. Mehrfach ausfuehrbar.

  python3 -I build/hygiene.py .

1. width/height an jedes <img>. Ohne diese Angaben reserviert der Browser
   keinen Platz und das Layout springt beim Laden nach (CLS).
2. Ueberschriftenstufen: ein Sprung von h1 auf h3 bricht die Gliederung
   fuer Screenreader. Zu tief angesetzte Ueberschriften ruecken eine
   Stufe hoch - oeffnendes und schliessendes Tag zusammen.
"""
import sys, os, re
from PIL import Image
Image.MAX_IMAGE_PIXELS = 300_000_000

SITE = sys.argv[1] if len(sys.argv) > 1 else "."
_cache = {}


def groesse(rel):
    if rel not in _cache:
        try:
            with Image.open(os.path.join(SITE, rel)) as im:
                _cache[rel] = im.size
        except Exception:
            _cache[rel] = None
    return _cache[rel]


def bilder(s):
    n = 0

    def fix(m):
        nonlocal n
        tag = m.group(0)
        if re.search(r'\swidth=', tag):
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        if not src or src.group(1).startswith(("http", "data:")):
            return tag
        g = groesse(src.group(1))
        if not g:
            return tag
        n += 1
        return tag[:-1].rstrip() + f' width="{g[0]}" height="{g[1]}">'
    return re.sub(r'<img\b[^>]*>', fix, s), n


def ueberschriften(s):
    a, b = s.index("<main"), s.index("</main>")
    main = s[a:b]
    stufe, plan = 0, []
    for m in re.finditer(r'<h([1-4])\b', main):
        lvl = int(m.group(1))
        neu = stufe + 1 if (stufe and lvl > stufe + 1) else lvl
        plan.append((m.start(), lvl, neu))
        stufe = neu
    if not any(l != n for _, l, n in plan):
        return s, 0
    out, pos, n = [], 0, 0
    for start, alt, neu in plan:
        schluss = f"</h{alt}>"
        ende = main.index(schluss, start) + len(schluss)
        block = main[start:ende]
        if alt != neu:
            block = re.sub(rf'^<h{alt}\b', f'<h{neu}', block)
            block = re.sub(rf'{re.escape(schluss)}$', f'</h{neu}>', block)
            n += 1
        out += [main[pos:start], block]
        pos = ende
    out.append(main[pos:])
    return s[:a] + "".join(out) + s[b:], n


ni = nh = ns = 0
for f in sorted(os.listdir(SITE)):
    if not f.endswith(".html"):
        continue
    p = os.path.join(SITE, f)
    s = o = open(p, encoding="utf-8").read()
    s, a = bilder(s)
    s, b = ueberschriften(s)
    ni += a; nh += b
    if s != o:
        open(p, "w", encoding="utf-8").write(s); ns += 1
print(f"{ni} Bilder mit Groessenangabe, {nh} Ueberschriften umgestuft, {ns} Seiten geaendert")
