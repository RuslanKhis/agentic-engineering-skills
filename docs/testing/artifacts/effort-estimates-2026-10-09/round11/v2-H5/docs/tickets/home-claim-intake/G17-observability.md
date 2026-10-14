---
goal: G17
title: On-call can see whether claims are being filed and find the session behind an alert
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G08, G16]
phase: 1
profile: production
estimate:
  hands_on: 12-19
  review_and_verify: 4-6
  total: 16-25
  calendar_waits: none
owner: Eng C
status: proposed
---

# G17 On-call can see whether claims are being filed and find the session behind an alert

## Outcome

Implements D14: content-free OpenTelemetry, SLIs for I3, I4, T1 and T2 and
alerts. Dashboards and the runbook walkthrough are G35. Handoff: 1 h from
Eng B on operation states.

## Scope

- In: telemetry set-up with one provider per process, IDs on every span,
  burn-rate and uncertain-operation alerts, business metric for call-back
  rate. (A2 and A4 moved to G35.)
- Out: production sampling into evaluation (phase 2 G29).
- Depth: production.

## Acceptance

- [ ] A1 An in-memory exporter test shows one span per agent, tool and logical model call, each carrying session, invocation, draft and operation IDs and no message content.
- [ ] A3 An operation in `create_unknown`, `draft_created` or `needs_ops` for over 15 minutes pages on-call in staging; a burn-rate alert exists for the filing SLI.

Verification: offline exporter test; authorised staging alert test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-observability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
