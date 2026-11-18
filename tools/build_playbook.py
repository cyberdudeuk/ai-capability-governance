#!/usr/bin/env python3
"""Build playbook.html and data/playbook-taxonomy.jsonld from data/playbook.json (D-25).

The playbook page is generated, never edited by hand: check S21 rebuilds it and fails on any difference.
Every string from the data file is escaped on output. Only two inline marks are recognised:
**bold** and [[https://url|link text]]; links must be absolute https URLs or they are dropped to text.

Run: python3 tools/build_playbook.py          (writes the files)
     python3 tools/build_playbook.py --check  (exit 1 if the stored files differ)
"""
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://cyberdudeuk.github.io/ai-capability-governance/'
REPO = 'cyberdudeuk/ai-capability-governance'
URL_OK = re.compile(r'^https://[A-Za-z0-9.-]+(?:/[^\s"\'<>]*)?$')

# Icon sprite: one stroke icon per family. Source icon names map to a family by keyword.
ICONS = {
    'shield': '<path d="M12 3l7 3v6c0 4.4-3 7.6-7 9-4-1.4-7-4.6-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    'people': '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M15 15.2c.6-.2 1.3-.2 2-.2 2.8 0 4 2 4 5"/>',
    'chart': '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-5M12 16V8M16 16v-3"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    'data': '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/>',
    'money': '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9v.01M18 15v.01"/>',
    'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    'lock': '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
    'book': '<path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2z"/><path d="M4 21V5M8 7h7"/>',
    'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    'flag': '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'link': '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
    'robot': '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 16h6"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 2.5 15.3 0 18M12 3c-2.5 2.7-2.5 15.3 0 18"/>',
    'leaf': '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19l7-7"/>',
    'scale': '<path d="M12 4v16M6 20h12M5 8h14"/><path d="M5 8l-3 6a3 3 0 006 0zM19 8l-3 6a3 3 0 006 0z"/>',
    'doc': '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    'star': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    'warn': '<path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17v.01"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>',
    'idea': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 00-3.5 10.9V16h7v-2.1A6 6 0 0012 3z"/>',
    'loop': '<path d="M4 12a8 8 0 0114-5.3L20 9"/><path d="M20 4v5h-5M20 12a8 8 0 01-14 5.3L4 15"/><path d="M4 20v-5h5"/>',
    'access': '<circle cx="12" cy="4.5" r="1.8"/><path d="M5 8l7 1.5L19 8M12 9.5V14l-3 7M12 14l3 7"/>',
    'dot': '<circle cx="12" cy="12" r="4"/>',
}
ICON_MAP = [
    ('shield', 'shield verified policy privacy gavel security crisis emergency'),
    ('check', 'check task fact_check assignment_turned_in done'),
    ('people', 'group person supervisor diversity badge co_present volunteer handshake forum account'),
    ('chart', 'chart insights trending bar_chart timeline monitor_heart speed analytics'),
    ('gear', 'settings tune build extension api router cable deployed apps grid_view'),
    ('data', 'database memory storage inventory receipt label'),
    ('money', 'payments account_balance savings'),
    ('search', 'search travel_explore explore compare'),
    ('lock', 'lock block link_off'),
    ('book', 'menu_book school description history library'),
    ('bolt', 'bolt rocket auto_awesome'),
    ('flag', 'flag signpost campaign door_front target home'),
    ('clock', 'schedule hourglass event update pause'),
    ('link', 'link share hub account_tree group_work'),
    ('robot', 'smart_toy psychology code desktop cloud science'),
    ('globe', 'globe public language'),
    ('leaf', 'eco'),
    ('scale', 'balance scale'),
    ('star', 'star workspace_premium'),
    ('warn', 'warning priority_high error report delete'),
    ('info', 'info help notifications more_horiz sentiment'),
    ('idea', 'lightbulb emoji_objects'),
    ('loop', 'autorenew loop repeat sync'),
    ('access', 'accessibility'),
    ('doc', 'assignment checklist open_in_new add videocam screen_record'),
]
PART_ICONS = ['flag', 'scale', 'gear', 'shield', 'chart', 'money', 'people', 'bolt', 'doc', 'book', 'robot', 'globe']
# Part accents. Light theme uses the colour as given; dark theme lightens it in CSS.
NEW_SINCE = '3.2.0'


