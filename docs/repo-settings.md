# Repository settings: owner checklist

The build sets everything it can as files in the repository. These settings can only be changed in the repository
settings. Status as at 8 November 2026. The build session could not change any of them: the connection it used refuses every
repository settings write (rename, settings, topics, rulesets, security), so every row below is for the owner.

| Setting | Value | Where | Status |
|---|---|---|---|
| Rename | `ai-capability-governance` (ADR 0001). GitHub redirects the old repository address, not the old Pages root | Settings, General | Owner to set |
| Description | AI Capability Governance and Implementation: public guidance, tools and weekly signals for governing AI and AI agents in UK public services. Prototype, not official guidance. | About | Owner to set |
| Website | https://cyberdudeuk.github.io/ai-capability-governance/ | About | Owner to set |
| Topics | ai, ai-governance, ai-assurance, responsible-ai, agentic-ai, ai-agents, data-governance, human-in-the-loop, transparency, public-sector, uk-government, open-standards, accessibility | About | Owner to set |
| Features | Issues on; Discussions on; Wiki off | Settings, General | Owner to set |
| Merge | Squash merging only; delete branches after merge; suggest updating branches | Settings, General | Owner to set |
| Pages | Source: GitHub Actions (the publish workflow, `pages.yml`, deploys only the site files after every check passes) | Settings, Pages | Owner to confirm: the Pages settings cannot be read or changed through the API from the build session |
| Ruleset "Protect main" | Block deletion and force pushes; require linear history; require a pull request; require the Checks status | Settings, Rules | Owner to set |
| Private vulnerability reporting | On | Settings, Security | Owner to set |
| Dependabot alerts and security updates | On | Settings, Security | Owner to set |
| Secret scanning and push protection | On | Settings, Security | Owner to set |
| CodeQL | Uses `.github/workflows/codeql.yml` (advanced setup); leave default setup off | Settings, Security | Owner to confirm default setup is off |
| Actions permissions | Allow GitHub-owned actions and `ossf/scorecard-action`, pinned to a full commit (ADR 0002) | Settings, Actions | Owner to set: not reachable through the API from the build session |
| Labels | Run the Labels workflow once | Actions, Labels | Runs automatically when `.github/labels.yml` reaches main |

No email address belongs in any of these. Contact is by the contact form only.

## Order to do them in

1. **Rename** the repository to `ai-capability-governance` (Settings, General, Repository name).
2. **Pages**: Settings, Pages, Source: GitHub Actions. Then merge the open pull request; the publish workflow deploys to
   https://cyberdudeuk.github.io/ai-capability-governance/ after every check passes.
3. Description, website, topics, features and merge settings (this table).
4. Security: private vulnerability reporting, Dependabot alerts and security updates (secret scanning and push protection
   were already on, read on 8 November 2026).
5. Ruleset "Protect main", then require the **Checks** status once it has run on main.
6. Create a new public repository named `cyberdudeuk.github.io` for the launchpad (ADR 0001).

## Read back on 8 November 2026, before any change

Name `cyberdudeuk.github.io`; Wiki on; Discussions off; merge commits, squash and rebase all allowed; delete branch on
merge off; topics ai, coding-agent, deve, metadata, software-engineering; secret scanning and push protection on;
Dependabot security updates off; no rulesets; Pages deployed by a workflow from `main`.
