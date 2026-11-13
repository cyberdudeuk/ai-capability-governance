# Advanced guide

For you if you build, assure, integrate or reuse this guidance, including in code.

## Reuse the content and data

- The page is one HTML file; every piece of content is readable without JavaScript.
- `data/ai-data-governance-signals.json` is the open signals register (also on the page as schema.org JSON-LD).
- The [metadata schema](https://cyberdudeuk.github.io/ai-capability-governance/#catalogue) has a worked YAML example for any AI asset.
- Content is under the Open Government Licence v3.0; code under MIT.

## How the repository works

| Path | What it is |
|---|---|
| `index.html`, `styles.css`, `app.js` | The site. The publish workflow deploys it after every check passes |
| `data/` | Open data the page is built from |
| `tools/check_site.py` | 17 static checks; each names the defect it prevents |
| `tools/check_browser.py` | Browser checks in Chrome at 1280, 390 and 320px: no sideways scroll, no console errors, contact form opens the GitHub form |
| `tools/build_signals.py` | Rebuilds the Signals section from the register; never edit that section by hand |
| `tools/health.py` | Weekly health run: review date and signals freshness |
| `tools/digest.py`, `tools/triage.py`, `tools/trials.py` | Estate routines (reports and labels only) |
| `tests/` | Vaccination tests: every check must fail on a deliberate break |
| `ops/automation.yaml` | What runs, when, its tier and what it may change |
| `docs/` | Decisions (ADRs), the defect register, settings checklist and these guides |

## Build and check locally

```
pip install -r requirements.txt
python3 tools/check_site.py
python3 -m unittest discover -s tests -v
node --check app.js
python3 tools/check_browser.py         # needs Chrome; set CHROME to its path
```

## Worked example: certifying a definition an agent will serve

Agents increasingly answer questions from a shared glossary served over MCP. Many semantic-layer products mark each
definition as certified or not (for example NVIDIA Auto Ontology's per-field flag). The H-levels give that flag a
basis: it records which review the definition passed.

| Situation | H-level | Evidence | May an agent call it certified? |
|---|---|---|---|
| An AI drafted the definition and nobody has checked it | H0 or H1 | AI-use note at most | No |
| A second competent person checked it against its source | H2 | Reviewer, date, issues found | Yes, for internal use |
| It will feed public answers, or a named standard rests on it | H3 | Specialist sign-off (for example the data standards owner) | Yes |
| It affects entitlements or decisions about people | H4 or H5 | Panel record, or board approval and a transparency record | Yes, once that evidence exists |

Two rules keep this honest:

1. Record two fields with every definition: who drafted it (`human`, `ai-assisted` or `unknown`) and the review it
   passed (`H0` to `H5`, or `unknown`). A missing value means not certified, never "probably fine".
2. Certified means the definition is endorsed **and** reviewed at H2 or above. Endorsement alone is not review.

An open implementation of rule 2 is `term_lookup` in
[ndl-pubsec-mcp](https://github.com/cyberdudeuk/ndl-pubsec-mcp) (`src/lib/vocab.ts`, function `certify`, in
[pull request 18](https://github.com/cyberdudeuk/ndl-pubsec-mcp/pull/18) until it merges). It returns not certified
for any unknown value.

## Worked example: reviewing an answer an agent built from those definitions

A certified definition does not make the answer certified. An agent that writes a query from definitions (text-to-SQL)
can still choose the wrong join, filter or time period. Review the answer at a level set by what it will be used for.
This mapping is proposed, not policy (issue 16); the working group should confirm it.

| What the answer is used for | Suggested minimum | Why |
|---|---|---|
| Exploring inside the team | H1, self-check | Low impact, easy to reverse |
| Analysis that leaves the team | H2, peer check | Someone other than the asker checks the query |
| Published statistics, or answers released outside the organisation | H3, statistical specialist review | It is a statistical product |
| Casework or decisions about people | H4, or H5 with a transparency record | Decisions about people trigger the top levels |

**Keep the evidence path.** The evidence pack has a field for the data definitions the answer relied on: for each,
record the term, the column it maps to and its review level. Any definition below H2, or with an unknown level, makes
the answer unverified on that point. This is the toolkit's provenance rule, applied to agent answers.

**Transparency and the law.** Screen any text-to-SQL agent used in a public service for an Algorithmic Transparency
Recording Standard record. If its answers feed significant decisions about people, the UK GDPR's automated
decision-making rules (Articles 22A to 22D, in force from 5 February 2026) apply unless a person with the authority
and understanding to change the outcome genuinely considers it. A reviewer who only approves what the agent produced
is not meaningful human involvement. See the ICO's guidance on automated decision-making in the Resources section.

## Routines, and how a person stays in control

Every workflow is listed in `ops/automation.yaml` with a tier from 0 (observe) to 3 (person only). Nothing merges
itself. The kill switch is the repository variable `AUTOMATION` set to `off`. Near misses go in the occurrence form,
without blame. The weekly signals scan runs outside the repository and proposes its update as a pull request.

Back: [the intermediate guide](intermediate.md).
