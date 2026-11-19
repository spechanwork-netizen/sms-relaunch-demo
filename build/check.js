const SHOTS = process.env.SHOTS || require('os').tmpdir();
const { chromium, devices } = require('playwright');
const fs = require('fs');
const BASE = 'http://localhost:8971/';
const pages = fs.readdirSync('/home/claude/sms-website').filter(f=>f.endsWith('.html') && !f.endsWith('-optionen.html')).sort();

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let errors = [];
  // 1) alle Seiten bei Desktopbreite durchgehen, Konsolen- und Netzwerkfehler sammeln
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  for (const p of pages) {
    const page = await ctx.newPage();
    page.on('console', m => { if (m.type()==='error') errors.push([p,'console',m.text().slice(0,120)]); });
    page.on('pageerror', e => errors.push([p,'js',String(e).slice(0,120)]));
    page.on('requestfailed', r => errors.push([p,'net',r.url().split('/').slice(-1)[0]+' '+(r.failure()||{}).errorText]));
    const resp = await page.goto(BASE+p, { waitUntil:'networkidle' });
    if (!resp || resp.status()!==200) errors.push([p,'http',String(resp&&resp.status())]);
    const info = await page.evaluate(() => {
      // Die Startseite traegt seit dem Entwurf "Buehne" einen eigenen
      // Bildkopf mit Bildlayer statt eines fixierten Hintergrunds.
      const buehne = document.querySelector('.hero-buehne');
      const hero = buehne ? buehne.querySelector('.hero-buehne__bild')
                          : document.querySelector('.hero-parallax');
      const cs = hero ? getComputedStyle(hero) : null;
      return {
        h1: document.querySelectorAll('h1').length,
        heroAtt: cs ? (buehne ? 'fixed' : cs.backgroundAttachment) : null,
        heroImg: cs ? (cs.backgroundImage !== 'none') : null,
        navVisible: getComputedStyle(document.querySelector('.nav')).display !== 'none',
        burgerVisible: getComputedStyle(document.querySelector('.burger')).display !== 'none',
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        imgsBroken: Array.from(document.images).filter(i=>i.complete && i.naturalWidth===0).length,
      };
    });
    if (info.h1!==1) errors.push([p,'h1',info.h1]);
    if (info.heroAtt!=='fixed'||!info.heroImg) errors.push([p,'parallax',info.heroAtt+'/'+info.heroImg]);
    if (!info.navVisible||info.burgerVisible) errors.push([p,'nav@1440',JSON.stringify(info)]);
    if (info.overflow) errors.push([p,'h-overflow@1440','']);
    if (info.imgsBroken) errors.push([p,'bilder',info.imgsBroken]);
    await page.close();
  }
  await ctx.close();

  // 2) Breakpoints + Mobilmenue
  for (const w of [1159, 1160, 900, 390]) {
    const c = await b.newContext({ viewport: { width: w, height: 900 } });
    const page = await c.newPage();
    await page.goto(BASE+'index.html', { waitUntil:'networkidle' });
    const r = await page.evaluate(() => ({
      nav: getComputedStyle(document.querySelector('.nav')).display !== 'none',
      burger: getComputedStyle(document.querySelector('.burger')).display !== 'none',
      overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
    }));
    console.log(`  ${w}px  nav=${r.nav} burger=${r.burger} overflow=${r.overflow}`);
    if (r.nav === r.burger) errors.push(['index','breakpoint@'+w,JSON.stringify(r)]);
    if (r.overflow) errors.push(['index','h-overflow@'+w,'']);
    if (w===390) {
      await page.click('.burger');
      const open = await page.evaluate(()=>({hidden:document.getElementById('mobilmenue').hidden,
        exp:document.querySelector('.burger').getAttribute('aria-expanded'),
        lock:document.body.classList.contains('mnav-open')}));
      console.log('  Mobilmenue nach Klick:', JSON.stringify(open));
      if (open.hidden||open.exp!=='true'||!open.lock) errors.push(['index','mobilmenue',JSON.stringify(open)]);
      await page.screenshot({ path:SHOTS + '/_shot-mobil-menue.png' });
      await page.keyboard.press('Escape');
      const closed = await page.evaluate(()=>document.getElementById('mobilmenue').hidden);
      if (!closed) errors.push(['index','escape','Menue blieb offen']);
    }
    await c.close();
  }

  // 3) Screenshots
  for (const [name,w,h,file] of [['desktop',1440,900,'index.html'],['tablet',900,1200,'engineering.html'],['mobil',390,844,'index.html'],['desktop-kart',1440,900,'elektro-kart.html']]) {
    const c = await b.newContext({ viewport:{width:w,height:h}, deviceScaleFactor: name==='mobil'?2:1 });
    const page = await c.newPage();
    await page.goto(BASE+file, { waitUntil:'networkidle' });
    await page.screenshot({ path:SHOTS + `/_shot-${name}.png`, fullPage: false });
    await c.close();
  }

  console.log('\n=== Befunde: ' + errors.length + ' ===');
  errors.slice(0,30).forEach(e=>console.log('  ', e.join(' | ')));
  await b.close();
})();
