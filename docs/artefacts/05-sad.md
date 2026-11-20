---
artefact:id: P09-SAD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P09 AI Capability Governance and Implementation
grade: G3
profile: public sector > personal public good (content under CC BY 4.0)
---

# Solution architecture (SAD): AI Capability Governance and Implementation

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Context
Public servants using AI, and the data it uses, lack practical, proportionate tools to decide how much human review an AI use needs and what evidence to keep.

The solution is described in [03-prd.md](03-prd.md). It connects with: NDL PubSec MCP; GOV.UK AI guidance and ATRS.

## Architecturally significant decisions
These are the decisions already recorded in this repository (V):

- [0001-rename-and-scope.md](../adr/0001-rename-and-scope.md)
- [0002-actions-policy.md](../adr/0002-actions-policy.md)

## Quality attributes

| Attribute | How it is met |
|---|---|
| Self-contained with vendored fonts | Self-contained with vendored fonts |
| Content CC BY 4.0, code MIT | Content CC BY 4.0, code MIT (personal project) |
| CodeQL, dependency review, Scorecard | CodeQL, dependency review, Scorecard |
| Contact | By form only; no email address anywhere (estate rule) |
| Documentation | This kit, checked in CI by `tools/artefact_check.py` |

## Constraints
- Prototype, version 3.3.0, 18 Nov 2026; content reviewed 13 Nov 2026 (V: README).
- No personal data unless a DPIA has been done first.
- Contact by form only.

## Risks (proposed ratings)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Read as official assurance | Medium | High | Status banner; 'does not replace' statement |
| Fast-changing guidance | High | Medium | Quarterly content review; signals digest |
