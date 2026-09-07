/* ckservice.be — consent banner (Consent Mode v2), measurement, form helpers. No dependencies. */
(function () {
  'use strict';
  var KEY = 'ck_consent_v1';
  var PIXEL_ID = '2483986251880768';
  function gtag() { window.dataLayer = window.dataLayer || []; window.dataLayer.push(arguments); }

  function loadPixel() {
    if (window.fbq) return;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PIXEL_ID); window.fbq('track', 'PageView');
  }

  function applyConsent(choice) {
    var granted = choice === 'all';
    gtag('consent', 'update', {
      ad_storage: granted ? 'granted' : 'denied', ad_user_data: granted ? 'granted' : 'denied',
      ad_personalization: granted ? 'granted' : 'denied', analytics_storage: granted ? 'granted' : 'denied'
    });
    window.dataLayer.push({ event: 'ck_consent', ck_consent: choice });
    if (granted) loadPixel();
  }

  function banner() {
    var el = document.createElement('div');
    el.className = 'ck-consent'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Cookies');
    el.innerHTML = '<div class="ck-consent__box"><p><strong>Cookies?</strong> We gebruiken cookies om te meten hoe onze website gebruikt wordt en om onze advertenties beter af te stemmen. Kies gerust zelf. <a href="/cookiebeleid/">Meer over ons cookiebeleid</a>.</p><div class="ck-consent__actions"><button type="button" class="btn" data-choice="all">Alles aanvaarden</button><button type="button" class="btn btn--ghost" data-choice="necessary">Enkel noodzakelijk</button></div></div>';
    el.addEventListener('click', function (e) {
      var c = e.target && e.target.getAttribute && e.target.getAttribute('data-choice');
      if (!c) return;
      try { localStorage.setItem(KEY, c); } catch (err) {}
      applyConsent(c); el.remove();
    });
    document.body.appendChild(el);
  }

  function initConsent() {
    var stored = null; try { stored = localStorage.getItem(KEY); } catch (e) {}
    if (stored === 'all' || stored === 'necessary') { applyConsent(stored); } else { banner(); }
    var links = document.querySelectorAll('[data-consent-reset]');
    for (var i = 0; i < links.length; i++) links[i].addEventListener('click', function (e) { e.preventDefault(); try { localStorage.removeItem(KEY); } catch (err) {} banner(); });
  }

  function param(name) { try { return new URL(window.location.href).searchParams.get(name) || ''; } catch (e) { return ''; } }

  function initForms() {
    var forms = document.querySelectorAll('form[action="/api/lead"]');
    for (var i = 0; i < forms.length; i++) (function (f) {
      var set = function (n, v) { var el = f.querySelector('input[name="' + n + '"]'); if (el) el.value = v; };
      set('t0', String(Date.now()));
      set('page', window.location.pathname);
      set('referrer', document.referrer || '');
      ['gclid', 'wbraid', 'gbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach(function (k) {
        var v = param(k); if (!v) { try { v = sessionStorage.getItem('ck_' + k) || ''; } catch (e) {} } else { try { sessionStorage.setItem('ck_' + k, v); } catch (e) {} }
        if (v) set(k, v);
      });
      f.addEventListener('submit', function () {
        var b = f.querySelector('button[type="submit"]'); if (b) { b.disabled = true; b.textContent = 'Even geduld…'; }
        window.dataLayer = window.dataLayer || []; window.dataLayer.push({ event: 'ck_form_submit', form_interest: (f.querySelector('[name="dienst"], [name="interesse"]') || {}).value || '' });
      });
    })(forms[i]);
    if (param('fout') === '1') {
      var msg = document.querySelector('.ck-form-error'); if (msg) msg.hidden = false;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initConsent(); initForms(); });
  else { initConsent(); initForms(); }
})();
