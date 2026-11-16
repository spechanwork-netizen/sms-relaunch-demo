const { chromium } = require('playwright');
const B = 'http://localhost:8971/';
const last = u => u.split('/').pop();
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  const Y = () => p.evaluate(() => Math.round(scrollY));
  const out = [];

  await p.goto(B + 'index.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => scrollTo(0, 2000)); await p.waitForTimeout(400);
  const y1a = await Y();
  await Promise.all([p.waitForLoadState('networkidle'),
                     p.click('.site-header .nav a[href="fertigung.html"]')]);
  await p.waitForTimeout(800);
  out.push(['Kopfmenue -> andere Seite', `${y1a} -> ${last(p.url())} y=${await Y()}`]);

  await p.evaluate(() => scrollTo(0, 1800)); await p.waitForTimeout(400);
  const y2a = await Y();
  await p.click('.site-header .nav a[href="fertigung.html"]');
  await p.waitForTimeout(1300);
  out.push(['Kopfmenue -> gleiche Seite', `${y2a} -> y=${await Y()} url=${last(p.url())}`]);

  await p.evaluate(() => scrollTo(0, 2200)); await p.waitForTimeout(400);
  await Promise.all([p.waitForLoadState('networkidle'),
                     p.click('.site-footer a[href="messen.html"]')]);
  await p.waitForTimeout(800);
  out.push(['Fussbereich -> andere Seite', `${last(p.url())} y=${await Y()}`]);

  await p.evaluate(() => scrollTo(0, 1200)); await p.waitForTimeout(400);
  await Promise.all([p.waitForLoadState('networkidle'), p.goBack()]);
  await p.waitForTimeout(1000);
  out.push(['Zurueck-Knopf (soll NICHT 0 sein)', `${last(p.url())} y=${await Y()}`]);

  // Inhaltslink mitten auf der Seite soll unberuehrt bleiben
  await p.goto(B + 'index.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => scrollTo(0, 1500)); await p.waitForTimeout(300);
  const inl = await p.$('main a[href$=".html"]');
  if (inl) {
    await Promise.all([p.waitForLoadState('networkidle'), inl.click()]);
    await p.waitForTimeout(700);
    out.push(['Inhaltslink (Browser-Normalfall)', `${last(p.url())} y=${await Y()}`]);
  }

  // Mobil: Menue oeffnen, Link klicken
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  m.on('pageerror', e => errs.push('mobil: ' + e));
  await m.goto(B + 'index.html', { waitUntil: 'networkidle' });
  await m.evaluate(() => scrollTo(0, 1600)); await m.waitForTimeout(400);
  await m.click('.burger'); await m.waitForTimeout(400);
  await Promise.all([m.waitForLoadState('networkidle'),
                     m.click('.mnav a[href="fraesen.html"]')]);
  await m.waitForTimeout(800);
  out.push(['Mobilmenue -> Seite', `${last(m.url())} y=${await m.evaluate(() => Math.round(scrollY))} ` +
    `lock=${await m.evaluate(() => getComputedStyle(document.body).overflow)}`]);
  // gleiche Seite aus dem Mobilmenue
  await m.evaluate(() => scrollTo(0, 900)); await m.waitForTimeout(300);
  await m.click('.burger'); await m.waitForTimeout(400);
  await m.click('.mnav a[href="fraesen.html"]');
  await m.waitForTimeout(1300);
  out.push(['Mobilmenue -> gleiche Seite', `y=${await m.evaluate(() => Math.round(scrollY))} ` +
    `menueOffen=${await m.evaluate(() => !document.getElementById('mobilmenue').hidden)} ` +
    `lock=${await m.evaluate(() => getComputedStyle(document.body).overflow)}`]);
  await m.close();

  out.forEach(([k, v]) => console.log(k.padEnd(36) + v));
  console.log('Fehler: ' + (errs.length ? errs.join(' | ') : 'keine'));
  await b.close();
})();
