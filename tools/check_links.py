#!/usr/bin/env python3
"""Link check for the resource library (tier 0, run in the Monday health run). Needs the network.

Classifies every link in the Resources section:
  broken   404, 410 or a 5xx: a person must replace it with the authoritative source's new address
  moved    the link redirects to a different address: a person should update it
  blocked  403 or 429: the site refuses automated checks; not proof the page is gone (check by hand at review)
  ok       200 at the same address
Run: python3 tools/check_links.py   (exit 2 if anything is broken or moved, else 0)
"""
import html
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def links(page):
    a = page.find('<section id="resources"')
    b = page.find('</section>', a)
    return [html.unescape(m.group(1)) for m in re.finditer(r'<a [^>]*href="(https?://[^"]+)"', page[a:b])]


def classify(url, code, final):
    if code in ('404', '410') or code.startswith('5') or code == '000':
        return 'broken'
    if code in ('403', '429'):
        return 'blocked'
    from urllib.parse import urlparse
    u, f = urlparse(url), urlparse(final)
    if u.path in ('', '/') and u.netloc == f.netloc:
        return 'ok'  # a site's front page redirecting within the same site is normal; the front page is the right link
    if final.rstrip('/') != url.rstrip('/'):
        return 'moved'
    return 'ok'


def probe(url):
    r = subprocess.run(['curl', '-sS', '-L', '-o', '/dev/null', '-m', '25', '-A', 'Mozilla/5.0 (link check)',
                        '-w', '%{http_code} %{url_effective}', url], capture_output=True, text=True)
    code, _, final = r.stdout.partition(' ')
    return url, code or '000', final or url


def main():
    urls = sorted(set(links((ROOT / 'index.html').read_text(encoding='utf-8'))))
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(probe, urls))
    found = {'broken': [], 'moved': [], 'blocked': [], 'ok': []}
    for url, code, final in res:
        found[classify(url, code, final)].append((url, code, final))
    print(f"Resource links: {len(urls)} checked; {len(found['ok'])} ok, {len(found['blocked'])} refuse automated checks, "
          f"{len(found['moved'])} moved, {len(found['broken'])} broken")
    for url, code, final in found['broken']:
        print(f'- Broken ({code}): {url}')
    for url, code, final in found['moved']:
        print(f'- Moved: {url} -> {final}')
    return 2 if found['broken'] or found['moved'] else 0


if __name__ == '__main__':
    sys.exit(main())