def icon_for(name):
    for fam, words in ICON_MAP:
        if any(w in name for w in words.split()):
            return fam
    return 'dot'


def esc(s):
    return html.escape(s or '', quote=True)


def inline(s):
    """Escape a data string, then turn the two permitted marks into markup."""
    out = esc(s)

    def link(m):
        url, text = html.unescape(m.group(1)), m.group(2)
        if not URL_OK.match(url):
            return text
        return (f'<a href="{esc(url)}" rel="noopener noreferrer">{text}'
                '<span class="visually-hidden"> (opens an external website)</span></a>')
    out = re.sub(r'\[\[(.+?)\|(.+?)\]\]', link, out)
    out = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', out)
    return out.replace('**', '')


def svg_icon(fam, cls='pb-ico'):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{fam}"></use></svg>'


class Renderer:
    """Render one chapter body. Heading levels never skip: h4 needs an h4 slot, h5 needs an h4 before it."""

    def __init__(self, title=''):
        self.seen4 = False
        self.title = title
        self.tables = 0

    def heading(self, text, want):
        lvl = 4 if (want <= 4 or not self.seen4) else 5
        if lvl == 4:
            self.seen4 = True
        return f'<h{lvl} class="pb-h">{inline(text)}</h{lvl}>'

    def seq(self, nodes, in_card=False):
        out, i = [], 0
        while i < len(nodes):
            n = nodes[i]
            if isinstance(n, dict) and n.get('t') == 'small':
                run = []
                while i < len(nodes) and isinstance(nodes[i], dict) and nodes[i].get('t') == 'small':
                    run.append(nodes[i]['v'])
                    i += 1
                if len(run) == 1:
                    out.append(f'<p class="pb-small">{inline(run[0])}</p>')
                else:
                    out.append('<ul class="pb-chips">' + ''.join(f'<li>{inline(v)}</li>' for v in run) + '</ul>')
                continue
            out.append(self.node(n, in_card))
            i += 1
        return ''.join(out)

    def node(self, n, in_card=False):
        if isinstance(n, str):
            return f'<p>{inline(n)}</p>'
        if isinstance(n, list):
            return self.seq(n, in_card)
        t = n['t']
        if t == 'h':
            return self.heading(n['v'], 4 if n['l'] <= 2 else 5)
        if t == 'title':
            return self.heading(n['v'], 5) if in_card else f'<p class="pb-title">{inline(n["v"])}</p>'
        if t == 'p':
            return f'<p>{inline(n["v"])}</p>'
        if t == 'eyebrow':
            return f'<p class="pb-eyebrow">{inline(n["v"])}</p>'
        if t == 'num':
            return f'<span class="pb-num">{esc(n["v"])}</span>'
        if t == 'stat':
            return f'<p class="pb-stat">{inline(n["v"])}</p>'
        if t == 'small':
            return f'<p class="pb-small">{inline(n["v"])}</p>'
        if t == 'icon':
            return svg_icon(icon_for(n['v']))
        if t == 'row':
            parts = []
            for it in n['items']:
                if it['t'] == 'icon':
                    parts.append(svg_icon(icon_for(it['v'])))
                else:
                    parts.append(f'<span class="pb-r-{esc(it["t"])}">{inline(it.get("v", ""))}</span>')
            return '<p class="pb-row">' + ' '.join(parts) + '</p>'
        if t == 'grid':
            cols = max(2, min(4, int(n.get('cols', 2))))
            cells = []
            for it in n['items']:
                body = self.seq(it['kids'], True) if isinstance(it, dict) and it.get('t') in ('card', 'group') else self.node(it, True)
                cells.append(f'<div class="pb-card">{body}</div>')
            return f'<div class="pb-grid pb-c{cols}">' + ''.join(cells) + '</div>'
        if t in ('card', 'group'):
            body = self.seq(n['kids'], t == 'card' or in_card)
            return f'<div class="pb-card">{body}</div>' if t == 'card' else body
        if t == 'list':
            tag = 'ol' if n.get('o') else 'ul'
            lis = ''.join(f'<li>{inline(it) if isinstance(it, str) else self.seq(it, in_card)}</li>' for it in n['items'])
            return f'<{tag} class="pb-list">{lis}</{tag}>'
        if t == 'table':
            rows = n['rows']
            head = rows[0] if rows and all(c['h'] for c in rows[0]) else None
            body = rows[1:] if head else rows
            th = ''.join(f'<th scope="col">{inline(c["v"])}</th>' for c in head) if head else ''
            trs = ''.join('<tr>' + ''.join(
                (f'<th scope="row">{inline(c["v"])}</th>' if c['h'] else f'<td>{inline(c["v"])}</td>') for c in r) + '</tr>' for r in body)
            self.tables += 1
            return (f'<div class="pb-table-wrap" tabindex="0" role="region" aria-label="Table {self.tables} in {esc(self.title)}">'
                    f'<table class="pb-table">{"<thead><tr>" + th + "</tr></thead>" if th else ""}<tbody>{trs}</tbody></table></div>')
        raise ValueError(f'unknown node type {t!r}')


