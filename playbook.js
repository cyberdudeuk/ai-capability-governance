/*!
 * AI Capability Governance and Implementation — playbook.js
 * Progressive enhancement for playbook.html: every chapter and rule is in the HTML and readable without JavaScript.
 * Adds the drawer switch, chapter filter, tabs, position marker, counters and the route tool.
 * No network calls; nothing typed leaves the browser. Licence: MIT (code) / Open Government Licence v3.0 (content).
 */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k, d) { try { return window.localStorage.getItem('paut.' + k) || d; } catch { return d; } },
    set: function (k, v) { try { window.localStorage.setItem('paut.' + k, v); } catch { /* storage unavailable: keep the default */ } }
  };
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Theme: shared with the home page (same storage key). */
  var THEMES = ['light', 'dark'];
  function setTheme(t) {
    if (THEMES.indexOf(t) < 0) { t = 'light'; }
    doc.setAttribute('data-theme', t);
    var b = $('pbTheme');
    if (b) { b.setAttribute('aria-pressed', String(t === 'dark')); }
  }
  setTheme(store.get('theme', 'light'));
  var contrast = store.get('contrast', 'normal');
  doc.setAttribute('data-contrast', contrast === 'high' ? 'high' : 'normal');
  if ($('pbTheme')) {
    $('pbTheme').addEventListener('click', function () {
      var t = doc.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      setTheme(t); store.set('theme', t);
    });
  }

  /* Masthead menu on narrow screens. */
  var navT = $('navToggle'), nav = $('primary-nav');
  if (navT && nav) {
    navT.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navT.setAttribute('aria-expanded', String(open));
    });
  }

  /* Drawer: a labelled sliding switch retracts it; the choice is remembered. */
  var layout = document.querySelector('.pb-layout'), sw = $('pbDrawerToggle');
  function setDrawer(open) {
    layout.classList.toggle('pb-closed', !open);
    sw.setAttribute('aria-checked', String(open));
  }
  if (layout && sw) {
    setDrawer(store.get('pbDrawer', 'open') !== 'closed');
    sw.addEventListener('click', function () {
      var open = sw.getAttribute('aria-checked') !== 'true';
      setDrawer(open); store.set('pbDrawer', open ? 'open' : 'closed');
    });
  }

  /* Tabs (ARIA Authoring Practices, automatic activation). */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.pb-tabs [role="tab"]'));
  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      $(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) { tab.focus(); }
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t, false); });
    t.addEventListener('keydown', function (e) {
      var j = null;
      if (e.key === 'ArrowRight') { j = (i + 1) % tabs.length; }
      else if (e.key === 'ArrowLeft') { j = (i - 1 + tabs.length) % tabs.length; }
      else if (e.key === 'Home') { j = 0; }
      else if (e.key === 'End') { j = tabs.length - 1; }
      if (j !== null) { e.preventDefault(); select(tabs[j], true); }
    });
  });
  function showTarget() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    if (!/^[\w-]+$/.test(id)) { return; }
    var el = $(id);
    if (!el) { return; }
    var panel = el.closest('[role="tabpanel"]');
    if (panel && panel.hidden) {
      select(tabs.filter(function (t) { return t.getAttribute('aria-controls') === panel.id; })[0], false);
      el.scrollIntoView({ block: 'start' });
    }
  }
  if (tabs.length) {
    select(tabs[0], false);
    showTarget();
    window.addEventListener('hashchange', showTarget);
  }

  /* Chapter filter: plain substring match over each chapter's text. */
  var chapters = Array.prototype.slice.call(document.querySelectorAll('.pb-ch'));
  var index = chapters.map(function (c) { return c.textContent.toLowerCase().replace(/\s+/g, ' '); });
  var links = {};
  Array.prototype.forEach.call(document.querySelectorAll('.pb-dsec a[data-ch]'), function (a) { links[a.getAttribute('data-ch')] = a; });
  var search = $('pbSearch'), res = $('pbSearchRes'), timer = null;
  function filter() {
    var q = (search.value || '').toLowerCase().trim().slice(0, 80);
    var shown = 0;
    chapters.forEach(function (c, i) {
      var hit = !q || index[i].indexOf(q) >= 0;
      c.classList.toggle('pb-hidden', !hit);
      var a = links[c.id.slice(3)];
      if (a) { a.parentNode.classList.toggle('pb-hidden', !hit); }
      if (hit) { shown += 1; }
    });
    Array.prototype.forEach.call(document.querySelectorAll('.pb-part'), function (p) {
      p.classList.toggle('pb-hidden', !p.querySelector('.pb-ch:not(.pb-hidden)'));
    });
    Array.prototype.forEach.call(document.querySelectorAll('.pb-dsec'), function (d) {
      d.classList.toggle('pb-hidden', !d.querySelector('li:not(.pb-hidden)'));
    });
    res.textContent = q ? shown + ' of ' + chapters.length + ' chapters match' : '';
    if (q && tabs.length) { select(tabs[0], false); }
  }
  if (search && res) {
    search.addEventListener('input', function () { window.clearTimeout(timer); timer = window.setTimeout(filter, 150); });
  }

  /* Where am I: mark the chapter in view in the drawer. */
  if ('IntersectionObserver' in window) {
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) { return; }
        var a = links[en.target.id.slice(3)];
        if (!a || a === current) { return; }
        if (current) { current.removeAttribute('aria-current'); }
        a.setAttribute('aria-current', 'location');
        current = a;
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    chapters.forEach(function (c) { io.observe(c); });
  }

  /* Counters: count up once, unless the reader prefers reduced motion. */
  if (!reduced) {
    Array.prototype.forEach.call(document.querySelectorAll('.pb-statn[data-count]'), function (el) {
      var end = parseInt(el.getAttribute('data-count'), 10), start = null;
      if (!(end > 1)) { return; }
      el.textContent = '0';
      var step = function (ts) {
        if (start === null) { start = ts; }
        var p = Math.min(1, (ts - start) / 700);
        el.textContent = String(Math.round(end * p));
        if (p < 1) { window.requestAnimationFrame(step); }
      };
      window.requestAnimationFrame(step);
    });
  }

  /* Route tool. Rules are the table on the page, in the same order: first match wins. */
  var ROUTES = [
    { k: 'red', t: 'Seek advice before going further', d: 'AI must not make or directly change this kind of decision on its own. Register a use case; it takes the specialist route with a named human decision-maker.', go: '#ch-raiassess', cta: 'Classify the use case' },
    { k: 'amber', t: 'Try conventional automation first', d: 'A rule, form or workflow is usually safer, cheaper and more consistent. Use AI only where judgement over unstructured material is the task.', go: '#ch-capclasses', cta: 'Read the capability classes' },
    { k: 'red', t: 'Take the agent route', d: 'Anything that acts, runs on a schedule or works through steps without you needs an agent design record, approval points and a stop control.', go: '#ch-raiagents', cta: 'Open the agent assurance X-ray' },
    { k: 'blue', t: 'Register a use case', d: 'Personal or sensitive information, or an unclear impact on people, needs data readiness and privacy screening before use.', go: '#ch-raiassess', cta: 'Classify the use case' },
    { k: 'green', t: 'Go ahead with an approved tool', d: 'Use it within its approved uses and check its catalogue entry for conditions. Review every output before you rely on it.', go: '#ch-raioperate', cta: 'Read monitoring and reassessment' },
    { k: 'blue', t: 'Check for reuse, then register', d: "No approved tool is known to fit. Search your organisation's catalogue first; if nothing fits, request a tool through a use case.", go: '#ch-registers', cta: 'Read registers and lifecycle' }
  ];
  function route(a) {
    if (a[0] === 'y') { return ROUTES[0]; }
    if (a[4] === 'y') { return ROUTES[1]; }
    if (a[2] !== 'n') { return ROUTES[2]; }
    if (a[0] === 'u' || a[1] !== 'n') { return ROUTES[3]; }
    if (a[3] === 'y') { return ROUTES[4]; }
    return ROUTES[5];
  }
  var form = $('routeForm'), out = $('routeOut');
  function render() {
    var a = [0, 1, 2, 3, 4].map(function (i) {
      var c = form.querySelector('input[name="rq' + i + '"]:checked');
      return c && /^[ynu]$/.test(c.value) ? c.value : null;
    });
    var left = a.filter(function (x) { return x === null; }).length;
    out.textContent = '';
    var h = document.createElement('p'); h.className = 'pb-title';
    var p = document.createElement('p');
    if (left) {
      out.removeAttribute('data-k');
      h.textContent = left === 5 ? 'Answer the five questions' : left + (left > 1 ? ' questions left' : ' question left');
      p.textContent = 'The route appears when every question has an answer. “Not sure” is a valid answer.';
      out.appendChild(h); out.appendChild(p);
      return;
    }
    var r = route(a);
    out.setAttribute('data-k', r.k);
    h.textContent = r.t; p.textContent = r.d;
    var l = document.createElement('a'); l.href = r.go; l.textContent = r.cta;
    out.appendChild(h); out.appendChild(p); out.appendChild(l);
  }
  if (form && out) {
    form.addEventListener('change', render);
    form.addEventListener('reset', function () { window.setTimeout(render, 0); });
    form.addEventListener('submit', function (e) { e.preventDefault(); });
  }
}());
