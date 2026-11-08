# Resource link review, 8 November 2026

An automated check of all 68 links in the Resources section, done because the quarterly review fell due on
8 November 2026. **This is a link check, not a content review**: whether each source still says what the toolkit says
it does has not been re-checked, so the last-reviewed and next-review dates are unchanged.

| Result | Count | What was done |
|---|---|---|
| Working at the same address | 56 | Nothing |
| Broken | 1 | NCSC post-quantum guidance: the old collection page returns 404; replaced with NCSC's current guidance, *Timelines for migration to post-quantum cryptography* (https://www.ncsc.gov.uk/guidance/pqc-migration-timelines), found by search and confirmed to load |
| Moved | 4 | Updated to the address each now redirects to: DDaT capability framework, GOV.UK style guides, OWASP Top 10 for LLM Applications, X-GOVUK |
| Refuse automated checks (403) | 11 | **Not verified.** ICO (3), ISO (3), Equality and Human Rights Commission, security.gov.uk Secure by Design, Alan Turing Institute, and two GitHub organisation pages. A 403 usually means the site blocks automated requests, not that the page is gone. Check these by hand at the content review |

The model context protocol front page redirects into its versioned documentation; that is normal for a front page and
the link is kept.

From now on, `tools/check_links.py` runs in the Monday health run and opens a health issue for any broken or moved link.
