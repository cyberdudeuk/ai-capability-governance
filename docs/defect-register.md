# Defect register

Every defect found gets a check that prevents it coming back, in the same change as the fix. The check suite never
shrinks. Check codes refer to `tools/check_site.py`; each has a vaccination test in `tests/test_site.py`.

| ID | Found | Defect | Root cause | Fix | Check |
|---|---|---|---|---|---|
| D-01 | 2026-11-08 | Two email addresses on `example.gov.uk` in the worked metadata example, and an email-client route in the contact form | Written before the contact-form-only rule; `example.gov.uk` looks real and is not a reserved example domain | Replaced with a role and the contact form; removed the mailbox setting, the email route and the reply-address field | S1, S8 |
| D-02 | 2026-11-08 | Risk that signals on the page drift from the register, or lose their attribution or evidence label | The page is static HTML generated from the JSON register | Page built from the register; both published together | S2, S3, S4 |
| D-03 | 2026-11-08 | Risk of version strings disagreeing across page, JSON-LD, footer and script | Version written in five places | One version, checked everywhere | S5 |
| D-04 | 2026-11-08 | The Contact section linked to four issue forms and a security policy that did not exist, so every report route was broken | `.github/ISSUE_TEMPLATE` was never created | Added the forms | S7 |
| D-05 | 2026-11-08 | Self-references would keep pointing at the old root address and repository after the rename | Addresses hard-coded in the page, script and README | Updated everywhere | S9 |
| D-06 | 2026-11-08 | Personas and tasks had no level, so beginners and experts were sent to the same place | Levels were not part of the original design | Levels and journeys on every persona and task | S10 |
| D-07 | 2026-11-08 | README linked to `CHANGELOG.md` and `ACCESSIBILITY.md`, which did not exist | Files referenced but never written | Added both | S11 |
| D-08 | 2026-11-08 | An early version of the email check flagged the Google Fonts address `GRAD@20..48` (false positive) | Pattern allowed a domain starting with a digit | Domain must start with a letter and end in a letter top-level domain | S1 (vaccinated) |
| D-09 | 2026-11-08 | The inherited Pages workflow used actions by moving tag (`@v4`) and published the whole repository, including tools and tests, with no checks first | Written before the estate actions policy | Publish now checks first, publishes only the site files, and pins every action to a full commit | S13 |
| D-10 | 2026-11-08 | The new levels table made the page scroll sideways on a 390px phone; static checks could not see it | Layout is only visible in a browser | Levels shown as cards; browser checks added at three widths | B1, B2, B3 (`tools/check_browser.py`, vaccinated in CI) |
| D-11 | 2026-11-08 | The page scrolled sideways on a 320px screen (fails WCAG 2.2 reflow, 1.4.10). Present in v2.0.0 | Header tools did not wrap, and grid columns had fixed minimum widths wider than a small screen | Header tools wrap; grid columns capped at the container width | B1 at 320px |
