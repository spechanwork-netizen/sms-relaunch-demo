/* Misst Smartphone- und Tabletansicht auf allen Seiten. */
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = 'http://localhost:8971/';
const SITE = '/home/claude/sms-website';
const BREITEN = [
  { w: 360, h: 740, name: 'Handy klein' },
  { w: 390, h: 844, name: 'Handy' },
  { w: 768, h: 1024, name: 'Tablet hoch' },
  { w: 1024, h: 768, name: 'Tablet quer' },
];

(async () => {
  const seiten = fs.readdirSync(SITE).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch();
  const befunde = [];
  for (const bp of BREITEN) {
    const ctx = await b.newContext({ viewport: { width: bp.w, height: bp.h }, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    for (const f of seiten) {
      await p.goto(BASE + f, { waitUntil: 'networkidle' });
      await p.waitForTimeout(250);
      const r = await p.evaluate((vw) => {
        const out = { ueberlauf: [], klein: [], schrift: [], bilder: [], sonst: [] };
        const sichtbar = e => {
          const r = e.getBoundingClientRect();
          return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden';
        };
        // 1. horizontaler Ueberlauf
        if (document.documentElement.scrollWidth > vw + 1) {
          document.querySelectorAll('body *').forEach(e => {
            const r = e.getBoundingClientRect();
            if (r.right > vw + 1 && sichtbar(e) && getComputedStyle(e).position !== 'fixed') {
              out.ueberlauf.push(e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '')
                + ' bis ' + Math.round(r.right) + 'px');
            }
          });
          out.ueberlauf = out.ueberlauf.slice(0, 4);
        }
        // 2. Tippziele
        document.querySelectorAll('a[href], button').forEach(e => {
          if (!sichtbar(e)) return;
          if (e.closest('.mnav') && document.querySelector('.mnav').hidden) return;
          const r = e.getBoundingClientRect();
          if (r.height < 36 || r.width < 24) {
            out.klein.push((e.textContent || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 28)
              + ' ' + Math.round(r.width) + '×' + Math.round(r.height));
          }
        });
        out.klein = [...new Set(out.klein)].slice(0, 6);
        // 3. Schriftgroessen im Fliesstext
        document.querySelectorAll('main p, main li span, footer a, footer p').forEach(e => {
          if (!sichtbar(e)) return;
          const fs = parseFloat(getComputedStyle(e).fontSize);
          if (fs < 14) out.schrift.push(Math.round(fs) + 'px: ' + e.textContent.trim().slice(0, 24));
        });
        out.schrift = [...new Set(out.schrift)].slice(0, 4);
        // 4. Bilder
        document.querySelectorAll('img').forEach(e => {
          if (!sichtbar(e)) return;
          const r = e.getBoundingClientRect();
          if (e.naturalWidth && r.width > e.naturalWidth * 1.35) {
            out.bilder.push(e.src.split('/').pop() + ' ' + e.naturalWidth + ' auf ' + Math.round(r.width));
          }
        });
        out.bilder = [...new Set(out.bilder)].slice(0, 4);
        return out;
      }, bp.w);
      for (const art of Object.keys(r)) {
        for (const t of r[art]) befunde.push({ bp: bp.name + ' ' + bp.w, seite: f, art, text: t });
      }
    }
    await ctx.close();
  }
  await b.close();
  const nach = {};
  for (const x of befunde) {
    const k = x.art + ' | ' + x.bp + ' | ' + x.text;
    (nach[k] = nach[k] || []).push(x.seite);
  }
  const keys = Object.keys(nach).sort();
  for (const k of keys) {
    const s = nach[k];
    console.log(k + '   [' + (s.length > 3 ? s.length + ' Seiten' : s.join(', ')) + ']');
  }
  console.log('\n=== ' + keys.length + ' verschiedene Befunde, ' + befunde.length + ' insgesamt ===');
})();