def code128(text):
    """Code 128-B as SVG bars (for the colophon barcode). Printable ASCII only."""
    pats = ('212222 222122 222221 121223 121322 131222 122213 122312 132212 221213 221312 231212 112232 122132 122231 '
            '113222 123122 123221 223211 221132 221231 213212 223112 312131 311222 321122 321221 312212 322112 322211 '
            '212123 212321 232121 111323 131123 131321 112313 132113 132311 211313 231113 231311 112133 112331 132131 '
            '113123 113321 133121 313121 211331 231131 213113 213311 213131 311123 311321 331121 312113 312311 332111 '
            '314111 221411 431111 111224 111422 121124 121421 141122 141221 112214 112412 122114 122411 142112 142211 '
            '241211 221114 413111 241112 134111 111242 121142 121241 114212 124112 124211 411212 421112 421211 212141 '
            '214121 412121 111143 111341 131141 114113 114311 411113 411311 113141 114131 311141 411131 211412 211214 '
            '211232 2331112').split()
    codes = [104] + [ord(c) - 32 for c in text]
    chk = (104 + sum(i * v for i, v in enumerate(codes[1:], 1))) % 103
    seq = ''.join(pats[c] for c in codes + [chk]) + pats[106]
    x, bars = 10, []
    for k, w in enumerate(seq):
        w = int(w)
        if k % 2 == 0:
            bars.append(f'<rect x="{x}" y="0" width="{w}" height="40"/>')
        x += w
    return (f'<svg class="pb-barcode" viewBox="0 0 {x + 10} 40" role="img" aria-label="Barcode: {esc(text)}">'
            + ''.join(bars) + '</svg>')


def qr_svg(url):
    import segno
    q = segno.make(url, error='m')
    mat = q.matrix
    n = len(mat)
    rects = ''.join(f'<rect x="{x + 2}" y="{y + 2}" width="1" height="1"/>'
                    for y, row in enumerate(mat) for x, v in enumerate(row) if v)
    return (f'<svg class="pb-qr" viewBox="0 0 {n + 4} {n + 4}" role="img" aria-label="QR code linking to {esc(url)}" '
            f'shape-rendering="crispEdges"><rect width="{n + 4}" height="{n + 4}" fill="#fff"/><g fill="#0b0c0c">{rects}</g></svg>')


