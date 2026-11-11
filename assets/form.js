/* Kontaktformular.
   Die Seite liegt statisch, es gibt also keinen Server, der die Anfrage
   entgegennimmt. Darum entsteht beim Absenden eine fertig ausgefuellte
   E-Mail. Sobald am <form> ein action gesetzt ist, haelt sich dieses
   Skript heraus und der Browser schickt ganz normal ab.
*/
(function () {
  'use strict';
  var form = document.getElementById('kontaktformular');
  if (!form) { return; }
  var status = document.getElementById('kform-status');

  var TEXTE = {
    thema: 'Bitte wählen Sie ein Thema.',
    name: 'Bitte tragen Sie Ihren Namen ein.',
    email: 'Bitte tragen Sie eine gültige E-Mail-Adresse ein.',
    nachricht: 'Bitte schreiben Sie uns, worum es geht.',
    datenschutz: 'Ohne diese Zustimmung dürfen wir die Anfrage nicht bearbeiten.'
  };

  function melde(feld, text) {
    var box = document.getElementById(feld.id + '-fehler');
    if (!box) { return; }
    if (text) {
      box.textContent = text;
      box.hidden = false;
      feld.setAttribute('aria-invalid', 'true');
      feld.setAttribute('aria-describedby', box.id);
    } else {
      box.hidden = true;
      feld.removeAttribute('aria-invalid');
      feld.removeAttribute('aria-describedby');
    }
  }

  function pruefe(feld) {
    var gut = feld.type === 'checkbox' ? feld.checked : feld.checkValidity();
    melde(feld, gut ? '' : (TEXTE[feld.name] || 'Bitte prüfen Sie diese Angabe.'));
    return gut;
  }

  Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (f) {
    f.addEventListener('blur', function () { pruefe(f); });
    f.addEventListener('input', function () {
      if (f.getAttribute('aria-invalid')) { pruefe(f); }
    });
    f.addEventListener('change', function () {
      if (f.getAttribute('aria-invalid')) { pruefe(f); }
    });
  });

  // Thema aus der Adresszeile vorbelegen: kontakt.html?thema=support
  try {
    var wunsch = new URLSearchParams(location.search).get('thema');
    var thema = form.elements.thema;
    if (wunsch && thema) {
      for (var i = 0; i < thema.options.length; i++) {
        if (thema.options[i].value === wunsch) { thema.selectedIndex = i; break; }
      }
    }
  } catch (e) {}

  form.addEventListener('submit', function (e) {
    if (form.getAttribute('action')) { return; }   // echtes Ziel vorhanden
    e.preventDefault();

    // Honigtopf: ausgefuellt heisst Maschine. Still abbrechen.
    if (form.elements.webseite && form.elements.webseite.value) { return; }

    var fehler = null;
    Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (f) {
      if (!pruefe(f) && !fehler) { fehler = f; }
    });
    if (fehler) {
      status.textContent = 'Bitte ergänzen Sie die markierten Felder.';
      status.className = 'kform__status kform__status--fehler';
      fehler.focus();
      return;
    }

    var w = form.elements;
    var thema = w.thema.options[w.thema.selectedIndex].text;
    var zeilen = [
      'Thema: ' + thema, '',
      'Name: ' + w.name.value,
      w.firma.value ? 'Firma: ' + w.firma.value : null,
      'E-Mail: ' + w.email.value,
      w.telefon.value ? 'Telefon: ' + w.telefon.value : null,
      '', w.nachricht.value
    ].filter(Boolean);

    var ziel = w.thema.value === 'support' || w.thema.value === 'ersatzteile'
      ? 'revo@sms.gmbh' : 'info@sms.gmbh';
    var adresse = 'mailto:' + ziel
      + '?subject=' + encodeURIComponent('Anfrage über die Website: ' + thema)
      + '&body=' + encodeURIComponent(zeilen.join('\n'));

    status.className = 'kform__status kform__status--ok';
    status.textContent = 'Ihr E-Mail-Programm öffnet sich mit der fertigen Nachricht. '
      + 'Falls nicht, schreiben Sie bitte direkt an ' + ziel + '.';
    window.location.href = adresse;
  });
})();
