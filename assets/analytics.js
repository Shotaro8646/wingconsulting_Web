/* 本番サイトだけを計測する。開発・プレビューの閲覧は送信しない。 */
(function () {
  'use strict';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  if (!['wingconsulting.org', 'www.wingconsulting.org'].includes(location.hostname)) return;
  try { if (localStorage.getItem('wing_analytics_off') === '1') return; } catch (_) {}
  var tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=G-KN7NWHFK9G';
  document.head.appendChild(tag);
  gtag('js', new Date());
  /* 問い合わせ内容などがURLに入っても、計測には渡さない。 */
  var page = new URL(location.href);
  var allowed = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];
  Array.from(page.searchParams.keys()).forEach(function (key) {
    if (!allowed.includes(key)) page.searchParams.delete(key);
  });
  page.hash = '';
  gtag('config', 'G-KN7NWHFK9G', { page_location: page.href });

  function ready() {
    document.addEventListener('click', function (event) {
      var link = event.target.closest && event.target.closest('a[href]');
      if (!link) return;
      var dest = new URL(link.href, location.href);
      if (dest.origin === location.origin && dest.hash === '#contact') {
        gtag('event', 'contact_click', { source_path: location.pathname });
      }
    });
    /* 送信後の遷移だけを数える。入力内容は保存・送信しない。 */
    document.querySelectorAll('form[data-netlify]').forEach(function (form) {
      if (new URL(form.action, location.href).pathname !== '/thanks') return;
      form.addEventListener('submit', function (event) {
        if (event.defaultPrevented || !form.checkValidity()) return;
        var trap = form.querySelector('[name="bot-field"]');
        if (trap && trap.value) return;
        try { sessionStorage.setItem('wing_contact_pending', String(Date.now())); } catch (_) {}
      });
    });
    if (/^\/thanks(?:\.html)?\/?$/.test(location.pathname)) {
      try {
        var pending = Number(sessionStorage.getItem('wing_contact_pending'));
        sessionStorage.removeItem('wing_contact_pending');
        if (pending > 0 && Date.now() >= pending && Date.now() - pending < 900000) {
          gtag('event', 'generate_lead', { form_name: 'contact' });
        }
      } catch (_) {}
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
