#!/usr/bin/env python3
"""Browser checks (D-10): render the site in Chrome at desktop and phone widths and fail on
- the page scrolling sideways (any width),
- a console error or uncaught exception,
- the contact form not opening the GitHub contact form,
- the playbook page scrolling sideways or erroring (B5), or its route tool giving the wrong route (B6),
- any serious or critical axe-core WCAG 2.2 AA failure on the portal in light or dark mode (B7),
- page search not reaching sections below the hero (B8, D-36), or Escape not closing the menu (B9, D-37),
- the masthead wrapping its menu labels or tagline on a laptop screen (B10, D-39).

Run: python3 tools/check_browser.py [--break overflow|consoleerror|contact|evidence]
--break injects a deliberate fault so CI proves each check fails when it should (a vaccination).
Uses the Chrome installed on the runner (CHROME env var, default /usr/bin/google-chrome); no browser download.
"""
import argparse
import asyncio
import functools
import http.server
import os
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTACT = 'https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=contact.yml'
BREAKS = {
    'overflow': "document.querySelector('#start-here').insertAdjacentHTML('beforeend','<div style=\"width:2000px;height:2px\"></div>')",
    'consoleerror': "console.error('deliberate break')",
    'contact': "document.getElementById('cfIssue').replaceWith(document.getElementById('cfIssue').cloneNode(true))",
    'evidence': "document.getElementById('evGo').replaceWith(document.getElementById('evGo').cloneNode(true))",
    'route': "document.getElementById('routeForm').replaceWith(document.getElementById('routeForm').cloneNode(true))",
    'pboverflow': "document.querySelector('#playbook').insertAdjacentHTML('beforeend','<div style=\"width:2000px;height:2px\"></div>')",
}
PB_BREAKS = {'route', 'pboverflow'}
BREAKS['search'] = "document.getElementById('siteSearch').replaceWith(document.getElementById('siteSearch').cloneNode(true))"
BREAKS['menuescape'] = "document.addEventListener('keydown', e => { if (e.key === 'Escape') e.stopImmediatePropagation(); }, true)"
BREAKS['mastwrap'] = "document.head.insertAdjacentHTML('beforeend','<style>.top-nav a,.nav-group>summary{white-space:normal!important;padding:0 18px!important}</style>')"
BREAKS['contrast'] = "document.querySelector('.btn-primary').style.color = '#d9e5ff'"
AXE = ROOT / 'node_modules' / 'axe-core' / 'axe.min.js'
AXE_RUN = ("async () => (await axe.run(document, {runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}))"
           ".violations.filter(v => v.impact === 'serious' || v.impact === 'critical').map(v => v.id + ' x' + v.nodes.length)")


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


