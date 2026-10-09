---
goal: G13
title: On-call can see failures, cost and uncertain submissions and act on them
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [deploy-adk-on-google-cloud]
blocked_by: [G04, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 26–42
  review_and_verify: 14–22
  total: 40–64
  calendar_waits: none
owner: E3
status: blocked
---

# G13 On-call can see failures, cost and uncertain submissions and act on them

## Outcome

Traces, metrics and logs with session/invocation/operation IDs, the SLIs from the design, alerts with owners, and runbooks for uncertain submissions, Vertex outage and kill switch. I6.

## Scope

- In: One OTel provider owner in the app; dashboards; alert policies (uncertain age > 1 h, Guidewire error rate, completed-claim ratio drop, cost per claim); runbooks in `docs/runbooks/`.
- Out: Production-to-eval loop (G25).
- Depth: Production: SLOs and alerts. Floor: content capture off.
- Route: ADK spans exported to Cloud Trace in the EU; custom metrics for operations.
- Supporting skills: `deploy-adk-on-google-cloud` (exporter setup on Cloud Run and sink regions)
- Execution scope: Dev and staging.

## Acceptance

- [ ] In-memory exporter test: one span per agent, tool and logical model call, session ID set, no content attributes
- [ ] Synthetic uncertain operation in staging raises the alert and the runbook resolves it
- [ ] Dashboard shows tokens and cost per completed claim

Verification: Offline exporter test; staging alert drill.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-observability-and-runbooks.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
