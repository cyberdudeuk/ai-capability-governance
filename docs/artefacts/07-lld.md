---
artefact:id: P09-LLD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P09 AI Capability Governance and Implementation
grade: G3
profile: public sector > personal public good (content under CC BY 4.0)
---

# Low-level design (LLD): AI Capability Governance and Implementation

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Build and check commands (V: README)
```
python3 -I tools/build_static.py
python3 -I tools/check_site.py
python3 -I -m pytest tests
```

## Scripts (V: file tree)
- `tools/build_playbook.py`
- `tools/build_signals.py`
- `tools/build_static.py`
- `tools/check_browser.py`
- `tools/check_links.py`
- `tools/check_site.py`
- `tools/digest.py`
- `tools/health.py`
- `tools/triage.py`
- `tools/trials.py`

## Tests (V: file tree)
- `tests/test_automation.py`
- `tests/test_publiccode.py`
- `tests/test_site.py`

## Workflows (V: .github/workflows)
- `checks.yml`
- `codeql.yml`
- `dependency-review.yml`
- `digest.yml`
- `labels.yml`
- `pages.yml`
- `release.yml`
- `scorecard.yml`
- `triage.yml`

## Repository size
79 files tracked on 20 November 2026.

## Documentation kit
- `docs/artefacts/manifest.yaml` lists every core document, where it is, and its review date.
- `tools/artefact_check.py` checks the kit (rules AC-01 to AC-08, each with a negative test). Run `python3 tools/artefact_check.py --self-test` then `python3 tools/artefact_check.py .`.

## Handover
Someone new can rebuild and verify with the commands above, then read [03-prd.md](03-prd.md) and [05-sad.md](05-sad.md).
