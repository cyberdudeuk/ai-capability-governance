"""Vaccination tests: every static check passes on the real site and fails on a deliberate break.

Run: python -m unittest discover -s tests
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import check_site  # noqa: E402
import health  # noqa: E402

FILES = ['index.html', 'app.js', 'README.md', 'CHANGELOG.md', 'ACCESSIBILITY.md', 'SECURITY.md', 'CONTRIBUTING.md', 'LICENSE', 'data', '.github', 'docs', '.gitignore']


class Site(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in FILES:
            src = ROOT / f
            if src.is_dir():
                shutil.copytree(src, self.tmp / f)
            elif src.exists():
                shutil.copy(src, self.tmp / f)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, name, old, new):
        p = self.tmp / name
        t = p.read_text(encoding='utf-8')
        self.assertIn(old, t, f'vaccine anchor missing in {name}: {old[:50]}')
        p.write_text(t.replace(old, new, 1), encoding='utf-8')

    def fails_with(self, code):
        found = check_site.problems(self.tmp)
        self.assertTrue(any(x.startswith(code) for x in found), f'{code} did not fail: {found}')

    def test_the_real_site_passes(self):
        self.assertEqual(check_site.problems(ROOT), [])

    def test_S19_doc_points_at_a_pending_pull_request(self):
        self.edit('docs/user-guide/advanced.md', 'function `certify`)', 'function `certify`, in pull request 18 until it merges)')
        self.fails_with('S19')

    def test_S1_email_on_page(self):
        self.edit('index.html', 'AI assurance lead (role, not a named person)', 'someone@example.gov.uk')
        self.fails_with('S1')

    def test_S3_page_out_of_step_with_register(self):
        p = self.tmp / 'data' / 'ai-data-governance-signals.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        d['items'][0]['url'] += 'x'
        p.write_text(json.dumps(d), encoding='utf-8')
        self.fails_with('S3')

    def test_S5_versions_disagree(self):
        # Reads the current version, so a version bump does not break the test (D-16).
        import re
        p = self.tmp / 'index.html'
        t, n = re.subn(r'<span>Version [\d.]+</span>', '<span>Version 0.0.1</span>', p.read_text(encoding='utf-8'))
        self.assertEqual(n, 1)
        p.write_text(t, encoding='utf-8')
        self.fails_with('S5')

    def test_S6_nav_without_target(self):
        self.edit('index.html', '<a href="#signals">Signals</a>', '<a href="#nowhere">Signals</a>')
        self.fails_with('S6')

    def test_S7_missing_issue_form(self):
        (self.tmp / '.github' / 'ISSUE_TEMPLATE' / 'bug_report.yml').unlink()
        self.fails_with('S7')

    def test_S8_email_route_in_script(self):
        self.edit('app.js', "var repoUrl = 'https://github.com/' + PAUT_CONFIG.repo;", "var repoUrl = 'https://github.com/' + PAUT_CONFIG.repo; var x = 'mailto:';")
        self.fails_with('S8')

    def test_S9_old_address(self):
        self.edit('index.html', '<link rel="canonical" href="https://cyberdudeuk.github.io/ai-capability-governance/">', '<link rel="canonical" href="https://cyberdudeuk.github.io/">')
        self.fails_with('S9')

    def test_S10_persona_without_level(self):
        self.edit('index.html', '<article class="card" data-level="beginner"><span class="tag t-ok">Beginner</span>', '<article class="card">')
        self.fails_with('S10')

    def test_S10_task_without_level(self):
        self.edit('index.html', '<span class="tag t-ok">Beginner</span><h3>Decide how much human review my output needs</h3>', '<h3>Decide how much human review my output needs</h3>')
        self.fails_with('S10')

    def test_S11_readme_dead_link(self):
        (self.tmp / 'CHANGELOG.md').unlink()
        self.fails_with('S11')

    def test_S12_unlisted_workflow(self):
        (self.tmp / '.github' / 'workflows' / 'extra.yml').write_text('name: x\n', encoding='utf-8')
        self.fails_with('S12')


    def test_S13_unpinned_pages_action(self):
        # Matches whatever commit the action is pinned to, so a Dependabot update does not break the test (D-14).
        import re
        p = self.tmp / '.github' / 'workflows' / 'pages.yml'
        t, n = re.subn(r'actions/deploy-pages@[0-9a-f]{40}', 'actions/deploy-pages@v4', p.read_text(encoding='utf-8'))
        self.assertEqual(n, 1)
        p.write_text(t, encoding='utf-8')
        self.fails_with('S13')

    def test_S16_duplicate_pin(self):
        p = self.tmp / 'requirements.txt'
        p.write_text((ROOT / 'requirements.txt').read_text(encoding='utf-8') + 'PyYAML==6.0.1\n', encoding='utf-8')
        self.fails_with('S16')

    def test_S17_duplicate_step(self):
        import re
        p = self.tmp / '.github' / 'workflows' / 'pages.yml'
        t = p.read_text(encoding='utf-8')
        line = re.search(r'      - uses: actions/configure-pages@[^\n]+\n', t).group(0)
        p.write_text(t.replace(line, line + line, 1), encoding='utf-8')
        self.fails_with('S17')


    def test_S18_cache_not_ignored(self):
        p = self.tmp / '.gitignore'
        p.write_text(p.read_text(encoding='utf-8').replace('__pycache__/\n', ''), encoding='utf-8')
        self.fails_with('S18')

    def test_S18_cache_tracked(self):
        import subprocess
        for a in (['init', '-q'], ['add', '-A']):
            subprocess.run(['git', '-C', str(self.tmp)] + a, check=True)
        d = self.tmp / 'tools' / '__pycache__'
        d.mkdir(parents=True)
        (d / 'x.cpython-313.pyc').write_bytes(b'\0')
        subprocess.run(['git', '-C', str(self.tmp), 'add', '-f', str(d / 'x.cpython-313.pyc')], check=True)
        self.fails_with('S18')

    def test_S14_truncated_licence(self):
        self.edit('LICENSE', 'Copyright (c) 2026 cyberdudeuk and contributors', 'Copyright (c) 2026 Em')
        self.fails_with('S14')


    def test_S15_signals_section_edited_by_hand(self):
        self.edit('index.html', 'What practitioners and regulators are saying</h2>', 'Hand-edited</h2>')
        self.fails_with('S15')


class Links(unittest.TestCase):
    def test_classification(self):
        import check_links
        self.assertEqual(check_links.classify('https://a/x', '200', 'https://a/x/'), 'ok')
        self.assertEqual(check_links.classify('https://a/x', '404', 'https://a/x'), 'broken')
        self.assertEqual(check_links.classify('https://a/x', '000', 'https://a/x'), 'broken')
        self.assertEqual(check_links.classify('https://a/x', '403', 'https://a/x'), 'blocked')
        self.assertEqual(check_links.classify('https://a/x', '200', 'https://b/y'), 'moved')
        self.assertEqual(check_links.classify('https://a/', '200', 'https://a/docs/intro'), 'ok')
        self.assertEqual(check_links.classify('https://a/', '200', 'https://b/'), 'moved')

    def test_finds_all_68_resource_links(self):
        import check_links
        self.assertEqual(len(check_links.links((ROOT / 'index.html').read_text(encoding='utf-8'))), 68)


class Health(unittest.TestCase):
    HTML = '<meta name="next-review" content="2027-02-08">'

    def test_healthy(self):
        import datetime as dt
        self.assertEqual(health.problems(self.HTML, {'scanned': '2026-11-08', 'pending': []}, dt.date(2026, 11, 10)), [])

    def test_negative_review_past_and_stale_signals(self):
        import datetime as dt
        p = health.problems(self.HTML, {'scanned': '2026-11-08', 'pending': [{}]}, dt.date(2027, 2, 9))
        self.assertTrue(any('review was due' in x for x in p))
        self.assertTrue(any('last scanned' in x for x in p))
        self.assertTrue(any('pending' in x for x in p))


if __name__ == '__main__':
    unittest.main()
