# Changelog

The site's own changelog, with fuller wording, is in its Transparency section.

## 3.1.0 — 13 November 2026

Content review, due since 8 November 2026 (`docs/content-review-2026-11-13.md`).

- **Withdrawn source removed.** The Generative AI Framework for HMG was withdrawn on 10 February 2025 and replaced by the AI Playbook for the UK Government. It is no longer listed, and toolkit asset TK-08 now anchors to the AI Playbook.
- **Automated decision-making law updated.** Added the Data (Use and Access) Act 2025, which replaced UK GDPR Article 22 with Articles 22A to 22D from 5 February 2026, and the ICO's draft guidance on automated decision-making. Added "meaningful human involvement" to the glossary, because it decides whether a decision counts as solely automated.
- **ICO guidance flagged as under review.** The ICO says its guidance on AI and data protection, its AI risk toolkit and its DPIA guidance are under review after the 2025 Act.
- **Links.** The ICO AI risk toolkit (now 404 at its old address), ISO/IEC 42001, the Turing's AI ethics guide and the W3C Web Sustainability Guidelines have moved; all four are updated. The 8 sites that refuse automated checks were opened by hand in a browser and all load.
- **Greening Government ICT strategy** marked as covering 2020 to 2025, with its successor on the way.
- **Agent answers (issue 16).** The evidence pack has a new optional field for the data definitions an agent's answer relied on, with each one's review level. Anything below H2 is flagged as not certified. Browser check B4 tests it. The advanced guide adds a worked example on reviewing an answer an agent built from those definitions, with its transparency and automated decision-making duties.
- **Signals.** Added S22, NVIDIA Auto Ontology, read from its repository rather than search results, and labelled as such (D-21). The owner's LinkedIn post (S00) is partly read: its opening line, author handle and date. The rest is behind LinkedIn's security check, so it stays pending.
- **New checks.** The weekly link check now reads each page for a withdrawal notice (D-19) and retries a timeout before calling a link broken (D-20). S19 keeps the no-JavaScript copy in step with the data, and S5 now covers CITATION.cff and the README (D-18).

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
