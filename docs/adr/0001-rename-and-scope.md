# ADR 0001: Rename to ai-capability-governance and become BOT's public edition

Status: accepted, 8 November 2026 (owner decision).

## Context

The repository was `cyberdudeuk.github.io`, the account's root user site, holding the Public AI Utility Toolkit. The
owner's internal BOT AI Agent Governance Toolkit (a govukOS app) covers the same themes. The owner wants the root address
as a launchpad and showcase for all projects, and the toolkit to be a project in its own right like the others.

## Decision

- Rename the repository to `ai-capability-governance`. The site moves to https://cyberdudeuk.github.io/ai-capability-governance/.
- The site becomes the public edition of BOT: **AI Capability Governance and Implementation**. Only public-source,
  public-safe content comes here. BOT's internal briefings, PMO and Private Office pages, films and deck stay out.
- A new `cyberdudeuk.github.io` repository becomes the launchpad and redirects the old root to this site.
- The site keeps its own design system; it is a published site, not a govukOS app.

## Consequences

- Links to the bare root address no longer reach the toolkit until the launchpad exists; the launchpad points here.
- GitHub redirects the old repository address, so clones and issue links keep working.
