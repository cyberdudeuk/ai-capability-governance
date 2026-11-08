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

FILES = ['index.html', 'app.js', 'README.md', 'CHANGELOG.md', 'ACCESSIBILITY.md', 'SECURITY.md', 'CONTRIBUTING.md', 'LICENSE', 'data', '.github', 'docs']


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
        self.edit('index.html', '<span>Version 3.0.0</span>', '<span>Version 2.0.0</span>')
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
        self.edit('.github/workflows/pages.yml', 'actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e', 'actions/deploy-pages@v4')
        self.fails_with('S13')


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
