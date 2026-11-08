#!/usr/bin/env python3
"""Browser checks (D-10): render the site in Chrome at desktop and phone widths and fail on
- the page scrolling sideways (any width),
- a console error or uncaught exception,
- the contact form not opening the GitHub contact form.

Run: python3 tools/check_browser.py [--break overflow|consoleerror|contact]
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
}


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
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(url, wait_until='load')
            if brk in BREAKS:
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
        code = {'overflow': 'B1', 'consoleerror': 'B2', 'contact': 'B3'}[a.brk]
        ok = any(x.startswith(code) for x in found)
        print(f'Vaccination {a.brk}: {"caught" if ok else "NOT CAUGHT"}')
        return 0 if ok else 1
    print('FAIL\n' + '\n'.join(found) if found else 'PASS: 3 browser checks at 3 widths')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
