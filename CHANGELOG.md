# Changelog

The site's own changelog, with fuller wording, is in its Transparency section.

## Unreleased

### Changed: content licence

- The portal's own content is now under Creative Commons Attribution 4.0 (CC BY 4.0), not the Open Government Licence: this is a personal project, not government work. Crown copyright material quoted in it stays under OGL v3.0. Code stays MIT. New check S26 (D-35).

## 3.3.0 — 18 November 2026

### Changed: one portal, after the original portal's design

- **One portal.** The playbook moved into `index.html`. One masthead with six grouped menus and a call to action,
  so it never overflows; one contents drawer for the whole portal (a labelled switch retracts it; parts with icons,
  counts, new flags and read marks); one glossary; one footer. `playbook.html` now redirects into the portal.
- **Redesigned after the original AI Capability Governance portal**, its visuals used as the blueprint: the Figtree
  typeface (self-hosted, SIL Open Font Licence, `fonts/`), the navy front page with the orbit illustration and glass
  panels, the "guidance in force" ticker (pauses on hover, focus or its button; still when reduced motion is set),
  white "what do you want to do?" cards with coloured top borders, tinted part cards for the contents, and the
  chapter view with part chips, chapter numbers and progress bars. Dark and high-contrast themes kept.
- **One glossary**: 39 playbook terms merged into the portal glossary (now 62); existing definitions kept (D-34).
- Order of precedence: start, playbook, tools, assurance and delivery, knowledge, then about.
- Check S25 (D-32); ticker overflow fixed (D-33).

## 3.2.0 — 18 November 2026

Includes the repository-standards work listed below under "Since 3.1.0".

### Added

- **Agent governance playbook** (`playbook.html`): the public edition of an internal AI agent governance toolkit.
  77 chapters in 12 parts, rebuilt as plain semantic content that reads without JavaScript; a retractable contents
  drawer with icons, counts and new flags; a chapter filter; tabs for reading, the route tool, the knowledge map and the
  method; a working “Can I use AI for this?” route tool; a knowledge map; a QR and barcode colophon.
- Open exchange: the full content as `data/playbook.json` and the part and chapter taxonomy as SKOS in JSON-LD
  (`data/playbook-taxonomy.jsonld`).
- `docs/content-classification-2026-11-18.md`: every chapter's decision. Ten chapters are withheld, each with a reason.
- Checks S21 to S24 and browser checks B5 to B7 (axe-core, WCAG 2.2 AA, light and dark), each with a negative test.

### Fixed

- Masthead line that repeated the old name (D-28); dark-mode contrast on buttons, chips and badges (D-30); keyboard
  access to the YAML example (D-31).


### Since 3.1.0: repository standards for the move to gds-dtx, 17 November 2026

- The Cabinet Office vulnerability disclosure route in `SECURITY.md`.
- Pre-commit hooks: detect-secrets against a new `.secrets.baseline`, YAML and JSON checks, whitespace fixes, and gitlint for GDS Way commit messages (`.gitlint`).
- `.secrets.baseline` with every candidate audited, and the audit recorded in `docs/compliance/secrets-audit.md`.

### Changed

- Replaced the old directorate name with Government Data Directorate in `ops/signals-scan-prompt.md`.

- Checks now run Ruff (Python) and ESLint (JavaScript) and fail on any finding (D-24). Eleven findings fixed, including
  browser-check listeners that could record an error against the wrong page. Part of applying the secure development
  standard to every project.

## 3.1.0 — 13 November 2026

Content review, due since 8 November 2026 (`docs/content-review-2026-11-13.md`).

