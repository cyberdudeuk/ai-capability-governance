#!/usr/bin/env python3
"""Rebuilds the no-JavaScript copies of the toolkit cards, the resource table and the glossary in index.html from app.js.

app.js draws both from PAUT when the page loads; index.html keeps a copy for anyone without JavaScript and for search
engines. Editing one and not the other made them drift (D-18), so this script writes the copy and check S19 compares
them.

Run: python3 tools/build_static.py           (rewrites index.html)
     python3 tools/build_static.py --check   (exits 1 if index.html is out of date; changes nothing)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = '<span class="ext visually-hidden"> (opens an external website)</span>'


def esc(s):
    return re.sub(r'[<>&]', lambda m: {'<': '&lt;', '>': '&gt;', '&': '&amp;'}[m.group(0)], str(s))


def data(js):
    m = re.search(r'  var PAUT = (\{.*?\});\n', js)
    def table(name):
        return dict(re.findall(r"(\w+): '([^']*)'", re.search(r'var ' + name + r' = \{([^}]*)\}', js).group(1)))
    return json.loads(m.group(1)), table('CAT'), table('EFF'), table('TYPE')


def link(url, text):
    return f'<a href="{url}" rel="noopener noreferrer">{esc(text)}{EXT}</a>'


def cards(d, cat, eff):
    out = []
    for a in d['toolkit']:
        live = '<span class="tag t-ok">Live tool</span>' if a.get('live') else ''
        tool = f'<p style="margin-top:6px"><a class="btn btn-secondary btn-sm" href="{a["live"]}">Open the tool</a></p>' if a.get('live') else ''
        out.append('<article class="card">\n'
                   f'    <div class="tags"><span class="tag t-gov">{a["id"]}</span><span class="tag">{cat[a["cat"]]}</span><span class="tag">{eff[a["eff"]]}</span>{live}</div>\n'
                   f'    <h3>{esc(a["t"])}</h3><p>{esc(a["w"])}</p>\n'
                   f'    <p style="font-size:.85rem;margin:0"><strong>Output:</strong> {esc(a["out"])}</p>\n'
                   '    <p style="font-size:.85rem;margin:0"><strong>Anchored to:</strong> ' + ', '.join(link(u, t) for t, u in a['links']) + '</p>\n'
                   f'    {tool}\n'
                   '  </article>')
    return ''.join(out)


def rows(d, typ):
    tier = {0: 't-risk', 1: 't-gov', 2: 't-ok'}
    out = []
    for r in d['resources']:
        tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r['tags'][:3])
        out.append('<tr>\n'
                   f'   <td>{link(r["u"], r["t"])}<div class="tags" style="margin-top:5px">{tags}</div></td>\n'
                   f'   <td>{esc(r["o"])}</td><td>{typ[r["c"]]}</td><td><span class="tag {tier.get(r["tier"], "")}">Tier {r["tier"]}</span></td><td>{esc(r["w"])}</td></tr>')
    return ''.join(out)


def glossary(d):
    return ''.join(f'<div><dt style="font-weight:700">{esc(g[0])}</dt><dd style="margin:2px 0 0;color:var(--c-text-muted);font-size:.93rem">{esc(g[1])}</dd></div>'
                   for g in d['glossary'])


def build(page, js):
    d, cat, eff, typ = data(js)
    page, a = re.subn(r'(<div class="grid g3" id="tkGrid">).*?(</div>\n  <p class="count-note" id="tkEmpty")',
                      lambda m: m.group(1) + cards(d, cat, eff) + m.group(2), page, count=1, flags=re.S)
    page, b = re.subn(r'(<tbody id="resBody">).*?(</tbody>)', lambda m: m.group(1) + rows(d, typ) + m.group(2), page, count=1, flags=re.S)
    page, c = re.subn(r'(<dl id="glList"[^>]*>).*?(</dl>)', lambda m: m.group(1) + glossary(d) + m.group(2), page, count=1, flags=re.S)
    if (a, b, c) != (1, 1, 1):
        raise SystemExit('build_static: could not find the toolkit grid, resource table or glossary in index.html')
    n = len(d['toolkit'])
    page = re.sub(r'Showing \d+ of \d+ toolkit assets\.', f'Showing {n} of {n} toolkit assets.', page, count=1)
    n = len(d['resources'])
    page = re.sub(r'Showing \d+ of \d+ resources\.', f'Showing {n} of {n} resources.', page, count=1)
    return page


def main(argv):
    p = ROOT / 'index.html'
    old = p.read_text(encoding='utf-8')
    new = build(old, (ROOT / 'app.js').read_text(encoding='utf-8'))
    if '--check' in argv:
        if new != old:
            print('index.html is out of date with app.js: run python3 tools/build_static.py')
            return 1
        print('index.html matches app.js')
        return 0
    p.write_text(new, encoding='utf-8')
    print('index.html rebuilt from app.js')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
