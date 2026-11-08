#!/usr/bin/env python3
"""Rebuild the Signals section of index.html from data/ai-data-governance-signals.json.

The register is the master; the section is never edited by hand. check_site.py S15 fails if the page differs from
what this script would write. Run: python3 tools/build_signals.py [--check]
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = {'UK public sector': 't-gov', 'Agent governance': 't-risk', 'Regulation & policy': 't-risk'}
e = html.escape


def section(d):
    cards = []
    for i in d['items']:
        tags = ''.join(f'<span class="tag {TAG.get(t, "")}">{e(t)}</span>' for t in i['themes'])
        ci = '<span class="tag">Commercial interest</span>' if i.get('commercialInterest') else ''
        cards.append(f'''<article class="card"><div class="tags"><span class="tag t-gov">{e(i["id"])}</span><span class="tag">{e(i["region"])}</span>{tags}{ci}</div>
 <h3>{e(i["title"])}</h3>
 <p style="font-size:.9rem;margin:0 0 6px"><strong>{e(i["who"])}</strong>, {e(i["org"])} · {e(i["date"])}</p>
 <p>{e(i["summary"])}</p>
 <p style="font-size:.85rem;margin:0"><strong>Why it matters:</strong> {e(i["relevance"])}</p>
 <p style="font-size:.85rem;margin:0"><strong>Caution:</strong> {e(i["caution"])}</p>
 <p style="font-size:.85rem;margin:6px 0 0"><a href="{e(i["url"])}" rel="noopener noreferrer">Source on LinkedIn<span class="ext visually-hidden"> (opens an external website)</span></a> · evidence: search-indexed text, post not opened</p></article>''')
    n = len(d['items'])
    comm = sum(1 for i in d['items'] if i.get('commercialInterest'))
    return f'''<section id="signals" class="section" aria-labelledby="sec-h-signals">
 <div class="wrap">
  <span class="eyebrow">Horizon scan · AI and data governance</span>
  <h2 id="sec-h-signals">What practitioners and regulators are saying</h2>
  <p class="lede">{n} signals on governing AI agents and the data they use, gathered from public LinkedIn content and refreshed weekly. Each names its author, links to where it was found and says how far it has been checked. Inclusion is not endorsement.</p>
  <div class="callout"><p style="margin:0"><strong>Read with care.</strong> LinkedIn does not allow automated reading of posts, so every summary comes from search-indexed text and is paraphrased. {comm} of {n} come from vendors, consultancies or law firms and are marked. Statistics without a primary source are flagged as unverified. Check the source before you quote anything. The register is open data: <a href="data/ai-data-governance-signals.json">ai-data-governance-signals.json</a> (scanned {e(d["scanned"])}, version {e(d["version"])}).</p></div>
  <div class="grid g2" style="margin-top:18px">
{chr(10).join(cards)}
  </div>
  <p class="count-note">Credit belongs to the named authors. To correct or remove an item, use the contact routes below.</p>
 </div>
</section>'''


def rebuilt(page, d):
    a = page.find('<section id="signals"')
    if a < 0:
        raise ValueError('index.html has no Signals section')
    b = page.find('</section>', a) + len('</section>')
    return page[:a] + section(d) + page[b:]


def main(argv=None):
    p = ROOT / 'index.html'
    page = p.read_text(encoding='utf-8')
    d = json.loads((ROOT / 'data' / 'ai-data-governance-signals.json').read_text(encoding='utf-8'))
    new = rebuilt(page, d)
    if '--check' in (argv or sys.argv[1:]):
        print('Signals section matches the register' if new == page else 'Signals section is out of step: run python3 tools/build_signals.py')
        return 0 if new == page else 1
    p.write_text(new, encoding='utf-8')
    print(f"Signals section rebuilt: {len(d['items'])} items")
    return 0


if __name__ == '__main__':
    sys.exit(main())
