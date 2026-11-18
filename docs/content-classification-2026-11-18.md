# Content classification: agent governance playbook, 18 November 2026

The playbook (in `index.html` since 3.3.0; `playbook.html` redirects there) is the public edition of an internal AI agent governance toolkit of 87 chapters in 12 parts. This record says what was published, what was withheld and why. It is the decision record that check S23 holds the data to.

## Method

1. Rendered every chapter of the source in a headless browser and read its text and structure.
2. Searched every chapter for internal page names, internal document names, the former office name, team names, personal names and email addresses.
3. Classified each chapter: **public**, **public with redaction** or **withheld**. Withheld means it contains material that is internal, organisation-specific, a film or deck, or superseded by something the public site already does.
4. Rebuilt public chapters as plain semantic content (headings, cards, lists, tables) with the source's styles, internal links and interactive controls removed. Only absolute https links survive.
5. Kept every "illustrative" label. Figures in the control tower, cost lab and maturity chapters are illustrative in the source and stay labelled so. Named people in the illustrative control tower are invented.
6. Checks S21 to S24 hold the result: the page is generated from the data, no internal wording is published, every chapter is classified once and every link lands.

No source file, blueprint, deck or film is in this repository. The extraction scripts ran outside it.

## Summary

| Decision | Chapters |
| --- | --- |
| Public | 64 |
| Public with redaction | 12 |
| Withheld or merged | 11 |

## Withheld

| Chapter | Part | Reason |
| --- | --- | --- |
| AI tool catalogue | Decide and prioritise | Organisation-specific approved-tool statuses and links to internal pages; publishing them would read as endorsement. |
| Analytics, estimators & dashboards | Decide and prioritise | Its charts count entries in the withheld tool catalogue; the estimators it links to are published in "Cost, value and investment". |
| Blueprint coverage | Product documentation | Coverage map of internal source documents and blueprints, which are not published. |
| Portal specification trace | Product documentation | Traces requirements from an internal specification document. |
| Knowledge graph | Knowledge and navigation | Interactive graph of the internal edition; replaced by the generated knowledge map in this playbook. |
| Portal & site map | Knowledge and navigation | Map of the internal edition, including internal pages. The public playbook has its own contents and drawer. |
| Guided tours | Knowledge and navigation | Guided tours route through internal pages; the home page personas and journeys replace them. |
| Media centre | Knowledge and navigation | Films and decks: never kept in a repository (owner rule). They stay in the media library outside GitHub. |
| Self-assurance console | Knowledge and navigation | Self-test console of the internal edition; the public site runs its own checks in CI (see Transparency). |
| Sources & blueprints | Reference | Lists internal source documents. Public sources are in the resource library on the home page. |

## Published