- **Withdrawn source removed.** The Generative AI Framework for HMG was withdrawn on 10 February 2025 and replaced by the AI Playbook for the UK Government. It is no longer listed, and toolkit asset TK-08 now anchors to the AI Playbook.
- **Automated decision-making law updated.** Added the Data (Use and Access) Act 2025, which replaced UK GDPR Article 22 with Articles 22A to 22D from 5 February 2026, and the ICO's draft guidance on automated decision-making. Added "meaningful human involvement" to the glossary, because it decides whether a decision counts as solely automated.
- **ICO guidance flagged as under review.** The ICO says its guidance on AI and data protection, its AI risk toolkit and its DPIA guidance are under review after the 2025 Act.
- **Links.** The ICO AI risk toolkit (now 404 at its old address), ISO/IEC 42001, the Turing's AI ethics guide and the W3C Web Sustainability Guidelines have moved; all four are updated. The 8 sites that refuse automated checks were opened by hand in a browser and all load.
- **Greening Government ICT strategy** marked as covering 2020 to 2025, with its successor on the way.
- **Agent answers (issue 16).** The evidence pack has a new optional field for the data definitions an agent's answer relied on, with each one's review level. Anything below H2 is flagged as not certified. Browser check B4 tests it. The advanced guide adds a worked example on reviewing an answer an agent built from those definitions, with its transparency and automated decision-making duties.
- **Signals.** Brought the register up to the master copy in the BOT app (version 1.1.0: S22 to S27 from the 9 November scan had not reached this site, D-23). Added S28, NVIDIA Auto Ontology, read from its repository rather than search results, and labelled as such (D-22). Register now version 1.2.0. The owner's LinkedIn post (S00) is partly read: its opening line, author handle and date. The rest is behind LinkedIn's security check, so it stays pending.
- **New checks.** The weekly link check now reads each page for a withdrawal notice (D-20) and retries a timeout before calling a link broken (D-21). S20 keeps the no-JavaScript copy in step with the data, and S5 now covers CITATION.cff and the README (D-19). S19, merged in #20, stops published docs pointing at a pull request "until it merges" (D-18).

## 3.0.1 — 8 November 2026

- Replaced the broken NCSC post-quantum guidance link and four moved links, after an automated check of all 68 resource links (`docs/link-review-2026-11-08.md`). 11 sites refuse automated checks and are still to be checked by hand; the content review is still due.
- The Monday health run now checks every resource link and opens a health issue for any that break or move.
- Fixed the duplicate pins and steps left by Dependabot updates, with checks so they cannot return.
- Stopped committing compiled Python cache files. They had been in the repository since 3.0.0 and made merges conflict; a `.gitignore` and check S18 keep them out.

## 3.0.0 — 8 November 2026

- Renamed from the Public AI Utility Toolkit to **AI Capability Governance and Implementation**, the public edition of the BOT AI governance toolkit, and moved from the account's root address to its own repository and address. The root address becomes the owner's project launchpad.
- Added **Signals**: a weekly horizon scan of AI and data governance content, with attribution, evidence labels and an open JSON register.
- Added **Beginner, Intermediate and Advanced** levels to every persona, journey and common task, a "How much do you already know?" table, and a new data or AI governance lead persona.
- **Contact is by form only**: removed the email-client route, the mailbox setting and the reply-address field; replaced the two addresses in the worked metadata example with a role and the form.
- Added the issue forms the contact links already pointed to (they were missing), plus contact, signal and near-miss forms.
- Added the estate contract: automation policy, checks on every pull request, weekly health run and digest, triage, labels as code, CodeQL, Scorecard, dependency review, releases and Dependabot.
- Added this changelog, an accessibility statement, security, support, contributing and citation files, and beginner, intermediate and advanced guides.
- Fixed the page scrolling sideways on small phones (320px wide), present since 2.0.0, and added browser checks at three widths.
- Publishing now runs every check first and publishes only the site files; every action is pinned to a full commit.
- Not done: the 68 resource links were not re-verified, so the review dates are unchanged and the review is shown as due.

## 2.0.0 — 8 August 2026

Task-first entry points, six interactive tools, a tiered resource library, the H0–H5 review table, RACI, transparency and redress commitments, MoSCoW roadmap, glossary and FAQ, display modes, site search and a print stylesheet.

## 1.0.0

Concept portal: mission, knowledge corpus, toolkit, assurance workflow, catalogue, UCD and code of practice.
