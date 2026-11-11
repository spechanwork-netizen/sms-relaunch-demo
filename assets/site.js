/* sms engineering — Website
   1. Mobilmenue
   2. Parallax-Ersatz fuer iOS
   3. Menuelinks fuehren immer an den Seitenanfang
*/
(function () {
  'use strict';

  /* --- 1. Mobilmenue ---------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var mnav = document.getElementById('mobilmenue');
  var setOpen = null;
  if (burger && mnav) {
    setOpen = function (open) {
      mnav.hidden = !open;
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
      document.body.classList.toggle('mnav-open', open);
    };
    burger.addEventListener('click', function () {
      setOpen(mnav.hidden);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !mnav.hidden) { setOpen(false); burger.focus(); }
    });
    // Beim Wechsel auf Desktopbreite wieder schliessen, sonst bleibt der
    // Scroll-Lock am body haengen.
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1160 && !mnav.hidden) { setOpen(false); }
    });
  }

  /* --- 2. Parallax auf iOS ---------------------------------------------- */
  // WebKit auf iOS rendert background-attachment:fixed nicht als Parallax -
  // Absicht von Apple, kein Fehler. jarallax erzeugt dort stattdessen ein
  // echtes position:fixed-Kindelement. Alle anderen Browser bleiben bei CSS.
  function isIOS() {
    var ua = navigator.userAgent || '';
    if (/iP(hone|od|ad)/.test(ua)) { return true; }
    return navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1;
  }
  function reduced() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function initParallax() {
    if (!isIOS() || reduced() || typeof window.jarallax !== 'function') { return; }
    var els = document.querySelectorAll('.hero-parallax, .ds-cta-band');
    if (els.length) { window.jarallax(els, { speed: 0 }); }
  }
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    initParallax();
  } else {
    document.addEventListener('DOMContentLoaded', initParallax);
  }

  /* --- 3. Menuelinks fuehren an den Seitenanfang ------------------------- */
  // Zwei Faelle, die der Browser von sich aus nicht so loest, wie man es
  // erwartet: ein Klick auf die Seite, auf der man schon steht, tut nichts,
  // und beim Laden stellt der Browser die alte Scrollposition wieder her.
  // Beides wird hier nur fuer Klicks aus Kopf- und Fussbereich abgefangen -
  // der Zurueck-Knopf behaelt sein normales Verhalten.
  var TOP_KEY = 'sms:scroll-top';

  function reducedMotion() {
    return !!(window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function store(v) {
    try { if (v) { sessionStorage.setItem(TOP_KEY, '1'); }
          else { sessionStorage.removeItem(TOP_KEY); } } catch (e) {}
  }
  function wanted() {
    try { return sessionStorage.getItem(TOP_KEY) === '1'; } catch (e) { return false; }
  }
  function toTop(smooth) {
    try { window.scrollTo({ top: 0, left: 0, behavior: smooth ? 'smooth' : 'auto' }); }
    catch (e) { window.scrollTo(0, 0); }
  }
  function samePage(a) {
    return a.pathname === location.pathname && a.search === location.search;
  }

  function onMenuClick(e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || e.defaultPrevented || e.button !== 0) { return; }
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
    if (a.target && a.target !== '_self') { return; }
    if (a.origin !== location.origin) { return; }       // mailto:, tel:, extern
    if (a.hash) { return; }                             // Sprungmarken in Ruhe lassen

    if (samePage(a)) {
      // Schon auf dieser Seite: nicht neu laden, nur nach oben
      e.preventDefault();
      if (mnav && !mnav.hidden && typeof setOpen === 'function') { setOpen(false); }
      toTop(!reducedMotion());
      var main = document.getElementById('inhalt');
      if (main) {
        main.setAttribute('tabindex', '-1');
        try { main.focus({ preventScroll: true }); } catch (err) { main.focus(); }
      }
      return;
    }
    store(true);                                        // naechste Seite oben starten
  }

  ['.site-header', '.mnav', '.site-footer'].forEach(function (sel) {
    var box = document.querySelector(sel);
    if (box) { box.addEventListener('click', onMenuClick); }
  });

  // Beim Ankommen: der Browser stellt die alte Position wieder her, danach
  // sind wir dran. pageshow deckt auch den Vor-/Zurueck-Cache ab.
  function applyTop() {
    if (!wanted()) { return; }
    store(false);
    toTop(false);
    requestAnimationFrame(function () { toTop(false); });
  }
  window.addEventListener('pageshow', applyTop);
  applyTop();

})();
