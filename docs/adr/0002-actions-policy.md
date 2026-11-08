# ADR 0002: Plain commands in workflows; third-party actions only where unavoidable, pinned

Status: accepted, 8 November 2026. Follows the estate pattern (D-018 in dam-capability-playbooks, ADR 0005 there).

Workflows check out code with plain git and run the runner's own Python and Node.js. The only actions used are
GitHub-owned ones and OpenSSF Scorecard, each pinned to a full commit SHA with its release tag in a comment. Dependabot
proposes updates; a person checks the commit against its tag before merging.
