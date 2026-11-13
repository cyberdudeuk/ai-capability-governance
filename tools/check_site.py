#!/usr/bin/env python3
"""Static checks for AI Capability Governance and Implementation. Each check names the defect it guards against
(docs/defect-register.md). tests/test_site.py proves every check fails on a deliberate break.

Run: python3 tools/check_site.py [root]   (exit 1 on any failure)
"""
import html as htmllib
import json
import re
import sys
from pathlib import Path

SITE_URL = 'https://cyberdudeuk.github.io/ai-capability-governance/'
REPO = 'cyberdudeuk/ai-capability-governance'
EXPECTED_WORKFLOWS = {'pages.yml', 'checks.yml', 'release.yml', 'triage.yml', 'digest.yml', 'labels.yml', 'codeql.yml', 'scorecard.yml', 'dependency-review.yml'}
LEVELS = ('beginner', 'intermediate', 'advanced')
EMAIL = re.compile(r'[\w.+-]+@[A-Za-z][\w-]*(\.[\w-]+)*\.[A-Za-z]{2,}\b')


def problems(root):
    root = Path(root)
    s = (root / 'index.html').read_text(encoding='utf-8')
    js = (root / 'app.js').read_text(encoding='utf-8')
    readme = (root / 'README.md').read_text(encoding='utf-8')
    d = json.loads((root / 'data' / 'ai-data-governance-signals.json').read_text(encoding='utf-8'))
    out = []

    def check(ok, msg):
        if not ok:
            out.append(msg)

    # S1 (D-01, 2026-11-08): the worked metadata example published two addresses. Contact is by form only.
    check(not EMAIL.search(s), 'S1 email address in index.html (contact is form only)')
    check(not EMAIL.search(readme.replace('noreply@anthropic.com', '')), 'S1 email address in README.md')
    # S2, S3, S4 (D-02): every signal shown has its author, source link and evidence label, in step with the register.
    ids = [i['id'] for i in d['items']]
    check(len(ids) == len(set(ids)), 'S2 duplicate signal ids')
    for i in d['items']:
        for f in ('title', 'who', 'org', 'url', 'summary', 'caution'):
            check(bool(i.get(f)), f"S2 {i['id']} missing {f}")
        check(htmllib.escape(i['url']) in s, f"S3 {i['id']} source link not on the page (page out of step with register)")
    import build_signals
    for label in {build_signals.evidence(i) for i in d['items']}:
        want = sum(1 for i in d['items'] if build_signals.evidence(i) == label)
        check(s.count('evidence: ' + build_signals.e(label)) == want, f'S4 evidence label "{label}" count does not match register')
    # S5 (D-03): version strings agree across the page, JSON-LD, footer and app.js metadata.
    vers = (set(re.findall(r'<meta name="version" content="([\d.]+)"', s)) | set(re.findall(r'"version": "([\d.]+)"', s))
            | set(re.findall(r'<span>Version ([\d.]+)</span>', s)) | set(re.findall(r'"meta":\{"version":"([\d.]+)"', js)))
    # D-18: CITATION.cff stayed at 3.0.0 after 3.0.1 shipped, because S5 did not look at it or the README.
    cff, rd = root / 'CITATION.cff', root / 'README.md'
    if cff.exists():
        vers |= set(re.findall(r'^version: ([\d.]+)', cff.read_text(encoding='utf-8'), re.M))
    vers |= set(re.findall(r'badge/version-([\d.]+)-', readme)) | set(re.findall(r'\| \*\*Version\*\* \| ([\d.]+),', readme))
    check(len(vers) == 1, f'S5 version strings disagree: {sorted(vers)}')
    # S19 (D-18): the no-JavaScript copies of the toolkit cards and resource table match the data in app.js.
    import build_static
    check(build_static.build(s, js) == s, 'S19 index.html is out of step with app.js: run python3 tools/build_static.py')
    # S6: every in-page navigation link has a target.
    nav = re.findall(r'<nav class="top-nav"[^>]*>(.*?)</nav>', s, re.S)
    check(bool(nav), 'S6 primary navigation not found')
    for m in re.finditer(r'href="#([\w-]+)"', nav[0] if nav else ''):
        check(f'id="{m.group(1)}"' in s, f'S6 nav link #{m.group(1)} has no target')
    # S7 (D-04): the contact links pointed at issue forms that did not exist. Every form linked must exist.
    for t in sorted(set(re.findall(r'issues/new\?template=([\w.-]+\.yml)', s + js + readme))):
        check((root / '.github' / 'ISSUE_TEMPLATE' / t).exists(), f'S7 linked issue form .github/ISSUE_TEMPLATE/{t} does not exist')
    # S8 (D-01): no email route in the script: no mailto and no mailbox setting.
    check('mailto:' not in js and 'mailbox' not in js.lower(), 'S8 app.js still has an email route (mailto or mailbox)')
    # S9 (D-05): after the rename, every self-reference uses the new address and repository.
    for pat in (r'<link rel="canonical" href="([^"]+)"', r'<meta property="og:url" content="([^"]+)"', r'"url": "(https://cyberdudeuk[^"]+)"'):
        found = re.findall(pat, s)
        check(found and all(u == SITE_URL for u in found), f'S9 {pat[:30]}… is not {SITE_URL}: {found}')
    for text, name in ((s, 'index.html'), (js, 'app.js'), (readme, 'README.md')):
        check('cyberdudeuk/cyberdudeuk.github.io' not in text, f'S9 {name} still names the old repository')
    check(f"repo: '{REPO}'" in js, 'S9 app.js PAUT_CONFIG.repo is not the new repository')
    # S10 (D-06): every persona has a level and a journey; every common task has a level.
    grid = re.search(r'<div class="grid g3" id="personaGrid">(.*?)</div>\n\s*<h3 style="margin-top:32px">Common tasks</h3>', s, re.S)
    check(bool(grid), 'S10 persona grid not found')
    cards = re.findall(r'<article class="card"[^>]*>.*?</article>', grid.group(1) if grid else '', re.S)
    check(len(cards) >= 6, f'S10 expected at least 6 personas, found {len(cards)}')
    for c in cards:
        title = re.search(r'<h3>(.*?)</h3>', c)
        t = title.group(1) if title else '?'
        check(re.search(r'data-level="(%s)"' % '|'.join(LEVELS), c) is not None, f'S10 persona "{t}" has no level')
        check('Journey:' in c, f'S10 persona "{t}" has no journey')
        for h in re.findall(r'href="#([\w-]+)"', c):
            check(f'id="{h}"' in s, f'S10 persona "{t}" links to #{h}, which does not exist')
    tasks = re.search(r'<h3 style="margin-top:32px">Common tasks</h3>\s*<div class="grid g3">(.*?)</div>\s*<div class="callout warn"', s, re.S)
    for c in re.findall(r'<a class="card card--link".*?</a>', tasks.group(1) if tasks else '', re.S):
        check(re.search(r'>(Beginner|Intermediate|Advanced)<', c) is not None, 'S10 a common task has no level')
    # S11 (D-07): README pointed to CHANGELOG.md and ACCESSIBILITY.md, which did not exist. Every local link must resolve.
    for link in re.findall(r'\]\((?!https?:|#|mailto:)([^)#\s]+)', readme):
        check((root / link).exists(), f'S11 README links to {link}, which does not exist')
    check(all(f'## {lvl.capitalize()}' in readme for lvl in LEVELS), 'S11 README lacks a Beginner, Intermediate or Advanced section')
    # S13 (D-09): the inherited Pages workflow used actions by moving tag and published the whole repository.
    pw = root / '.github' / 'workflows' / 'pages.yml'
    if pw.exists():
        t = pw.read_text(encoding='utf-8')
        for u in re.findall(r'uses:\s*(\S+)', t):
            check(re.search(r'@[0-9a-f]{40}$', u) is not None, f'S13 pages.yml action not pinned to a full commit: {u}')
        check('path: _site' in t and 'python tools/check_site.py' in t, 'S13 pages.yml must check first and publish only _site')
    # S15 (D-13): the Signals section was written by a one-off script, so a weekly update could drift from the register.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_signals
    check(build_signals.rebuilt(s, d) == s, 'S15 Signals section is out of step with the register: run python3 tools/build_signals.py')
    # S14 (D-12): the licence named its holder as "Em", cut off.
    lic = (root / 'LICENSE').read_text(encoding='utf-8')
    m = re.search(r'Copyright \(c\) \d{4} (.+)', lic)
    check(m is not None and len(m.group(1).strip()) >= 4, 'S14 LICENSE copyright holder is missing or cut off')
    # S16 (D-14): on the launchpad, Dependabot pull requests merged one after another left two pins per package and
    # pip refused to install. One pin per package.
    req = root / 'requirements.txt'
    if req.exists():
        names = [re.split(r'[=<>~!\[ ]', l.strip())[0].lower() for l in req.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
        check(len(names) == len(set(names)), f'S16 requirements.txt pins a package more than once: {sorted({n for n in names if names.count(n) > 1})}')
    # S17 (D-14): the same merges left two copies of the Pages configure and upload steps. One use of an action per job.
    for w in sorted((root / '.github' / 'workflows').glob('*.y*ml')):
        for job in re.split(r'\n  [\w-]+:\n', w.read_text(encoding='utf-8')):
            uses = re.findall(r'uses:\s*([^@\s]+)@', job)
            dup = sorted({u for u in uses if uses.count(u) > 1})
            check(not dup, f'S17 {w.name}: the same action is used twice in one job: {dup}')
    # S18 (D-17): compiled Python caches were committed from 3.0.0 on, and merges conflicted on binary .pyc files.
    # The ignore file must cover them, and git must track none.
    gi = root / '.gitignore'
    ignored = gi.read_text(encoding='utf-8').split() if gi.exists() else []
    check('__pycache__/' in ignored and '*.py[cod]' in ignored, 'S18 .gitignore must list __pycache__/ and *.py[cod]')
    if (root / '.git').exists():
        import subprocess
        tracked = subprocess.run(['git', '-C', str(root), 'ls-files'], capture_output=True, text=True).stdout.split('\n')
        caches = [f for f in tracked if '__pycache__/' in f or f.endswith(('.pyc', '.pyo'))]
        check(not caches, f'S18 git tracks compiled Python caches: {caches[:3]}')
    # S12: the workflow inventory matches the files.
    wf = {p.name for p in (root / '.github' / 'workflows').glob('*.y*ml')} if (root / '.github' / 'workflows').exists() else set()
    check(wf == EXPECTED_WORKFLOWS, f'S12 workflows differ from the inventory: {sorted(wf ^ EXPECTED_WORKFLOWS)}')
    return out


def main(argv=None):
    root = (argv or sys.argv[1:] or ['.'])[0]
    p = problems(root)
    n = len(json.loads((Path(root) / 'data' / 'ai-data-governance-signals.json').read_text(encoding='utf-8'))['items'])
    print('FAIL\n' + '\n'.join(p) if p else f'PASS: 19 checks, {n} signals')
    return 1 if p else 0


if __name__ == '__main__':
    sys.exit(main())
