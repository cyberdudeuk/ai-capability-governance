# AI Capability Governance and Implementation

[![Version](https://img.shields.io/badge/version-3.1.0-0b3d91)](CHANGELOG.md)
[![Checks](https://github.com/cyberdudeuk/ai-capability-governance/actions/workflows/checks.yml/badge.svg)](https://github.com/cyberdudeuk/ai-capability-governance/actions/workflows/checks.yml)
[![Licence: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![Content: OGL v3.0](https://img.shields.io/badge/content-OGL%20v3.0-blue)](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
[![WCAG 2.2 AA target](https://img.shields.io/badge/accessibility-WCAG%202.2%20AA%20target-00703c)](ACCESSIBILITY.md)

**Govern AI, and the data it uses, in public services: guidance you can act on, working tools, and a weekly read of what is changing.**

### [Open the site →](https://cyberdudeuk.github.io/ai-capability-governance/)

It opens in any browser, works on a phone, keeps nothing you type and has no tracking. Formerly the **Public AI Utility
Toolkit**; now the public edition of the BOT AI governance toolkit, in its own repository (see [ADR 0001](docs/adr/0001-rename-and-scope.md)).

| | |
|---|---|
| **Status** | Prototype. Not official GOV.UK guidance; it does not replace your organisation's policies, data protection officer, security team or legal advice |
| **Version** | 3.1.0, 13 November 2026 ([changelog](CHANGELOG.md)) |
| **Review** | Last reviewed 13 November 2026 ([record](docs/content-review-2026-11-13.md)). Next review due 13 February 2027 |
| **Contact** | By [contact form](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=contact.yml) only. There is no email route |

## Choose your way in

### 1. How much do you already know?

| If you… | You are | Start on the site with | Read here |
|---|---|---|---|
| are new to AI in public services, or to this site | **Beginner** | The four principles, then the 2-minute human review triage | [Beginner](#beginner-new-to-ai-governance), and the [beginner guide](docs/user-guide/beginner.md) |
| use, buy or approve AI in your work and need to show it is governed | **Intermediate** | The H0–H5 review model, then the evidence pack | [Intermediate](#intermediate-governing-ai-in-your-work), and the [intermediate guide](docs/user-guide/intermediate.md) |
| build, assure, integrate or reuse this guidance, including in code | **Advanced** | The toolkit and the metadata schema | [Advanced](#advanced-building-assuring-and-reusing-it), and the [advanced guide](docs/user-guide/advanced.md) |

### 2. What kind of work do you do?

| Persona | Their question | Level | Journey on the site |
|---|---|---|---|
| **New or occasional contributor** | "I don't want to get this wrong." | Beginner | Human review triage → Evidence pack → Code of practice |
| **Member of the public** | "How is AI being used on my case?" | Beginner | Transparency → Glossary and FAQ → Contact |
| **Supplier or delivery partner** | "What will I be assessed against?" | Intermediate | Resources (procurement, security) → Catalogue metadata → Assurance |
| **Accountable owner or SRO** | "What am I signing?" | Intermediate | H0–H5 review model → Transparency record → Roadmap |
| **Data or AI governance lead** | "What is changing, and does my data estate let us govern agents?" | Intermediate to advanced | Signals → Agent registry (TK-03) → AI asset metadata → Review model |
| **Experienced practitioner** | "Give me the fast, correct route." | Advanced | Toolkit → Metadata schema → Tools |
| **Specialist reviewer** | "Show me what to challenge." | Advanced | Reviewer checklist → Authority tiering → Signals |

The same levels and journeys are on the site's **Start here** section, and every common task there is marked with its level.

### 3. How the site is laid out

Most important first: **Start here**, then **Knowledge**, the **Toolkit** and **Tools**, **Assurance**, the metadata
**Catalogue**, **UCD and DEIA**, the code of **Practice**, **Resources** and **Signals**, with **Transparency**, the
**Roadmap**, **Glossary** and **Contact** last.

## Beginner: new to AI governance

Four principles sit under everything:

1. **Humans remain accountable.** AI never grants authority a person does not already hold.
2. **AI outputs are verified, not trusted by default.** Every claim traces to a citable source.
3. **Public value, equality and accessibility are built in**, screened before delivery, not audited after.
4. **Evidence, metadata and provenance are mandatory** for anything material or public-facing.

Three things to try first:

- [Decide how much human review your work needs](https://cyberdudeuk.github.io/ai-capability-governance/#tool-triage) (2 minutes)
- [Write an AI-use declaration and evidence pack](https://cyberdudeuk.github.io/ai-capability-governance/#tool-evidence) (3 minutes)
- [Look up a word in the glossary](https://cyberdudeuk.github.io/ai-capability-governance/#glossary)

Everything runs in your browser. Nothing you type is sent anywhere, stored or logged.

## Intermediate: governing AI in your work

### The six tools

| Tool | What it does | Level | Time |
|---|---|---|---|
| Human review triage | Scores audience, impact, data classification, reversibility and six escalating factors to return an H0–H5 level with mandatory follow-on actions | Beginner | 2 min |
| Evidence pack generator | Produces a copy-ready AI-use declaration and evidence record | Beginner | 3 min |
| DEIA impact screen | Tests ten exclusion risks and says whether a full equality impact assessment is needed | Intermediate | 5 min |
| Transparency record generator | Drafts a record shaped like the Algorithmic Transparency Recording Standard | Intermediate | 10 min |
| Quantum readiness assessor | Scores harvest-now-decrypt-later exposure against NCSC migration milestones | Advanced | 5 min |
| Plain-language checker | Reading age, sentence length, passive voice, unexplained acronyms, jargon and non-inclusive phrasing | Beginner | 1 min |

### Signals: what is changing

[Signals](https://cyberdudeuk.github.io/ai-capability-governance/#signals) is a weekly horizon scan of AI and data
governance content (21 items on 8 November 2026). Each names its author and organisation, links to where it was found
and carries an evidence label. **Read with care:** LinkedIn does not allow automated reading of posts, so summaries come
from search-indexed text; 13 of the 21 come from vendors, consultancies or law firms and are marked; two statistics are
flagged as unverified. [Suggest a signal](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=signal_suggestion.yml).

### What is on the site

| Section | What it gives you |
| --- | --- |
| Start here | Levels, seven role-based routes with journeys, and six common tasks with times and levels |
| Knowledge | Authority tiering (0–3), conflict resolution and drift triggers |
| Toolkit | 18 catalogued assets, each anchored to the standards it implements, including the agent registry (TK-03) |
| Tools | The six tools above |
| Assurance | The H0–H5 review model, reviewer checklist, failure patterns and a RACI |
| Catalogue | Minimum viable metadata for any AI asset, with a worked YAML example |
| UCD and DEIA | Design and research practice, accessibility commitments and AI-specific equity risks |
| Practice | Code of practice: core duties, prohibited behaviours, agent rules, code rules, speaking up |
| Resources | 69 tiered sources, searchable and filterable |
| Signals | The weekly AI and data governance horizon scan |
| Transparency | Ownership, versioning, licence, privacy, limitations and changelog |
| Roadmap | Identified gaps prioritised with MoSCoW |
| Glossary and FAQ | Plain-English terms and answers |
| Contact | Bug, accessibility, feature, correction, security and contact routes, all through GitHub |

## Advanced: building, assuring and reusing it

### Repository map

| Path | What it is |
| --- | --- |
| `index.html`, `styles.css`, `app.js` | The site. All content is in the HTML and readable without JavaScript |
| `data/ai-data-governance-signals.json` | The open signals register, shared with the internal BOT toolkit |
| `tools/check_site.py` | 17 static checks, each naming the defect it prevents ([defect register](docs/defect-register.md)) |
| `tools/check_browser.py` | Browser checks in Chrome at 1280, 390 and 320px: no sideways scroll, no console errors, contact form opens the GitHub form |
| `tools/build_signals.py` | Rebuilds the Signals section from the register; never edit that section by hand |
| `tools/health.py` | Weekly health run: review date and signals freshness |
| `tools/digest.py`, `tools/triage.py`, `tools/trials.py` | Estate routines: they report and label, never change content |
| `tests/` | Vaccination tests (every check must fail on a deliberate break) and automation tests |
| `ops/automation.yaml` | Every workflow, its tier, when it runs and what it may change |
| `docs/` | [Decisions](docs/adr/0001-rename-and-scope.md), [defect register](docs/defect-register.md), [settings checklist](docs/repo-settings.md), [user guides](docs/user-guide/advanced.md) |
| `.github/` | Issue forms, labels as code, workflows, Dependabot and the pull request template |

### Build and check locally

```bash
pip install -r requirements.txt
python3 tools/check_site.py
python3 -m unittest discover -s tests -v
node --check app.js
python3 tools/check_browser.py         # needs Chrome; set CHROME to its path
python3 -m http.server 8000   # then open http://localhost:8000
```

### Routines, and how a person stays in control

A change reaches `main` only through a pull request that has passed the checks, and the publish workflow checks again before it deploys only the site files to GitHub Pages.
Every workflow is declared in [`ops/automation.yaml`](ops/automation.yaml) with a tier from 0 (observe) to 3 (person
only): checks on every pull request, a Monday health run and digest, weekday triage, labels as code, CodeQL, OpenSSF
Scorecard and dependency review. Nothing merges itself. The kill switch is the repository variable `AUTOMATION` set to
`off`. Near misses go in the [occurrence form](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=occurrence.yml), without blame.
The weekly signals scan runs outside the repository and proposes its update as a pull request.

### Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Every factual claim needs a tiered, dated, authoritative source; anything that
cannot be reproduced is labelled modelled, estimated or unconfirmed.

| I want to… | Route |
| --- | --- |
| Ask a question or give feedback | [Contact form](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=contact.yml) |
| Report a bug | [Bug report](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=bug_report.yml) |
| Report an accessibility barrier | [Accessibility issue](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=accessibility_issue.yml) |
| Suggest a feature or resource | [Feature request](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=feature_request.yml) |
| Correct out-of-date content | [Content correction](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=content_correction.yml) |
| Suggest a signal | [Signal suggestion](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=signal_suggestion.yml) |
| Report a vulnerability | [Security policy](SECURITY.md): private reporting, never a public issue |

## Part of a wider set of projects

This is one of several public projects listed on the owner's launchpad at [cyberdudeuk.github.io](https://cyberdudeuk.github.io/),
alongside the [DAM capability playbooks](https://cyberdudeuk.github.io/dam-capability-playbooks/), the
[Data Quality Commons](https://cyberdudeuk.github.io/dq-commons/), [DCAT-AP-UK](https://cyberdudeuk.github.io/dcat-ap-uk/) and
the [GitHub Repos Asset Catalogue](https://cyberdudeuk.github.io/github-repos-asset-catalogue/).

## Governance and licence

| | |
| --- | --- |
| Owner | AI Capability Governance working group |
| Content licence | [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) |
| Code licence | [MIT](LICENSE) |
| Accessibility | [Accessibility statement](ACCESSIBILITY.md) (designed to WCAG 2.2 AA; not independently audited) |
| Security | [SECURITY.md](SECURITY.md) |
| Support | [SUPPORT.md](SUPPORT.md) |
| Conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Citation | [CITATION.cff](CITATION.cff) |
