# Repository settings: owner checklist

The build sets everything it can as files in the repository. These settings can only be changed in the repository
settings. Status as at 8 November 2026; "Set" means it was set through the GitHub API in the build session and read back.

| Setting | Value | Where | Status |
|---|---|---|---|
| Rename | `ai-capability-governance` (ADR 0001). GitHub redirects the old repository address, not the old Pages root | Settings, General | See status below |
| Description | AI Capability Governance and Implementation: public guidance, tools and weekly signals for governing AI and AI agents in UK public services. Prototype, not official guidance. | About | See status below |
| Website | https://cyberdudeuk.github.io/ai-capability-governance/ | About | See status below |
| Topics | ai, ai-governance, ai-assurance, responsible-ai, agentic-ai, ai-agents, data-governance, human-in-the-loop, transparency, public-sector, uk-government, open-standards, accessibility | About | See status below |
| Features | Issues on; Discussions on; Wiki off | Settings, General | See status below |
| Merge | Squash merging only; delete branches after merge; suggest updating branches | Settings, General | See status below |
| Pages | Source: GitHub Actions (the publish workflow, `pages.yml`, deploys only the site files after every check passes) | Settings, Pages | Owner to confirm: the Pages settings cannot be read or changed through the API from the build session |
| Ruleset "Protect main" | Block deletion and force pushes; require linear history; require a pull request; require the Checks status | Settings, Rules | See status below |
| Private vulnerability reporting | On | Settings, Security | See status below |
| Dependabot alerts and security updates | On | Settings, Security | See status below |
| Secret scanning and push protection | On | Settings, Security | See status below |
| CodeQL | Uses `.github/workflows/codeql.yml` (advanced setup); leave default setup off | Settings, Security | Owner to confirm default setup is off |
| Actions permissions | Allow GitHub-owned actions and `ossf/scorecard-action`, pinned to a full commit (ADR 0002) | Settings, Actions | Owner to set: not reachable through the API from the build session |
| Labels | Run the Labels workflow once | Actions, Labels | Runs automatically when `.github/labels.yml` reaches main |

No email address belongs in any of these. Contact is by the contact form only.

## Status

Filled in after the settings were applied and read back.
