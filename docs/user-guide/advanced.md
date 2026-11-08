# Advanced guide

For you if you build, assure, integrate or reuse this guidance, including in code.

## Reuse the content and data

- The page is one HTML file; every piece of content is readable without JavaScript.
- `data/ai-data-governance-signals.json` is the open signals register (also on the page as schema.org JSON-LD).
- The [metadata schema](https://cyberdudeuk.github.io/ai-capability-governance/#catalogue) has a worked YAML example for any AI asset.
- Content is under the Open Government Licence v3.0; code under MIT.

## How the repository works

| Path | What it is |
|---|---|
| `index.html`, `styles.css`, `app.js` | The site. The publish workflow deploys it after every check passes |
| `data/` | Open data the page is built from |
| `tools/check_site.py` | 15 static checks; each names the defect it prevents |
| `tools/check_browser.py` | Browser checks in Chrome at 1280, 390 and 320px: no sideways scroll, no console errors, contact form opens the GitHub form |
| `tools/build_signals.py` | Rebuilds the Signals section from the register; never edit that section by hand |
| `tools/health.py` | Weekly health run: review date and signals freshness |
| `tools/digest.py`, `tools/triage.py`, `tools/trials.py` | Estate routines (reports and labels only) |
| `tests/` | Vaccination tests: every check must fail on a deliberate break |
| `ops/automation.yaml` | What runs, when, its tier and what it may change |
| `docs/` | Decisions (ADRs), the defect register, settings checklist and these guides |

## Build and check locally

```
pip install -r requirements.txt
python3 tools/check_site.py
python3 -m unittest discover -s tests -v
node --check app.js
python3 tools/check_browser.py         # needs Chrome; set CHROME to its path
```

## Routines, and how a person stays in control

Every workflow is listed in `ops/automation.yaml` with a tier from 0 (observe) to 3 (person only). Nothing merges
itself. The kill switch is the repository variable `AUTOMATION` set to `off`. Near misses go in the occurrence form,
without blame. The weekly signals scan runs outside the repository and proposes its update as a pull request.

Back: [the intermediate guide](intermediate.md).
