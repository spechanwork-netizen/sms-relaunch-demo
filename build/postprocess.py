#!/usr/bin/env python3
"""Nacharbeit: tote Links auf sms.gmbh ersetzen.

Der Host sms.gmbh antwortet nicht mehr (DNS loest auf, Verbindung wird
abgelehnt). Im Design-Export zeigen aber 13 PDF-Links und 6 Beitragslinks
dorthin - das sind tote Links. Hier entstehen stattdessen lokale
Platzhalter, damit die Seite vollstaendig navigierbar ist und die echten
Dateien spaeter nur ausgetauscht werden muessen.
"""
import os, re, sys, html


def mini_pdf(title, lines):
    """Einseitiges PDF ohne externe Bibliothek."""
    def esc(s):
        return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    content = ["BT", "/F1 20 Tf", "60 760 Td", f"({esc(title)}) Tj", "ET"]
    y = 720
    for ln in lines:
        content += ["BT", "/F1 11 Tf", f"60 {y} Td", f"({esc(ln)}) Tj", "ET"]
        y -= 18
    content += ["0.81 0.12 0.08 rg", "60 790 480 4 re f"]
    stream = "\n".join(content).encode("latin-1", "replace")

    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, o in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n").encode()
    return bytes(out)


ART_HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | sms engineering GmbH</title>
<meta name="description" content="{descr}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>
{header}
<main id="inhalt">
  <section class="hero-parallax" style="background-image:url('assets/img/bg/aktuelles.jpg'); padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 32px)">
    <div style="max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px">
      <span class="t-label" style="color: var(--on-dark-soft)">{eyebrow}</span>
      <h1 class="t-display-xl" style="color: var(--on-dark); font-size: clamp(28px, 3.8vw, 46px); max-width: 900px">{title}</h1>
    </div>
  </section>
  <section class="legal">
    <div class="legal__inner">
      <p class="t-body-md" style="font-size:18px">{excerpt}</p>
      <p class="t-body-md"><strong>Platzhalter.</strong> Der vollständige Beitragstext lag dem Design nicht bei — im Export stand hier nur der Anrisstext und ein Link auf die alte Domain.</p>
      <p><a class="ds-link" href="aktuelles.html">Zurück zu Aktuelles<span class="ds-link__chev" aria-hidden="true">›</span></a></p>
    </div>
  </section>
</main>
"""


def main(site, src_design):
    src = open(src_design, encoding="utf-8").read()
    # „Aktuelles" wurde am 13.11.2026 von der Website genommen. Ohne die
    # Uebersichtsseite gibt es keine Beitragsseiten mehr - die Platzhalter-PDFs
    # weiter unten entstehen aber nach wie vor.
    quelle = os.path.join(site, "aktuelles.html")
    beitraege = os.path.exists(quelle)
    if beitraege:
        idx = open(quelle, encoding="utf-8").read()
        header = idx[idx.index("<header"):idx.index("<main id=")]
        foot = idx[idx.index("</main>"):]

    # ---------- PDFs ----------------------------------------------------
    dl = os.path.join(site, "downloads")
    os.makedirs(dl, exist_ok=True)
    pdfs = sorted(set(re.findall(r'href="(https://sms\.gmbh/[^"]+\.pdf)"', "".join(
        open(os.path.join(site, f), encoding="utf-8").read()
        for f in os.listdir(site) if f.endswith(".html")))))
    for url in pdfs:
        name = url.rsplit("/", 1)[-1]
        open(os.path.join(dl, name), "wb").write(mini_pdf(
            "Platzhalter",
            [name, "",
             "Dieses Dokument ist ein Platzhalter.",
             "Die Originaldatei lag auf sms.gmbh und ist dort",
             "nicht mehr erreichbar.",
             "",
             "Zum Austauschen einfach diese Datei im Ordner",
             "downloads/ durch das echte PDF ersetzen -",
             "der Dateiname muss gleich bleiben.",
             "",
             "sms engineering GmbH, Cadolzburg"]))
    print(f"{len(pdfs)} Platzhalter-PDFs in downloads/")

    # ---------- Beitragsseiten ------------------------------------------
    if not beitraege:
        return
    arts = {}
    for m in re.finditer(r'<x-import[^>]*FeaturePhotoCard"([^>]*)>', src):
        a = dict(re.findall(r'([a-z-]+)="([^"]*)"', m.group(1)))
        href = a.get("href", "")
        if href.startswith("https://sms.gmbh/") and href not in arts:
            arts[href] = (html.unescape(a.get("eyebrow", "Aktuelles")),
                          html.unescape(a.get("title", "Beitrag")),
                          html.unescape(a.get("excerpt", "")))
    # Zusaetzlich der TextLinkCta auf der Fertigungsseite
    arts.setdefault("https://sms.gmbh/neue-fraesmaschine/",
                    ("Maschinenpark", "Neuzugang: 4-Achs-CNC-Fräsmaschine", ""))

    mapping = {}
    for url, (eyebrow, title, excerpt) in arts.items():
        slug = "beitrag-" + url.rstrip("/").rsplit("/", 1)[-1]
        fname = slug + ".html"
        mapping[url] = fname
        open(os.path.join(site, fname), "w", encoding="utf-8").write(
            ART_HEAD.format(title=html.escape(title), descr=html.escape(excerpt[:150] or title),
                            eyebrow=html.escape(eyebrow), excerpt=html.escape(excerpt),
                            header=header)
            + foot)
    print(f"{len(mapping)} Beitragsseiten erzeugt")

    # ---------- Links umschreiben ----------------------------------------
    changed = 0
    for f in os.listdir(site):
        if not f.endswith(".html"):
            continue
        p = os.path.join(site, f)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = re.sub(r'href="https://sms\.gmbh/([^"]+\.pdf)"',
                   lambda m: 'href="downloads/' + m.group(1).rsplit("/", 1)[-1] + '"', s)
        for url, target in mapping.items():
            s = s.replace(f'href="{url}"', f'href="{target}"')
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1
    print(f"{changed} Seiten mit umgeschriebenen Links")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
