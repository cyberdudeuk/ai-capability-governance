---
artefact:id: P09-HLD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P09 AI Capability Governance and Implementation
grade: G3
profile: public sector > personal public good (content under CC BY 4.0)
---

# High-level design (HLD): AI Capability Governance and Implementation

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Building blocks
Derived from the repository's top-level structure (V: git tree, 20 Nov 2026).

| Part | Role | Files |
|---|---|---|
| `.github/` | Workflows, issue forms and repository health files | 22 |
| `docs/` | Documentation and registers | 11 |
| `tools/` | Build, check and routine scripts | 10 |
| `data/` | Data files (single source) | 3 |
| `fonts/` | Vendored fonts | 3 |
| `tests/` | Automated tests | 3 |
| `ops/` | Operations: agents, routines, audit | 2 |

## How it fits together
1. Content and data live in the source folders above. They are the single source of truth.
2. The build and check commands in [07-lld.md](07-lld.md) generate the published output from those sources. Generated folders are never edited by hand. (D-KIT-02: an earlier draft named the first command as 'the build', which was wrong for repositories whose first command is a test run.)
3. Checks and tests run locally and in CI before anything is published.
4. Publication happens through the repository's workflow (pages.yml, release.yml).
5. People change things through pull requests and GitHub issue forms. Routines report; a person decides anything irreversible.

## Integrations
- **NDL PubSec MCP:** Its term review model (H0 to H5) (Referenced)
- **GOV.UK AI guidance and ATRS:** Link out (Live)

## Environments
- **Local:** run the build and checks below.
- **CI:** GitHub Actions. Note: on 20 November 2026 no Actions jobs could start on this account because of a billing block; local checks are the evidence until that is fixed.
- **Live:** https://cyberdudeuk.github.io/ai-capability-governance/

For the architecture rationale, see [05-sad.md](05-sad.md).
