---
goal: G20
title: A limited customer pilot shows the agent is safe and better than the form, and GA is approved
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [adk-agent-evaluation, adk-agent-security, adk-release-engineering]
blocked_by: [G09, G12, G13, G14, G17, G18]
phase: 1
profile: production
estimate: 80-120 h
status: blocked
---

# G20 A limited customer pilot shows the agent is safe and better than the form, and GA is approved

## Outcome

A feature-flagged pilot with a bounded customer cohort compares completion, missing-info callbacks and time to file with the form baseline, confirms SLIs and invariants in production, and produces a GA go/no-go record with DPO and security sign-off. Implements Outcome measurement; all invariants in the design.

## Scope

- In: Pilot cohort definition, comparison report, reviewed incident list, GA checklist (DPIA signed, threat model signed, SLOs met, rollback rehearsed).
- Out: Second market (P2-06).
- Depth: Build: production evidence; no claim of improvement without the comparison.
- Route: Feature flag in the portal; dashboards from G17; dev-set refresh from reviewed pilot sessions.
- Prerequisites: G09, G12, G13, G14, G17, G18; DPIA sign-off; business approval of the cohort.
- Supporting skills:
  - `adk-agent-evaluation`: pilot cases reviewed into the dev set
  - `adk-agent-security`: GA security sign-off
  - `adk-release-engineering`: GA release manifest
- Execution scope: Requires business, DPO and security approval and production access.

## Acceptance

- [ ] Pilot report compares agent and form cohorts on completion and missing-info callbacks with sample sizes and confidence stated.
- [ ] Every invariant I1–I10 has production evidence or a recorded exception approved by its owner.
- [ ] Forbidden: GA traffic is not enabled without the signed go/no-go record.

Verification: Authorised production pilot.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-pilot-and-ga-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