def knowledge_map(d):
    """Radial map: parts on an inner ring, their chapters fanned outside. Every node is a link."""
    W = H = 760
    cx = cy = W / 2
    parts = d['parts']
    out = [f'<svg class="pb-map" viewBox="0 0 {W} {H}" role="img" aria-labelledby="mapTitle mapDesc">',
           '<title id="mapTitle">Knowledge map of the playbook</title>',
           f'<desc id="mapDesc">{len(parts)} parts on an inner ring, each linked to its chapters on the outer ring. '
           'The same structure is listed as text in the contents drawer.</desc>',
           f'<circle cx="{cx}" cy="{cy}" r="46" class="pb-map-hub"/>',
           f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" class="pb-map-hubt">Playbook</text>']
    total = sum(len(p['chapters']) for p in parts)
    k = 0
    for i, p in enumerate(parts):
        a = -math.pi / 2 + 2 * math.pi * (k + len(p['chapters']) / 2) / total
        px, py = cx + 175 * math.cos(a), cy + 175 * math.sin(a)
        out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{px:.1f}" y2="{py:.1f}" class="pb-map-edge"/>')
        for cid in p['chapters']:
            b = -math.pi / 2 + 2 * math.pi * (k + .5) / total
            qx, qy = cx + 320 * math.cos(b), cy + 320 * math.sin(b)
            out.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" class="pb-map-edge pb-p{i + 1}"/>')
            title = next(c['title'] for c in d['chapters'] if c['id'] == cid)
            out.append(f'<a href="#ch-{esc(cid)}"><circle cx="{qx:.1f}" cy="{qy:.1f}" r="7" class="pb-map-ch pb-p{i + 1}"/>'
                       f'<title>{esc(title)} ({esc(p["name"])})</title></a>')
            k += 1
        out.append(f'<a href="#part-{esc(p["id"])}"><circle cx="{px:.1f}" cy="{py:.1f}" r="20" class="pb-map-part pb-p{i + 1}"/>'
                   f'<text x="{px:.1f}" y="{py + 5:.1f}" text-anchor="middle" class="pb-map-n">{i + 1}</text>'
                   f'<title>Part {i + 1}: {esc(p["name"])}</title></a>')
    out.append('</svg>')
    legend = ''.join(f'<li><span class="pb-dot pb-p{i + 1}" aria-hidden="true"></span>{i + 1}. <a href="#part-{esc(p["id"])}">{esc(p["name"])}</a> '
                     f'<span class="pb-count">{len(p["chapters"])}</span></li>' for i, p in enumerate(parts))
    return ''.join(out), f'<ol class="pb-legend">{legend}</ol>'


ROUTE_RULES = [
    ('Q1 is Yes', 'Seek advice before going further', 'AI must not make or directly change this kind of decision on its own. Register a use case; it takes the specialist route with a named human decision-maker.', 'red'),
    ('Q5 is Yes', 'Try conventional automation first', 'A rule, form or workflow is usually safer, cheaper and more consistent. Use AI only where judgement over unstructured material is the task.', 'amber'),
    ('Q3 is Yes or Not sure', 'Take the agent route', 'Anything that acts, runs on a schedule or works through steps without you needs an agent design record, approval points and a stop control.', 'red'),
    ('Q1 is Not sure, or Q2 is Yes or Not sure', 'Register a use case', 'Personal or sensitive information, or an unclear impact on people, needs data readiness and privacy screening before use.', 'blue'),
    ('Q4 is Yes', 'Go ahead with an approved tool', "Use it within its approved uses and check its catalogue entry for conditions. Review every output before you rely on it.", 'green'),
    ('Otherwise', 'Check for reuse, then register', "No approved tool is known to fit. Search your organisation's catalogue first; if nothing fits, request a tool through a use case.", 'blue'),
]
ROUTE_QS = [
    "Would the output decide, or directly change, someone’s rights, entitlements, safety or access to a service?",
    'Will you use personal data or information marked OFFICIAL-SENSITIVE or above?',
    'Can the AI take actions, run on a schedule or work through several steps without you?',
    "Is there an approved tool in your organisation's catalogue that already does this?",
    'Could a conventional rule, form or automation do the job reliably?',
]


def route_tool():
    qs = ''.join(
        f'<fieldset class="pb-q"><legend><span class="pb-num">{i + 1}</span> {esc(q)}</legend><div class="pb-opts">'
        + ''.join(f'<label><input type="radio" name="rq{i}" value="{v}"> {lab}</label>' for v, lab in (('y', 'Yes'), ('n', 'No'), ('u', 'Not sure')))
        + '</div></fieldset>' for i, q in enumerate(ROUTE_QS))
    rules = ''.join(f'<tr><th scope="row">{esc(c)}</th><td><span class="pb-tag pb-tag--{k}">{esc(t)}</span></td><td>{esc(d)}</td></tr>'
                    for c, t, d, k in ROUTE_RULES)
    return f'''<div class="pb-tool">
  <form id="routeForm" class="js-only pb-route" novalidate>{qs}
    <div class="pb-route-out" id="routeOut" role="status" aria-live="polite"><p class="pb-title">Answer the five questions</p><p>The route appears when every question has an answer. “Not sure” is a valid answer.</p></div>
    <p><button type="reset" class="btn btn-secondary btn-sm">Start again</button></p>
  </form>
  <h3>How the route is decided</h3>
  <p>The first rule that matches wins. A first sort, not an approval: every route other than an approved tool leads to a registered use case.</p>
  <ol class="pb-list">{"".join(f"<li>{esc(q)}</li>" for q in ROUTE_QS)}</ol>
  <div class="pb-table-wrap" tabindex="0" role="region" aria-label="Route rules"><table class="pb-table"><thead><tr><th scope="col">When</th><th scope="col">Route</th><th scope="col">What it means</th></tr></thead><tbody>{rules}</tbody></table></div>
</div>'''


def build(d):
    meta = d['meta']
    chs = {c['id']: c for c in d['chapters']}
    n_ch, n_parts, n_w = len(d['chapters']), len(d['parts']), len(d['withheld'])
    sprite = ('<svg class="pb-sprite" aria-hidden="true" focusable="false"><defs>'
              + ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
                        f'stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items())
              + '</defs></svg>')
    drawer = []
    body = []
    for i, p in enumerate(d['parts']):
        fam = PART_ICONS[i % len(PART_ICONS)]
        links = ''.join(f'<li><a href="#ch-{esc(c)}" data-ch="{esc(c)}">{esc(chs[c]["title"])}</a></li>' for c in p['chapters'])
        drawer.append(f'<details class="pb-dsec pb-p{i + 1}" open><summary>{svg_icon(fam)}<span class="pb-dname">{esc(p["name"])}</span>'
                      f'<span class="pb-count" aria-label="{len(p["chapters"])} chapters">{len(p["chapters"])}</span>'
                      f'<span class="pb-new" title="New in version {NEW_SINCE}">New</span></summary><ul>{links}</ul></details>')
        cards = []
        for cid in p['chapters']:
            c = chs[cid]
            r = Renderer(c['title'])
            eb = f'<p class="pb-eyebrow">{inline(c["eyebrow"])}</p>' if c.get('eyebrow') else ''
            lede = f'<p class="pb-lede">{inline(c["lede"])}</p>' if c.get('lede') else ''
            cards.append(f'<article class="pb-ch" id="ch-{esc(cid)}" aria-labelledby="h-{esc(cid)}" data-part="{esc(p["id"])}">'
                         f'{eb}<h3 id="h-{esc(cid)}">{svg_icon(icon_for(c.get("icon") or ""), "pb-ico pb-ico--h")}{inline(c["heading"])}</h3>'
                         f'<p class="pb-chmeta">{esc(p["name"])} · {esc(c["title"])}</p>{lede}<div class="pb-body">{r.seq(c["body"])}</div>'
                         f'<p class="pb-chfoot"><a href="#pb-top">Back to the top</a> · <a href="https://github.com/{REPO}/issues/new?template=content_correction.yml" rel="noopener noreferrer">Suggest a correction<span class="visually-hidden"> (opens GitHub)</span></a></p></article>')
        body.append(f'<section class="pb-part pb-p{i + 1}" id="part-{esc(p["id"])}" aria-labelledby="ph-{esc(p["id"])}">'
                    f'<div class="pb-parthead">{svg_icon(fam, "pb-ico pb-ico--part")}<div><p class="pb-eyebrow">Part {i + 1} of {n_parts}</p>'
                    f'<h2 id="ph-{esc(p["id"])}">{esc(p["name"])}</h2><p class="pb-chmeta">{len(p["chapters"])} chapters</p></div></div>'
                    + ''.join(cards) + '</section>')
    mosaic = ''.join(f'<a class="pb-tile pb-p{i + 1}" href="#part-{esc(p["id"])}">{svg_icon(PART_ICONS[i % 12], "pb-ico pb-ico--tile")}'
                     f'<span class="pb-tile-n">Part {i + 1}</span><span class="pb-tile-t">{esc(p["name"])}</span>'
                     f'<span class="pb-tile-c">{len(p["chapters"])} chapters</span></a>' for i, p in enumerate(d['parts']))
    mp, legend = knowledge_map(d)
    withheld = ''.join(f'<tr><th scope="row">{esc(w["title"])}</th><td>{esc(w["part"])}</td><td>{esc(w["reason"])}</td></tr>' for w in d['withheld'])
    cur = ' aria-current="page"'
    nav = ''.join(f'<a href="{h}"{cur if h == "playbook.html" else ""}>{t}</a>' for h, t in (
        ('index.html', 'Home'), ('playbook.html', 'Playbook'), ('index.html#tools', 'Tools'), ('index.html#resources', 'Resources'),
        ('index.html#signals', 'Signals'), ('index.html#transparency', 'Transparency'), ('index.html#contact', 'Contact')))
    jsonld = json.dumps({'@context': 'https://schema.org', '@type': 'Book', 'name': f'{meta["title"]} — {meta["edition"]}',
                         'url': SITE + 'playbook.html', 'inLanguage': 'en-GB', 'version': meta['version'], 'dateModified': meta['published'],
                         'license': 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/', 'isAccessibleForFree': True,
                         'numberOfPages': n_ch, 'hasPart': [{'@type': 'Chapter', 'name': p['name'], 'position': i + 1} for i, p in enumerate(d['parts'])]},
                        ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en-GB" data-theme="light" data-contrast="normal" data-density="normal">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(meta["title"])} — AI Capability Governance and Implementation</title>
  <meta name="description" content="{n_ch} chapters in {n_parts} parts on governing, assuring, funding and operating AI agents in public services, with a working route tool and a knowledge map.">
  <meta name="version" content="{esc(meta["version"])}">
  <meta name="last-reviewed" content="{esc(meta["published"])}">
  <meta name="next-review" content="{esc(meta["nextReview"])}">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{SITE}playbook.html">
  <link rel="alternate" type="application/json" href="data/playbook.json" title="Playbook content (JSON)">
  <link rel="alternate" type="application/ld+json" href="data/playbook-taxonomy.jsonld" title="Playbook taxonomy (SKOS, JSON-LD)">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="playbook.css">
  <script type="application/ld+json">{jsonld}</script>
</head>
<body class="pb">
  {sprite}
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="wrap hdr">
      <a class="brand" href="index.html"><span class="mark" aria-hidden="true">AI</span><span>AI Capability Governance<small>Agent governance playbook</small></span></a>
      <button class="icon-btn nav-toggle js-only" id="navToggle" type="button" aria-expanded="false" aria-controls="primary-nav">☰ Menu</button>
      <nav class="top-nav" id="primary-nav" aria-label="Primary">{nav}</nav>
      <div class="hdr-tools js-only"><button class="icon-btn" id="pbTheme" type="button" aria-pressed="false">Dark mode</button></div>
    </div>
  </header>
  <div class="pb-layout" id="pb-top">
    <aside class="pb-drawer" id="pbDrawer" aria-label="Playbook contents">
      <div class="pb-dtop">
        <button class="pb-switch js-only" id="pbDrawerToggle" type="button" role="switch" aria-checked="true" aria-controls="pbDrawerBody">
          <span class="pb-switch-track" aria-hidden="true"><span class="pb-switch-thumb"></span></span><span class="pb-switch-l">Contents drawer</span></button>
      </div>
      <div class="pb-dbody" id="pbDrawerBody">
        <label class="pb-search js-only" for="pbSearch">{svg_icon("search")}<span class="visually-hidden">Filter chapters</span>
          <input id="pbSearch" type="search" placeholder="Filter {n_ch} chapters" autocomplete="off" maxlength="80"></label>
        <p class="pb-searchres js-only" id="pbSearchRes" role="status" aria-live="polite"></p>
        <nav aria-label="Chapters">{"".join(drawer)}</nav>
      </div>
    </aside>
    <main id="main" tabindex="-1">
      <section class="pb-hero" aria-labelledby="pbH1">
        <p class="eyebrow">{esc(meta["edition"])} · version {esc(meta["version"])} · reviewed {esc(meta["published"])}</p>
        <h1 id="pbH1">{esc(meta["title"])}</h1>
        <p class="lede">One route from “can I use AI for this?” to a governed, monitored and eventually retired AI agent: principles, criticality and tiers, registers and transparency records, oversight, cost and value, people and adoption, a live-pilot method and the delivery documents behind it.</p>
        <ul class="pb-stats" aria-label="At a glance">
          <li><span class="pb-statn" data-count="{n_ch}">{n_ch}</span> public chapters</li>
          <li><span class="pb-statn" data-count="{n_parts}">{n_parts}</span> parts</li>
          <li><span class="pb-statn" data-count="1">1</span> working route tool</li>
          <li><span class="pb-statn" data-count="{n_w}">{n_w}</span> chapters withheld, with reasons</li>
        </ul>
        <div class="actions"><a class="btn btn-primary" href="#tool-route">Can I use AI for this?</a><a class="btn btn-secondary" href="#part-{esc(d["parts"][0]["id"])}">Start reading</a><a class="btn btn-secondary" href="#pb-method">How this edition was made</a></div>
        <p class="pb-note">{svg_icon("info")} {esc(meta["provenance"])}</p>
      </section>
      <div class="pb-tabs js-only" role="tablist" aria-label="Playbook views">
        <button role="tab" id="tab-read" aria-controls="pb-read" aria-selected="true" type="button">{svg_icon("book")} Read</button>
        <button role="tab" id="tab-tool" aria-controls="pb-tool" aria-selected="false" tabindex="-1" type="button">{svg_icon("check")} Route tool</button>
        <button role="tab" id="tab-map" aria-controls="pb-map" aria-selected="false" tabindex="-1" type="button">{svg_icon("link")} Knowledge map</button>
        <button role="tab" id="tab-method" aria-controls="pb-method" aria-selected="false" tabindex="-1" type="button">{svg_icon("shield")} Method and withheld content</button>
      </div>
      <div class="pb-panel" id="pb-read" role="tabpanel" aria-labelledby="tab-read">
        <h2 class="visually-hidden">Read the playbook</h2>
        <div class="pb-mosaic">{mosaic}</div>
        {"".join(body)}
      </div>
      <div class="pb-panel" id="pb-tool" role="tabpanel" aria-labelledby="tab-tool">
        <section id="tool-route" aria-labelledby="h-route"><p class="pb-eyebrow">Working tool</p><h2 id="h-route">Can I use AI for this?</h2>
        <p class="pb-lede">Five questions give a first route. Governance follows what the AI can see, create and do, not which company made it. Nothing you enter leaves your browser.</p>{route_tool()}</section>
      </div>
      <div class="pb-panel" id="pb-map" role="tabpanel" aria-labelledby="tab-map">
        <section aria-labelledby="h-map"><p class="pb-eyebrow">Knowledge map</p><h2 id="h-map">How the playbook fits together</h2>
        <p class="pb-lede">Parts on the inner ring, chapters on the outer ring; select any node to go to it. The taxonomy is published as SKOS in JSON-LD and the full content as JSON, so other portals can harvest it.</p>
        <div class="pb-mapwrap">{mp}{legend}</div>
        <p><a href="data/playbook-taxonomy.jsonld">Taxonomy (SKOS, JSON-LD)</a> · <a href="data/playbook.json">Content (JSON)</a> · <a href="index.html#glossary">Glossary</a></p></section>
      </div>
      <div class="pb-panel" id="pb-method" role="tabpanel" aria-labelledby="tab-method">
        <section aria-labelledby="h-method"><p class="pb-eyebrow">Transparency</p><h2 id="h-method">How this edition was made</h2>
        <p>The source is an internal AI agent governance toolkit of {n_ch + n_w} chapters. Every chapter was rendered, read and classified. {n_ch} are published here; {n_w} are withheld. Published chapters had internal links, internal document names and organisation-specific statuses removed; illustrative figures stay labelled illustrative. The full decision record is in <a href="https://github.com/{REPO}/blob/main/{esc(meta["classification"])}" rel="noopener noreferrer">the content classification<span class="visually-hidden"> (opens GitHub)</span></a>.</p>
        <h3>Withheld chapters</h3>
        <div class="pb-table-wrap" tabindex="0" role="region" aria-label="Withheld chapters"><table class="pb-table"><thead><tr><th scope="col">Chapter</th><th scope="col">Part</th><th scope="col">Why it is withheld</th></tr></thead><tbody>{withheld}</tbody></table></div>
        <h3>Update schedule and how changes are tracked</h3>
        <ul class="pb-list"><li>Reviewed every quarter; next review {esc(meta["nextReview"])}.</li><li>The page is generated from <a href="data/playbook.json">data/playbook.json</a> by <code>tools/build_playbook.py</code>; check S21 fails the build if the two drift.</li>
        <li>Check S22 fails the build if any published file names an internal page, an internal team or an email address.</li>
        <li>Corrections and requests go through <a href="https://github.com/{REPO}/issues/new/choose" rel="noopener noreferrer">GitHub issue forms<span class="visually-hidden"> (opens GitHub)</span></a>; the roadmap and backlog are on the <a href="index.html#roadmap">home page</a>.</li></ul></section>
      </div>
    </main>
  </div>
  <footer class="site-footer">
    <div class="wrap">
      <h2 class="visually-hidden">Site footer</h2>
      <div class="footer-grid">
        <div><h2>Playbook</h2><ul><li><a href="#part-{esc(d["parts"][0]["id"])}">Start reading</a></li><li><a href="#tool-route">Route tool</a></li><li><a href="#pb-map">Knowledge map</a></li><li><a href="#pb-method">Method and withheld content</a></li></ul></div>
        <div><h2>Portal</h2><ul><li><a href="index.html">Home</a></li><li><a href="index.html#tools">Tools</a></li><li><a href="index.html#resources">Resource library</a></li><li><a href="index.html#glossary">Glossary</a></li></ul></div>
        <div><h2>Disclaimers and disclosures</h2><ul><li>Not an official policy position of any department.</li><li>Illustrative figures are labelled illustrative.</li><li>Product names are examples, not endorsements or procurement decisions.</li><li>Built with AI assistance and reviewed against the checks in the repository.</li></ul></div>
        <div><h2>Contact</h2><ul><li><a href="index.html#contact">Contact form</a></li><li><a href="https://github.com/{REPO}/issues/new?template=content_correction.yml" rel="noopener noreferrer">Suggest a correction<span class="visually-hidden"> (opens GitHub)</span></a></li><li><a href="https://github.com/{REPO}/issues/new?template=accessibility_issue.yml" rel="noopener noreferrer">Report an accessibility problem<span class="visually-hidden"> (opens GitHub)</span></a></li></ul></div>
      </div>
      <div class="pb-colophon">
        {qr_svg(SITE + "playbook.html")}
        {code128("AICG-PB-" + meta["version"])}
        <p>Colophon: generated from data/playbook.json · version {esc(meta["version"])} · {esc(meta["published"])} · Open Government Licence v3.0 (content) / MIT (code)</p>
      </div>
      <div class="meta-bar"><span>{esc(meta["title"])} — {esc(meta["edition"])}</span><span>Version {esc(meta["version"])}</span><span>Next review {esc(meta["nextReview"])}</span><a href="#main">Return to main content</a></div>
    </div>
  </footer>
  <script src="playbook.js" defer></script>
</body>
</html>
'''


def taxonomy(d):
    base = SITE + 'playbook.html#'
    graph = [{'@id': base + 'scheme', '@type': 'skos:ConceptScheme', 'skos:prefLabel': {'@value': d['meta']['title'], '@language': 'en-GB'},
              'skos:hasTopConcept': [{'@id': base + 'part-' + p['id']} for p in d['parts']]}]
    for p in d['parts']:
        graph.append({'@id': base + 'part-' + p['id'], '@type': 'skos:Concept', 'skos:prefLabel': {'@value': p['name'], '@language': 'en-GB'},
                      'skos:inScheme': {'@id': base + 'scheme'}, 'skos:topConceptOf': {'@id': base + 'scheme'},
                      'skos:narrower': [{'@id': base + 'ch-' + c} for c in p['chapters']]})
    for c in d['chapters']:
        node = {'@id': base + 'ch-' + c['id'], '@type': 'skos:Concept', 'skos:prefLabel': {'@value': c['title'], '@language': 'en-GB'},
                'skos:inScheme': {'@id': base + 'scheme'}, 'skos:broader': {'@id': base + 'part-' + c['part']}}
        if c.get('lede'):
            node['skos:definition'] = {'@value': re.sub(r'\*\*|\[\[[^|]*\||\]\]', '', c['lede']), '@language': 'en-GB'}
        graph.append(node)
    return json.dumps({'@context': {'skos': 'http://www.w3.org/2004/02/skos/core#'}, '@graph': graph}, ensure_ascii=False, indent=1) + '\n'


def outputs(root=ROOT):
    d = json.loads((root / 'data' / 'playbook.json').read_text(encoding='utf-8'))
    return {root / 'playbook.html': build(d), root / 'data' / 'playbook-taxonomy.jsonld': taxonomy(d)}


def main(argv):
    out = outputs()
    if '--check' in argv:
        stale = [p.name for p, s in out.items() if not p.exists() or p.read_text(encoding='utf-8') != s]
        print('stale: ' + ', '.join(stale) if stale else 'up to date')
        return 1 if stale else 0
    for p, s in out.items():
        p.write_text(s, encoding='utf-8')
    print('wrote ' + ', '.join(p.name for p in out))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
