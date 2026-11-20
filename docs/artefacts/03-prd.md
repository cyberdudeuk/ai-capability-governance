---
artefact:id: P09-PRD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P09 AI Capability Governance and Implementation
grade: G3
profile: public sector > personal public good (content under CC BY 4.0)
---

# Product requirements (PRD): AI Capability Governance and Implementation

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Problem and outcome
Public servants using AI, and the data it uses, lack practical, proportionate tools to decide how much human review an AI use needs and what evidence to keep.

Outcome sought: AI uses in public services get proportionate human review and a clear evidence record, faster. See [01-theory-of-change.md](01-theory-of-change.md).

## Users
- New or occasional contributors
- Members of the public asking how AI is used on their case
- Suppliers and delivery partners
- Accountable owners and SROs
- Data or AI governance leads
- Experienced practitioners

User evidence: [02-ur-bundle.md](02-ur-bundle.md).

## Scope
**In:**
- The six tools
- Signals digest
- Beginner, intermediate and advanced guides

**Out:**
- Replacing an organisation's policy, DPO, security or legal advice
- Keeping anything users type

## Requirements
Derived from what this repository says it does (V: README and ADRs). The last column is the check that proves each one, where one exists. U means no check was found that clearly covers it; that is a gap to close, not a pass.

| ID | Requirement | Priority | Verified by |
|---|---|---|---|
| P09-R01 | Human review triage returns H0 to H5 with mandatory follow-on actions | Must | tests/test_site.py |
| P09-R02 | Evidence pack generator | Must | tests/test_site.py |
| P09-R03 | DEIA impact screen | Should | tests/test_site.py |
| P09-R04 | Transparency record shaped like ATRS | Should | tests/test_site.py |
| P09-R05 | Quantum readiness assessor | Could | tests/test_site.py |
| P09-R06 | Plain-language checker | Should | tests/test_site.py |
| P09-R07 | Keeps nothing typed; no tracking | Must | tools/check_site.py (U) |
| P09-R08 | Weekly signals digest | Should | digest.yml |

## Non-functional requirements
- Self-contained with vendored fonts
- Content CC BY 4.0, code MIT (personal project)
- CodeQL, dependency review, Scorecard

## Status
Prototype, version 3.3.0, 18 Nov 2026; content reviewed 13 Nov 2026 (V: README)
