const { chromium } = require('playwright');
const fs = require('fs');
const BASE = 'http://localhost:8971/';
(async () => {
  const pages = fs.readdirSync('/home/claude/sms-website').filter(f => f.endsWith('.html') && !f.endsWith('-optionen.html'));
  const b = await chromium.launch();
  let bad = [];
  for (const f of pages) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = [];
    p.on('pageerror', e => errs.push('JS: ' + e));
    p.on('console', m => { if (m.type() === 'error' && !/youtube|ERR_TUNNEL/i.test(m.text())) errs.push('CON: ' + m.text()); });
    await p.goto(BASE + f, { waitUntil: 'networkidle' });
    await p.waitForTimeout(900);
    const r = await p.evaluate(async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      const H = document.documentElement;
      const out = { js: H.classList.contains('js-motion') };
      out.anim = document.querySelectorAll('[data-anim]').length;
      // bis ans Ende scrollen, dann pruefen ob alles sichtbar wurde
      const step = Math.round(innerHeight * 0.7);
      for (let y = 0; y <= H.scrollHeight; y += step) { scrollTo(0, y); await sleep(90); }
      await sleep(900);
      out.hidden = [...document.querySelectorAll('[data-anim]')]
        .filter(e => getComputedStyle(e).opacity !== '1').length;
      out.overflow = H.scrollWidth > innerWidth + 1;
      scrollTo(0, 0); await sleep(500);
      out.headerHidden = document.querySelector('.site-header').classList.contains('is-hidden');
      return out;
    });
    if (!r.js) errs.push('js-motion fehlt');
    if (r.hidden > 0) errs.push(r.hidden + ' Element(e) bleiben unsichtbar');
    if (r.overflow) errs.push('horizontaler Ueberlauf');
    if (r.headerHidden) errs.push('Kopfleiste bleibt oben versteckt');
    console.log(`${f.padEnd(60)} anim=${String(r.anim).padStart(3)} ${errs.length ? 'FEHLER' : 'ok'}`);
    errs.forEach(e => { bad.push(f + ' | ' + e); });
    await p.close();
  }
  // Mobil: Menue + Kopfleiste
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await m.goto(BASE + 'index.html', { waitUntil: 'networkidle' });
  await m.waitForTimeout(700);
  await m.evaluate(() => scrollTo(0, 1500)); await m.waitForTimeout(600);
  await m.evaluate(() => scrollTo(0, 1200)); await m.waitForTimeout(600);
  await m.click('.burger'); await m.waitForTimeout(500);
  const mob = await m.evaluate(() => ({
    menuVisible: !document.getElementById('mobilmenue').hidden,
    headerHidden: document.querySelector('.site-header').classList.contains('is-hidden'),
    burgerX: getComputedStyle(document.querySelector('.burger__bars'), '::before').transform,
    lock: getComputedStyle(document.body).overflow
  }));
  console.log('MOBIL', JSON.stringify(mob));
  if (mob.headerHidden) bad.push('mobil | Kopfleiste versteckt, obwohl Menue offen');
  if (!mob.menuVisible) bad.push('mobil | Menue oeffnet nicht');
  await m.screenshot({ path: '/tmp/claude-0/-home-claude/f8f7221a-71d9-5a4b-b86e-e3127c241d72/scratchpad/m-mob.png' });
  await m.close();
  // reduzierte Bewegung
  const r2 = await b.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  await r2.goto(BASE + 'index.html', { waitUntil: 'networkidle' });
  await r2.waitForTimeout(800);
  const red = await r2.evaluate(() => {
    const els = [...document.querySelectorAll('main h1, main h2, main .ds-card')];
    return { n: els.length, hidden: els.filter(e => getComputedStyle(e).opacity !== '1').length,
             anim: document.querySelectorAll('[data-anim]').length };
  });
  console.log('REDUCED', JSON.stringify(red));
  if (red.hidden > 0) bad.push('reduced-motion | ' + red.hidden + ' Element(e) unsichtbar');
  await r2.close();
  await b.close();
  console.log('\n=== Befunde: ' + bad.length + ' ===');
  bad.forEach(x => console.log('   ' + x));
})();
