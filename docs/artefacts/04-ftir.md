---
artefact:id: P09-FTIR-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P09 AI Capability Governance and Implementation
grade: G3
profile: public sector > personal public good (content under CC BY 4.0)
---

# Functional, technical and integration requirements (FTIR): AI Capability Governance and Implementation

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

Requirements are stated once, in [03-prd.md](03-prd.md). This document says how each is met and checked.

## Functional

| ID | Requirement | Priority | Verified by | State |
|---|---|---|---|---|
| F01 | Human review triage returns H0 to H5 with mandatory follow-on actions | Must | tests/test_site.py | Has a check |
| F02 | Evidence pack generator | Must | tests/test_site.py | Has a check |
| F03 | DEIA impact screen | Should | tests/test_site.py | Has a check |
| F04 | Transparency record shaped like ATRS | Should | tests/test_site.py | Has a check |
| F05 | Quantum readiness assessor | Could | tests/test_site.py | Has a check |
| F06 | Plain-language checker | Should | tests/test_site.py | Has a check |
| F07 | Keeps nothing typed; no tracking | Must | tools/check_site.py (U) | Check named; coverage unconfirmed (U) |
| F08 | Weekly signals digest | Should | digest.yml | Has a check |

## Technical

| ID | Requirement | State |
|---|---|---|
| T01 | Code scanning | Present (V: .github/workflows) |
| T02 | Dependency review on pull requests | Present (V: .github/workflows) |
| T03 | OpenSSF Scorecard | Present (V: .github/workflows) |
| T04 | Automated release | Present (V: .github/workflows) |
| T05 | Published by workflow (Pages) | Present (V: .github/workflows) |
| T06 | Documentation kit checked in CI | Present (V: .github/workflows) |

Workflows present (V): `checks.yml`, `codeql.yml`, `dependency-review.yml`, `digest.yml`, `labels.yml`, `pages.yml`, `release.yml`, `scorecard.yml`, `triage.yml`.

Tests present (V): `test_automation.py`, `test_publiccode.py`, `test_site.py`.

## Integration

| ID | Integration | Direction | State |
|---|---|---|---|
| I01 | NDL PubSec MCP | Its term review model (H0 to H5) | Referenced |
| I02 | GOV.UK AI guidance and ATRS | Link out | Live |
