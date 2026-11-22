# Content classification: the RAIDU merge, 22 November 2026

Release 3.4.0 adds material from the Responsible AI and Data Use (RAIDU) work to the playbook. This record works like
[the 18 November record](content-classification-2026-11-18.md): it says what was published, what was changed on the
way in, and what was withheld and why. Every count below comes from the source data. None is estimated.

## How each item was screened

1. **Unresolved items are withheld.** Items graded U (unresolved) in the source are left out.
2. **Internal-only items are withheld.** If every source an item cites is internal (meeting and community-call notes,
   working papers, project records), the item is left out. Items with at least one public source are kept.
3. **Grades are kept.** Each published item carries its evidence grade in words:
   - A: **Verified**
   - B: **Corroborated**
   - C: **Reported**
   - P: **Proposed**

   Proposed items are design proposals for review. They are not policy or established practice, and the chapters say so.
4. **Clean text only.** Each item is taken from its plain-text field, not from its formatted copy. Several other
   things are removed:
   - cross-references to sections of the source (such as "§4.1") and to its internal milestones ("Source of M3");
   - attributions to the working conversation;
   - wording about "this build".
5. **Links are checked.** All 155 cited links were checked on 22 November 2026:
   - 145 answered;
   - one has gone (a UK Parliament committee publication) and is shown as plain text without a link;
   - the rest refuse automated checks and are linked as published.
6. **Glossary terms are deduplicated.** 121 candidate terms came from the source glossary and vocabulary. A term was
   added only if the portal did not already define it and its definition says something; 112 were added, taking the
   glossary from 62 to 174.

## Published: nine chapters

| Chapter | Part | Source collection | Items |
|---|---|---|---|
| Human oversight principles | Assure and govern | principles | 10 of 10 |
| Oversight controls | Assure and govern | controls | 30 of 30 |
| Measuring oversight | Assure and govern | signals; vocabulary (conformance tiers) | 20 of 20; 3 tiers |
| Human-side risks and priorities | Assure and govern | risks; priorities | 26 of 26; 25 of 25 |
| Verifying AI-assisted work | Assure and govern | practices; failures | 34 of 53; 3 of 4 |
| Oversight runbook and templates | Operate and oversee | runbook; templates | 12 of 12; 6 of 6 |
| Neuroinclusive AI at work | People and adoption | inclusion; characteristics; inclusion debates | 15 of 15; 6 of 6; 6 of 6 |
| Oversight crosswalk | Reference | crosswalk | 17 of 17 |
| Obligations register | Reference | obligations | 164 of 164 |

Of the 53 practices, 19 were withheld under rule 2, along with one of the four failure patterns and 48 of the 111
glossary terms.

## Redacted on the way in

- One risk row ended with its conversation provenance: "the chat's own warning. (Insight I21, Claude's reading)". The
  row now states the risk itself. This is recorded as defect D-40, and check S22 now bans that kind of wording.
- The governance templates are skeletons. Each one says to take it to your data protection officer, equality lead and
  legal adviser.

## Withheld whole collections, with reasons

| Reason | Collections (items) |
|---|---|
| **Already covered by an existing chapter**, so publishing would duplicate it | capability classes (6), lifecycle (12), artefacts (24), registers (12), adoption (8), supply chain (9), user groups (8), assessment questions (60), dashboard domains (10), jurisdictions (9), agents (6) |
| **Overlaps the oversight controls just published.** Kept back to avoid two control lists; to be reviewed for a merge into *Oversight controls* | safeguards (37) |
| **About the RAIDU work itself, not about oversight**: its build status, change history, defects, backlog, requirements, information architecture, visual scan, review panels, reading list and routing to named offices | blockers (19), history (33), defects (37), backlog (6), requirements (24), information architecture (116), visual scan (72), visuals (9), council (42), library (11), products (10), routing (18), guidance on using its evidence register (23) |
| **Evidence that names individuals or is not yet resolved.** To be reconsidered item by item after re-verification | evidence (132, of which 33 unresolved), inclusion evidence (32, all unresolved) |
| **Internal sources**: notes of cross-government community calls, and findings drawn from them | field reports (10), findings (20) |
| **Vendor-specific.** The portal is vendor-neutral | tool catalogue (16), vendor overlays (5), catalogue fields (81) |
| **A technical schema for a product that has not been built** | oversight event dictionary (52) |

## Limits of this classification

- The screen was automatic, and the result was read once by eye. Rule 2 judges a source by how it is cited, so an
  item that cites a public page in an unusual way may have been withheld wrongly.
- The obligations register was researched in October 2026. Guidance changes, so check the source before relying on
  any entry.