async def run(brk):
    from playwright.async_api import async_playwright
    srv = serve()
    url = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    found = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--no-sandbox'])
        for w, h, name in ((1280, 900, 'desktop'), (390, 844, 'phone'), (320, 640, 'small phone')):
            pg = await b.new_page(viewport={'width': w, 'height': h})
            errs = []
            pg.on('console', lambda m, errs=errs: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
            await pg.goto(url, wait_until='load')
            if brk in BREAKS and brk not in PB_BREAKS and brk != 'contrast':
                await pg.evaluate(BREAKS[brk])
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            if sw > w:
                found.append(f'B1 {name}: page is {sw}px wide on a {w}px screen (scrolls sideways)')
            if errs:
                found.append(f'B2 {name}: console errors: {errs[:3]}')
            if name == 'desktop':
                await pg.evaluate('window.__opened = null; window.open = function (u) { window.__opened = u; return null; }')
                await pg.fill('#cf-subject', 'Check'); await pg.fill('#cf-msg', 'Check')
                await pg.check('#cf-consent'); await pg.click('#cfIssue')
                opened = await pg.evaluate('window.__opened') or ''
                if not opened.startswith(CONTACT):
                    found.append(f'B3 contact form opened {opened[:80] or "nothing"}, not the GitHub contact form')
                # B4: the evidence pack records the data definitions an agent's answer relied on, and only when given.
                await pg.evaluate("document.getElementById('tool-evidence').open = true")
                await pg.click('#evGo')
                empty = await pg.inner_text('#evOut')
                await pg.fill('#ev-defs', 'Household - person_household - unknown')
                await pg.click('#evGo')
                given = await pg.inner_text('#evOut')
                if 'Data definitions relied on' in empty or 'Household' not in given or 'not certified' not in given:
                    found.append('B4 evidence pack does not record the data definitions relied on')
                # B8 (D-36): page search reaches sections below the hero. Each term lives only in a lower section.
                await pg.click('#searchBtn')
                for term in ('toolkit', 'triage', 'roadmap'):
                    await pg.fill('#siteSearch', term)
                    msg = await pg.inner_text('#ssCount')
                    if not msg or msg.startswith('0 '):
                        found.append(f'B8 page search found nothing for "{term}": {msg[:60] or "no answer"}')
                await pg.fill('#siteSearch', '')
                await pg.click('#searchBtn')
            if name == 'phone':
                # B9 (D-37): Escape closes the open menu and hands focus back to the Menu button.
                await pg.click('#navToggle')
                await pg.keyboard.press('Escape')
                state = await pg.evaluate("[navToggle.getAttribute('aria-expanded'), document.activeElement.id]")
                if state != ['false', 'navToggle']:
                    found.append(f'B9 Escape did not close the menu (aria-expanded={state[0]}, focus on #{state[1]})')
            await pg.close()
        # B10 (D-39): on laptop and desktop screens the masthead stays on one line: no menu label or tagline wraps.
        for w in (1180, 1280, 1366, 1440):
            pg = await b.new_page(viewport={'width': w, 'height': 800})
            await pg.goto(url, wait_until='load')
            if brk == 'mastwrap':
                await pg.evaluate(BREAKS[brk])
            m = await pg.evaluate("""(() => ({hdr: document.querySelector('.hdr').getBoundingClientRect().height,
                brand: document.querySelector('.brand').getBoundingClientRect().height,
                tall: [...document.querySelectorAll('.top-nav > a, .nav-group > summary')].filter(e => e.getBoundingClientRect().height > 48).map(e => e.textContent.trim())}))()""")
            if m['hdr'] > 72 or m['brand'] > 44 or m['tall']:
                found.append(f"B10 masthead wraps at {w}px: height {m['hdr']:.0f}px, wrapped {m['tall'][:3] or 'tagline'}")
            await pg.close()
        # The playbook inside the portal (D-29, D-32): no sideways scroll, no console errors, and the route tool answers.
        for w, h, name in ((1280, 900, 'desktop'), (390, 844, 'phone'), (320, 640, 'small phone')):
            pg = await b.new_page(viewport={'width': w, 'height': h})
            errs = []
            pg.on('console', lambda m, errs=errs: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
            await pg.goto(url, wait_until='load')
            if brk in PB_BREAKS:
                await pg.evaluate(BREAKS[brk])
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            if sw > w:
                found.append(f'B5 playbook {name}: page is {sw}px wide on a {w}px screen (scrolls sideways)')
            if errs:
                found.append(f'B5 playbook {name}: console errors: {errs[:3]}')
            if name == 'desktop':
                await pg.click('#tab-tool')
                for i, v in enumerate('nnnyn'):
                    await pg.check(f'input[name="rq{i}"][value="{v}"]')
                got = await pg.inner_text('#routeOut')
                if 'Go ahead with an approved tool' not in got:
                    found.append(f'B6 playbook route tool gave "{got[:60]}" for an approved-tool case')
            await pg.close()
        # B7 (D-30): axe-core finds no serious or critical WCAG 2.2 AA failure on either page, light or dark. Fails closed
        # if axe-core is not installed (CI installs the pinned version).
        if not AXE.exists():
            found.append('B7 axe-core is not installed: npm install --no-save axe-core@4.10.3')
        else:
            for page in ('index.html',):
                for theme in ('light', 'dark'):
                    pg = await b.new_page(viewport={'width': 1280, 'height': 900})
                    await pg.add_init_script(f"try {{ localStorage.setItem('paut.theme', '{theme}') }} catch (e) {{}}")
                    await pg.goto(url.replace('index.html', page), wait_until='load')
                    if brk == 'contrast':
                        await pg.evaluate(BREAKS[brk])
                    await pg.add_script_tag(path=str(AXE))
                    bad = await pg.evaluate(AXE_RUN)
                    if bad:
                        found.append(f'B7 {page} ({theme}): accessibility failures {bad[:4]}')
                    await pg.close()
        await b.close()
    srv.shutdown()
    return found


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--break', dest='brk', choices=sorted(BREAKS))
    a = ap.parse_args(argv)
    found = asyncio.run(run(a.brk))
    if a.brk:
        code = {'overflow': 'B1', 'consoleerror': 'B2', 'contact': 'B3', 'evidence': 'B4', 'route': 'B6', 'pboverflow': 'B5', 'contrast': 'B7', 'search': 'B8', 'menuescape': 'B9', 'mastwrap': 'B10'}[a.brk]
        ok = any(x.startswith(code) for x in found)
        print(f'Vaccination {a.brk}: {"caught" if ok else "NOT CAUGHT"}')
        return 0 if ok else 1
    print('FAIL\n' + '\n'.join(found) if found else 'PASS: 10 browser checks at 3 widths')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
