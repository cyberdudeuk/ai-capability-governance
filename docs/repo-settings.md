# Repository settings

These settings live in the repository settings, not in files. They were applied in the browser on 8 and 9 November 2026
and read back through the API or the settings pages on 9 November 2026. The build session cannot change them through the
API (the connection refuses settings writes), so any later change is made by hand and recorded here.

| Setting | Value | Status (9 November 2026) |
|---|---|---|
| Rename | `ai-capability-governance` (ADR 0001). GitHub redirects the old repository address, not the old Pages root | Done |
| Description | AI Capability Governance and Implementation: public guidance, tools and weekly signals for governing AI and AI agents in UK public services. Prototype, not official guidance. | Read back |
| Website | https://cyberdudeuk.github.io/ai-capability-governance/ | Read back |
| Topics | accessibility, agentic-ai, ai, ai-agents, ai-assurance, ai-governance, data-governance, human-in-the-loop, open-standards, public-sector, responsible-ai, transparency, uk-government | Read back |
| Features | Issues on; Discussions on; Wiki off | Read back |
| Merge | Squash only; delete branches after merge | Read back |
| Pages | Source: GitHub Actions. `pages.yml` deploys only the site files after every check passes | Read back |
| Ruleset "Protect main" | Default branch: block deletion and force pushes; require a pull request (no approvals, as the owner is the only maintainer); require the `check` status from GitHub Actions; no bypass. Linear history is not a separate rule: squash-only merging already gives it | Read back (ruleset 26820030) |
| Security | Dependency graph (the Dependency review check fails without it), Dependabot alerts, Dependabot security updates, private vulnerability reporting, secret scanning and push protection all on | Read back |
| CodeQL | `.github/workflows/codeql.yml` (advanced setup); default setup off | Read back |
| Actions | Allow GitHub-owned actions and `ossf/scorecard-action@*` only; require actions pinned to a full commit SHA (ADR 0002); default token read-only; Actions may not create or approve pull requests | Read back |
| Labels | Run by the Labels workflow when `.github/labels.yml` changes on main | Automatic |

No email address belongs in any of these. Contact is by the contact form only.

## If a workflow is blocked

A new third-party action fails to start until it is added to the allowed list in Settings, Actions. Add it there and
in ADR 0002 in the same change. Every workflow declares its own permissions, so the read-only default token does not
limit them. The release workflow asks for `contents: write` itself, and the ruleset only covers the default branch, so
version tags and releases still work.

## Read back on 8 November 2026, before any change

Name `cyberdudeuk.github.io`; Wiki on; Discussions off; merge commits, squash and rebase all allowed; delete branch on
merge off; topics ai, coding-agent, deve, metadata, software-engineering; secret scanning and push protection on;
Dependabot security updates off; no rulesets; Pages deployed by a workflow from `main`.