| Part | Chapter | Decision | Redaction |
| --- | --- | --- | --- |
| Start here | Overview | Public with redaction | Removed the source portal status line and the reference to its media centre. |
| Start here | Can I use AI for this? | Public with redaction | "This part of the Hub" became "this part of the playbook"; catalogue references point to the reader's own organisation's catalogue. |
| Start here | How to use this guide | Public with redaction | Removed the media centre and self-assurance console from the part summary. |
| Start here | The playbook | Public | None |
| Start here | Capability domains | Public | None |
| Decide and prioritise | Evidence before assertion | Public | None |
| Decide and prioritise | Use cases & evidence | Public | None |
| Decide and prioritise | Public sector case library | Public | None |
| Decide and prioritise | Classify & assess | Public | None |
| Decide and prioritise | Criticality & gates | Public | None |
| Decide and prioritise | Assurance tiers | Public | None |
| Design and build | Lifecycle & templates | Public | None |
| Design and build | Capability classes | Public | None |
| Design and build | Skill studio | Public | None |
| Design and build | Agent assurance X-ray | Public | None |
| Design and build | Connectors, MCP & integrations | Public | None |
| Design and build | Architecture & quality | Public | None |
| Design and build | Knowledge foundation | Public | None |
| Design and build | Autonomy boundaries | Public | None |
| Assure and govern | Control plane & evidence | Public with redaction | Catalogue reference points to the reader's own organisation's catalogue. |
| Assure and govern | Data & information governance | Public | None |
| Assure and govern | Architecture of trust | Public | None |
| Assure and govern | Governance operating model | Public | None |
| Assure and govern | Risks & mitigations | Public | None |
| Assure and govern | Registers & lifecycle | Public | None |
| Assure and govern | Internal ATRS registry | Public | None |
| Assure and govern | Failure & recovery | Public | None |
| Operate and oversee | Portfolio control tower | Public | None |
| Operate and oversee | Monitoring & reassessment | Public with redaction | Watch-list item now refers to the service atlas, not the withheld catalogue. |
| Operate and oversee | Agent journey | Public | None |
| Operate and oversee | Agent employment | Public | None |
| Operate and oversee | Public service impact | Public | None |
| Operate and oversee | Observatory & barometer | Public | None |
| Fund and buy | Cost, value & investment | Public | None |
| Fund and buy | FinOps & models | Public | None |
| Fund and buy | Commercial & suppliers | Public | None |
| Fund and buy | Dependency & exit | Public | None |
| People and adoption | Multidisciplinary teams | Public | None |
| People and adoption | AI service team | Public | None |
| People and adoption | Roles & pathways | Public | None |
| People and adoption | Capability academy | Public | None |
| People and adoption | Capability & maturity | Public | None |
| People and adoption | Inclusive adoption | Public | None |
| People and adoption | Adoption journey | Public | None |
| People and adoption | Agent rollout | Public | None |
| People and adoption | Community engagement | Public | None |
| People and adoption | Operating model | Public | None |
| People and adoption | Adoption & change model | Public with redaction | Removed links to internal worked-example pages and the films they pointed to. |
| Live pilot | The pilot in one view | Public | None |
| Live pilot | What it tests | Public | None |
| Live pilot | Candidate selection | Public | None |
| Live pilot | Pilot roles | Public | None |
| Live pilot | Assurance model | Public | None |
| Live pilot | Journey & ceremonies | Public | None |
| Live pilot | Communications | Public | None |
| Live pilot | Success & feedback | Public | None |
| Live pilot | Decision & toolkit | Public | None |
| Product documentation | Product requirements | Public with redaction | Source attribution reworded: "published guidance and community discussion", not internal documents. |
| Product documentation | Functional & technical spec | Public | None |
| Product documentation | Solution architecture | Public with redaction | "Blueprint-derived data" became "source-derived data"; the evidence boundary is this playbook's. |
| Product documentation | High-level design | Public with redaction | The provenance entity is a published source, not an internal blueprint. |
| Product documentation | Low-level design | Public | None |
| Product documentation | Theory of change | Public | None |
| Product documentation | Personas & journeys | Public with redaction | Source attribution reworded as above. |
| Product documentation | Gov.uk AI resources | Public with redaction | A pointer to the withheld sources chapter now points to the home page resource library. |
| Knowledge and navigation | Thesaurus | Public | None |
| Knowledge and navigation | Taxonomies & ontology | Public | None |
| Knowledge and navigation | Platforms & repositories | Public with redaction | Removed the claim that the guide's shell follows the GOV.UK Design System (the public site has its own design). |
| Knowledge and navigation | Federated guidance service | Public | None |
| Deploy for real | Service atlas | Public | None |
| Deploy for real | Case generator | Public | None |
| Deploy for real | Worked examples | Public | None |
| Deploy for real | What this does not cover | Public | None |
| Reference | UK nations | Public | None |
| Reference | International | Public | None |
| Reference | Pace & parity | Public | None |

## Known limits of this edition

- Interactive widgets in the source (stage selectors, sliders, the tier finder, the case generator and the cost estimators) are published as their default state. Only the route tool is ported as working code so far; porting the case generator and the cost lab is on the roadmap.
- Chapters describe the source toolkit's own product documents (PRD, specification, architecture). They are kept because the method is reusable, not because the public site implements every requirement in them.
- Product and vendor names are examples, not endorsements or procurement decisions.

## Review

Reviewed with the rest of the site every quarter; next review 18 February 2027. Corrections: use the content correction issue form.

## Update, 3.3.0

The playbook glossary chapter is merged into the portal glossary, so the portal has one glossary (62 terms). It is listed with the withheld chapters as "merged", with its reason. 76 chapters are now published.
