# Contributing

Thank you for helping improve AI Capability Governance and Implementation.

1. For a question or a small correction, use the [contact form](https://github.com/cyberdudeuk/ai-capability-governance/issues/new?template=contact.yml) or a more specific form from the site's Contact section.
2. To propose a change, edit `index.html`, `app.js`, `styles.css` or `data/ai-data-governance-signals.json` on a branch and open a pull request. Nothing reaches `main` except through a pull request.
3. Every new fact needs a source. Anything that cannot be reproduced from a source is labelled modelled, estimated or unconfirmed on the page.
4. Signals credit the named author and organisation, are paraphrased (no quotation over 15 words) and keep their evidence label.
5. Write in plain English and sentence case, following the GOV.UK style guide. Name roles, never people. Never include an email address.
6. Run `python3 tools/check_site.py && python3 -m unittest discover -s tests` before you open the pull request.
7. If you fix a defect, add a check that would have caught it in the same pull request, and add it to [the defect register](docs/defect-register.md).

See [the advanced guide](docs/user-guide/advanced.md) for how the repository and its routines work.
