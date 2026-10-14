---
goal: G20
title: The system holds a storm-day peak and degrades to the form, not to errors
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [safe-api-tool-calls, adk-operational-guardrails]
blocked_by: [G18, W5]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 20-30
  review_and_verify: 6-10
  total: 26-40
  calendar_waits: none on this goal; waits on W5 before it
owner: Eng B
status: blocked
---

# G20 The system holds a storm-day peak and degrades to the form, not to errors

## Outcome

A bounded load and resilience test on staging at A5's storm peak (200
concurrent conversations) with Guidewire non-prod in its agreed window,
measuring latency, tokens and cost per submitted claim, and game days for a
Guidewire outage and a model quota exhaustion.

## Scope

- In: load script with synthetic customers; Vertex quota check and request;
  executor concurrency cap tuned to Guidewire's limit; cost per claim from
  measured tokens and the price on the test date; findings and the
  production budget proposal for finance (A6).
- Out: tuning work (phase 2) unless a target is missed.
- Depth: production.

## Acceptance

- [ ] At the peak, p95 turn latency and the submission ratio meet A14 or the gap is written with a fix.
- [ ] Guidewire outage: drafts confirm and queue; all complete after recovery with no duplicates.
- [ ] Model quota exhausted: customers get the form link; no 5xx storm.
- [ ] Measured cost per submitted claim recorded against A6.

Verification: authorised staging load test with request, time and cost limits
declared beforehand.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-load-resilience.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
