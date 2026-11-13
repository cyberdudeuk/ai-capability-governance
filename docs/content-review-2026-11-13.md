# Content review, 13 November 2026

The quarterly review fell due on 8 November 2026. This record says what was checked, how, what changed and what was
not checked. Next review due: **13 February 2027**.

## What was checked, and how

| Check | Method | Result |
|---|---|---|
| Every resource link loads at its address | `tools/check_links.py` (automated), then the 8 sites that refuse automated requests opened by hand in a browser | 69 of 69 load after the changes below: 61 automatically, 8 by hand. The ICO pages, which refused automated checks on 8 November, now answer them |
| No source has been withdrawn or replaced | Each page read for GOV.UK's withdrawal banner and "superseded by" or "replaced by" notices; the check is now in the weekly link check (D-19) | 1 withdrawn: the Generative AI Framework for HMG |
| No source is flagged as under review | Each page searched for review notices | 3 ICO pages are under review after the Data (Use and Access) Act 2025 |
| Data protection law is current | The Act and its commencement read on legislation.gov.uk; the ICO's guidance pages read directly | The automated decision-making rules changed on 5 February 2026 and were missing from the toolkit |

## Changes

1. **Removed the Generative AI Framework for HMG.** GOV.UK says it was withdrawn on 10 February 2025 and superseded by the
   AI Playbook for the UK Government, which the library already lists. The AI Playbook's entry now says so, and toolkit asset
   TK-08 anchors to it.
2. **Added the Data (Use and Access) Act 2025** (tier 0). Section 80 replaced UK GDPR Article 22 with Articles 22A to 22D.
   legislation.gov.uk records section 80 as in force from 5 February 2026 (SI 2026/82, regulation 2(j)).
3. **Added the ICO's guidance on automated decision-making, including profiling** (tier 1). The ICO page says it is
   consulting on updates for the 2025 Act (latest update 31 March 2026). The consultation closed on 29 May 2026, and the
   guidance has not been finalised.
4. **Marked three ICO resources as under review.** These are AI and data protection, the AI and data protection risk
   toolkit, and DPIAs. Each page says "Due to changes made by the Data (Use and Access) Act, this guidance is under review
   and may be subject to change."
5. **Changed the Data Protection Act 2018 entry** so it no longer promises automated decision-making safeguards. Those rules
   are now in the 2025 Act's amendments.
6. **Added "meaningful human involvement" to the glossary.** Whether a person meaningfully takes part decides whether a
   decision counts as solely automated, so it shapes how the H0 to H5 review levels apply.
7. **Updated four moved links:**
   - The ICO AI risk toolkit's old address now returns 404 (confirmed in a browser). The new address, found from the ICO's AI page, is under the AI and data protection guidance.
   - ISO/IEC 42001 is now at `/standard/42001`.
   - The Turing's *Understanding AI ethics and safety* moved from `/research/` to `/news/`.
   - The W3C Web Sustainability Guidelines moved to `w3c-cg.github.io`.
8. **Greening Government ICT and digital services strategy:** its period was 2020 to 2025. Its 2024 to 2025 annual report
   (published 16 July 2026) says a new government digital sustainability strategy is coming. The entry now says so. Replace
   it when the new strategy is published.

## Checked by hand in a browser

These 8 sites refuse automated requests. On 13 November 2026 each one was opened in a browser and its title read.

- ISO/IEC 27001, 23894 and 42001 (the old 42001 address redirects to the new one)
- EHRC Public Sector Equality Duty
- security.gov.uk Secure by Design
- The Alan Turing Institute (new address)
- github.com/alphagov and UKHomeOffice/posters

## Limits

- **What a source says was not re-read word by word.** Each entry's one-line description was checked against the page title
  and any notice on the page, not against the full text. The data protection entries were checked in more depth (above).
- **Draft guidance:** the ICO's automated decision-making guidance is a draft. Re-check at the next review whether it has
  been finalised, and whether the ICO has published the statutory code of practice on AI and automated decision-making
  that commentary says the Act requires.
- **The toolkit is a prototype, not official guidance.** This review does not make it legal advice.

Contact: by the [contact form](https://github.com/cyberdudeuk/ai-capability-governance/issues/new/choose) only.
