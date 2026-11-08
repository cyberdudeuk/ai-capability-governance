#!/usr/bin/env python3
"""Health run (tier 0): review date and signals freshness. Prints findings; exit 0 healthy, 2 needs a person.

Run: python3 tools/health.py [--today YYYY-MM-DD]
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNALS_MAX_AGE_DAYS = 14  # the scan is weekly; two missed runs is a problem
REVIEW_WARN_DAYS = 14


def problems(html, signals, today):
    out = []
    m = re.search(r'<meta name="next-review" content="(\d{4}-\d{2}-\d{2})">', html)
    if not m:
        out.append('No next-review date in index.html')
    else:
        due = dt.date.fromisoformat(m.group(1))
        if due <= today:
            out.append(f'Content review was due on {due}; re-verify sources, then update last-reviewed and next-review')
        elif (due - today).days <= REVIEW_WARN_DAYS:
            out.append(f'Content review due on {due} (within {REVIEW_WARN_DAYS} days)')
    scanned = dt.date.fromisoformat(signals['scanned'])
    if (today - scanned).days > SIGNALS_MAX_AGE_DAYS:
        out.append(f'Signals register last scanned {scanned}, more than {SIGNALS_MAX_AGE_DAYS} days ago')
    if signals.get('pending'):
        out.append(f"{len(signals['pending'])} signal(s) pending content from the owner")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--today')
    a = ap.parse_args(argv)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    sig = json.loads((ROOT / 'data' / 'ai-data-governance-signals.json').read_text(encoding='utf-8'))
    p = problems(html, sig, today)
    print('Healthy' if not p else 'Needs attention:\n' + '\n'.join(f'- {x}' for x in p))
    return 2 if p else 0


if __name__ == '__main__':
    sys.exit(main())
