/* Schreibt je Seite einen Screenshot des Kopfbereichs ohne Text und die
   Textrechtecke als JSON. Die Rechnung macht build/kontrast.py. */
const { chromium } = require('playwright');
const fs = require('fs');
const SITE = '/home/claude/sms-website';
const OUT = process.env.OUT || '/tmp/kontrast';
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const daten = {};
  for (const f of fs.readdirSync(SITE).filter(x => x.endsWith('.html')).sort()) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto('http://localhost:8971/' + f, { waitUntil: 'networkidle' });
    await p.waitForTimeout(450);
    const ziele = await p.evaluate(() => {
      const hero = document.querySelector('.hero-parallax');
      if (!hero) return [];
      return [...hero.querySelectorAll('h1, p, span.t-label, a.ds-btn')].map(e => {
        const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
        return { tag: e.tagName + (e.className ? '.' + String(e.className).split(' ')[0] : ''),
                 x: Math.round(r.left), y: Math.round(r.top),
                 w: Math.round(r.width), h: Math.round(r.height),
                 col: cs.color.match(/\d+/g).slice(0, 3).map(Number),
                 size: parseFloat(cs.fontSize), bold: +cs.fontWeight >= 700,
                 eigenerGrund: cs.backgroundColor !== 'rgba(0, 0, 0, 0)' };
      }).filter(z => z.w > 10 && z.h > 6 && z.y >= 0 && z.y + z.h < 900 && !z.eigenerGrund);
    });
    if (!ziele.length) { await p.close(); continue; }
    await p.addStyleTag({ content: '.hero-parallax h1,.hero-parallax p,.hero-parallax span,.hero-parallax a{color:transparent !important}' });
    await p.waitForTimeout(200);
    await p.screenshot({ path: OUT + '/' + f + '.png' });
    daten[f] = ziele;
    await p.close();
  }
  fs.writeFileSync(OUT + '/ziele.json', JSON.stringify(daten));
  await b.close();
  console.log(Object.keys(daten).length + ' Kopfbereiche aufgenommen');
})();
