/* sms engineering — Bewegung
   1. Einblenden beim Scrollen (IntersectionObserver, einmalig)
   2. Parallax: Kopfbereich, Kartenbilder, Grossbilder, Anfrage-Band
   3. Kopfleiste: schrumpft, blendet beim Runterscrollen weg
   4. Zahlen zaehlen hoch
   Animiert werden nur transform/opacity. Ein einziger rAF-Takt, ein
   passiver Scroll-Listener, und nur was gerade im Bild ist.
*/
(function () {
  'use strict';

  var root = document.documentElement;
  var reduced = !!(window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  if (!('IntersectionObserver' in window)) { return; }

  root.classList.add('js-motion');
  if (reduced) { return; }          // CSS blendet dann alles statisch ein

  var EASE_OUT = function (t) { return 1 - Math.pow(1 - t, 3); };

  /* --- 1. Einblenden ----------------------------------------------------- */
  var SEL = [
    'main .ds-card', 'main .ds-spec', 'main h1', 'main h2', 'main h3',
    'main p', 'main img', 'main .ds-btn', 'main .ds-link',
    'main li', 'main table', 'main iframe'
  ].join(',');

  var nodes = Array.prototype.slice.call(document.querySelectorAll(SEL));
  // Elemente, die in einem bereits gewaehlten Element stecken, fallen raus -
  // sonst animiert die Karte und ihr Inhalt getrennt.
  var blocks = nodes.filter(function (el) {
    // Formularteile bleiben aussen vor: Felder einzeln einzublenden wirkt
    // zappelig, und Meldungen, die erst spaeter sichtbar werden, bekaemen
    // sonst opacity:0 und blieben unsichtbar.
    if (el.closest('form')) { return false; }
    // Was beim Start keine Flaeche hat, meldet der IntersectionObserver nie
    // als sichtbar - also gar nicht erst verstecken.
    if (el.hidden) { return false; }
    var r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) { return false; }
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i] !== el && nodes[i].contains(el)) { return false; }
    }
    return true;
  });

  var parallaxed = [];          // Elemente, die spaeter Parallax bekommen

  function variantFor(el) {
    if (el.tagName === 'H1') { return 'rise'; }
    if (el.tagName === 'IMG' || el.tagName === 'IFRAME') { return 'scale'; }
    return 'up';
  }

  var groups = new Map();
  blocks.forEach(function (el) {
    var p = el.parentElement || document.body;
    if (!groups.has(p)) { groups.set(p, []); }
    groups.get(p).push(el);
  });
  groups.forEach(function (list) {
    list.forEach(function (el, i) {
      el.setAttribute('data-anim', variantFor(el));
      el.style.setProperty('--d', Math.min(i * 70, 300) + 'ms');
    });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -7% 0px' });

  // Was beim Laden schon im Bild steht, wird direkt eingeblendet. Das ist
  // nicht nur huebscher - ein Element mit clip-path hat fuer den
  // IntersectionObserver die Flaeche null und wuerde sonst nie ausloesen.
  var openNow = [];
  var vh0 = window.innerHeight || 800;
  blocks.forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.top < vh0 * 0.94 && r.bottom > 0) { openNow.push(el); }
    else { io.observe(el); }
  });
  requestAnimationFrame(function () {
    requestAnimationFrame(function () {
      openNow.forEach(function (el) { el.classList.add('is-in'); });
    });
  });

  /* --- 2. Parallax -------------------------------------------------------- */
  var items = [];

  function px(el, apply) {
    if (!el) { return; }
    items.push({ el: el, apply: apply, live: false });
  }

  // Kopfbereich: Inhalt laeuft langsamer als die Seite und blendet aus
  var heroInner = document.querySelector('.hero-parallax > div');
  if (heroInner) {
    heroInner.setAttribute('data-px', 'hero');
    heroInner.removeAttribute('data-anim');
    px(heroInner, function (p) {
      // Minuszeichen: der Inhalt soll der Seite nachlaufen, nicht vorauseilen
      heroInner.style.setProperty('--py', (p * -80).toFixed(1) + 'px');
      var out = Math.min(1, Math.max(0, -p - 0.30) * 1.25);
      heroInner.style.setProperty('--po', (1 - out * 0.88).toFixed(3));
    });
  }

  // Kartenbilder wandern im eigenen Rahmen. Der Rahmen ist noetig: das Bild
  // ist um 8,5 % vergroessert und wuerde sonst ueber den Textbereich
  // darunter malen - das frisst genau den Abstand, der dort hingehoert.
  Array.prototype.forEach.call(
    document.querySelectorAll('.ds-card__photo'), function (img) {
      var frame = document.createElement('span');
      frame.className = 'px-frame';
      img.parentNode.insertBefore(frame, img);
      frame.appendChild(img);
      parallaxed.push(img);
      px(img, function (p) {
        img.style.setProperty('--py', (p * -18).toFixed(1) + 'px');
      });
    });

  // Grossbilder ausserhalb der Karten: sanft, ohne Beschnitt
  Array.prototype.forEach.call(
    document.querySelectorAll('main img:not(.ds-card__photo)'), function (img) {
      if (img.closest('.ds-card')) { return; }
      img.setAttribute('data-anim', 'fade');
      img.setAttribute('data-px', '1');
      parallaxed.push(img);
      px(img, function (p) {
        img.style.setProperty('--py', (p * -14).toFixed(1) + 'px');
      });
    });

  // Anfrage-Band
  var band = document.querySelector('.ds-cta-band__inner');
  if (band) {
    band.setAttribute('data-px', '1');
    px(band, function (p) {
      band.style.setProperty('--py', (p * -26).toFixed(1) + 'px');
    });
  }

  // Parallax nur fuer das, was gerade sichtbar ist
  var pio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      for (var i = 0; i < items.length; i++) {
        if (items[i].el === e.target) { items[i].live = e.isIntersecting; }
      }
    });
    schedule();
  }, { rootMargin: '25% 0px 25% 0px' });
  items.forEach(function (o) { pio.observe(o.el); });

  var ticking = false;
  function schedule() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }
  function update() {
    ticking = false;
    var vh = window.innerHeight || 800;
    for (var i = 0; i < items.length; i++) {
      var o = items[i];
      if (!o.live) { continue; }
      var r = o.el.getBoundingClientRect();
      var p = (r.top + r.height / 2 - vh / 2) / vh;   // 0 = Bildmitte
      if (p < -1.6) { p = -1.6; } else if (p > 1.6) { p = 1.6; }
      o.apply(p);
    }
  }

  /* --- 3. Kopfleiste ------------------------------------------------------ */
  var header = document.querySelector('.site-header');
  var lastY = window.pageYOffset || 0;
  function onScroll() {
    var y = window.pageYOffset || 0;
    if (header) {
      header.classList.toggle('is-scrolled', y > 10);
      var menuOpen = document.body.classList.contains('mnav-open');
      var down = y > lastY + 4;
      var up = y < lastY - 4;
      if (!menuOpen && y > 420 && down) { header.classList.add('is-hidden'); }
      else if (up || y <= 420 || menuOpen) { header.classList.remove('is-hidden'); }
    }
    lastY = y;
    progress();
    schedule();
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });

  /* --- 3b. Lesefortschritt ------------------------------------------------ */
  var bar = document.createElement('div');
  bar.className = 'read-bar';
  bar.setAttribute('aria-hidden', 'true');
  if (header) { header.appendChild(bar); }
  function progress() {
    var doc = document.documentElement;
    var max = (doc.scrollHeight - window.innerHeight) || 1;
    var k = Math.min(1, Math.max(0, (window.pageYOffset || 0) / max));
    bar.style.transform = 'scaleX(' + k.toFixed(4) + ')';
  }

  /* --- 4. Zahlen ----------------------------------------------------------- */
  function animateNumber(el) {
    var raw = (el.textContent || '').trim();
    var m = raw.match(/^(\D*?)([\d][\d.,]*)(\D*)$/);
    if (!m) { return; }
    var pre = m[1], numTxt = m[2], post = m[3];
    var dec = /,\d+$/.test(numTxt) ? numTxt.split(',')[1].length : 0;
    var target = parseFloat(numTxt.replace(/\./g, '').replace(',', '.'));
    if (!isFinite(target) || target <= 0) { return; }
    var grouped = numTxt.indexOf('.') >= 0;
    var t0 = 0, DUR = 1150;
    el.style.minWidth = el.getBoundingClientRect().width + 'px';
    function step(ts) {
      if (!t0) { t0 = ts; }
      var k = Math.min(1, (ts - t0) / DUR);
      var v = target * EASE_OUT(k);
      el.textContent = pre + v.toLocaleString('de-DE', {
        minimumFractionDigits: dec, maximumFractionDigits: dec,
        useGrouping: grouped
      }) + post;
      if (k < 1) { requestAnimationFrame(step); }
      else { el.textContent = raw; el.style.minWidth = ''; }
    }
    requestAnimationFrame(step);
  }

  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { animateNumber(e.target); cio.unobserve(e.target); }
    });
  }, { threshold: 0.6 });
  Array.prototype.forEach.call(
    document.querySelectorAll('.ds-spec__value'), function (el) { cio.observe(el); });

  update();
  progress();
})();
