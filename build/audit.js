/* Misst Symmetrie, Rhythmus und typische Fehler auf allen Seiten. */
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = 'http://localhost:8971/';
const SITE = '/home/claude/sms-website';

(async () => {
  const pages = fs.readdirSync(SITE).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch();
  const befunde = [];
  const add = (seite, art, text) => befunde.push({ seite, art, text });

  for (const f of pages) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(BASE + f, { waitUntil: 'networkidle' });
    await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const out = { sektionen: [], probleme: [] };
      const W = innerWidth;

      // --- Symmetrie: linker vs. rechter Rand jedes Inhaltsblocks ---------
      document.querySelectorAll('main > section').forEach((s, i) => {
        const inner = s.firstElementChild;
        const sr = s.getBoundingClientRect();
        const cs = getComputedStyle(s);
        const rec = { i, klasse: s.className || '-', hoehe: Math.round(sr.height),
                      padTop: parseFloat(cs.paddingTop), padBottom: parseFloat(cs.paddingBottom),
                      bg: cs.backgroundColor };
        if (inner && !s.classList.contains('hero-parallax')) {
          const ir = inner.getBoundingClientRect();
          rec.links = Math.round(ir.left);
          rec.rechts = Math.round(W - ir.right);
          rec.breite = Math.round(ir.width);
          if (Math.abs(rec.links - rec.rechts) > 2) {
            out.probleme.push(`Sektion ${i} unsymmetrisch: links ${rec.links}px, rechts ${rec.rechts}px`);
          }
        }
        out.sektionen.push(rec);
      });

      // --- Ueberschriften-Hierarchie ---------------------------------------
      const hs = [...document.querySelectorAll('main h1,main h2,main h3,main h4')]
        .map(h => +h.tagName[1]);
      if (hs.filter(x => x === 1).length !== 1) out.probleme.push(`h1 kommt ${hs.filter(x => x === 1).length}x vor`);
      for (let i = 1; i < hs.length; i++) {
        if (hs[i] - hs[i - 1] > 1) { out.probleme.push(`Ueberschrift springt von h${hs[i-1]} auf h${hs[i]}`); break; }
      }

      // --- doppelte IDs ------------------------------------------------------
      const ids = {};
      document.querySelectorAll('[id]').forEach(e => { ids[e.id] = (ids[e.id] || 0) + 1; });
      Object.entries(ids).filter(([, n]) => n > 1)
        .forEach(([id, n]) => out.probleme.push(`id "${id}" ${n}x vergeben`));

      // --- Bilder ------------------------------------------------------------
      document.querySelectorAll('img').forEach(im => {
        if (!im.alt && im.alt !== '') out.probleme.push(`Bild ohne alt: ${im.src.split('/').pop()}`);
        if (im.naturalWidth && im.clientWidth > im.naturalWidth * 1.6)
          out.probleme.push(`Bild hochskaliert: ${im.src.split('/').pop()} (${im.naturalWidth}px auf ${Math.round(im.clientWidth)}px)`);
        if (!im.getAttribute('width') || !im.getAttribute('height'))
          out.probleme.push(`Bild ohne Groessenangabe (Layoutsprung): ${im.src.split('/').pop()}`);
      });

      // --- Elemente, die aus ihrem Container laufen ---------------------------
      document.querySelectorAll('main *').forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.width === 0) return;
        if (r.right > W + 1 || r.left < -1) {
          const pos = getComputedStyle(e).position;
          if (pos !== 'fixed' && !e.closest('.hero-parallax') && !e.closest('.ds-cta-band'))
            out.probleme.push(`laeuft ueber den Rand: ${e.tagName.toLowerCase()}.${(e.className || '').toString().split(' ')[0]}`);
        }
      });

      // --- leere Links / Buttons ----------------------------------------------
      document.querySelectorAll('a,button').forEach(a => {
        // textContent statt innerText: in einem zugeklappten Menue liefert
        // innerText leeren Text, obwohl eine Beschriftung da ist.
        const t = (a.textContent || '').trim();
        if (!t && !a.getAttribute('aria-label') && !a.querySelector('img'))
          out.probleme.push(`Bedienelement ohne Beschriftung: ${a.tagName.toLowerCase()}`);
      });
      return out;
    });

    // Rhythmus: gleiche vertikale Polsterung?
    const pads = [...new Set(r.sektionen.filter(s => !/hero|cta|legal/.test(s.klasse))
      .map(s => `${s.padTop}/${s.padBottom}`))];
    if (pads.length > 2) add(f, 'Rhythmus', `${pads.length} verschiedene Sektionspolsterungen: ${pads.join('  ')}`);
    const breiten = [...new Set(r.sektionen.map(s => s.breite).filter(Boolean))];
    if (breiten.length > 2) add(f, 'Breite', `${breiten.length} verschiedene Containerbreiten: ${breiten.join(', ')}`);
    [...new Set(r.probleme)].forEach(x => add(f, 'Problem', x));
    await p.close();
  }
  await b.close();

  const nachArt = {};
  befunde.forEach(x => { (nachArt[x.text.replace(/\d+/g, 'N')] ||= []).push(x.seite); });
  console.log(`\n=== ${befunde.length} Befunde auf ${pages.length} Seiten ===\n`);
  Object.entries(nachArt).sort((a, b2) => b2[1].length - a[1].length).forEach(([t, s]) => {
    console.log(`${String(s.length).padStart(3)}x  ${t}`);
    if (s.length <= 4) console.log(`      ${s.join(', ')}`);
  });
})();
