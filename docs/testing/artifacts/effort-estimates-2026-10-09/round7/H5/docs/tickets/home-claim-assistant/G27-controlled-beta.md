---
goal: G27
title: Real customers file claims; decide GA
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-observability, adk-operational-guardrails]
blocked_by: [G20, G22, G24, G25, G26, W2]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 24-36
  review_and_verify: 6-10
  total: 30-46
  calendar_waits: two-week controlled beta
  wait_days: 10
owner: Eng B
status: blocked
---

# G27 Real customers file claims; decide GA

## Outcome

A two-week controlled beta to a small share of German customers, after DPIA sign-off and security remediation, ending in a go/no-go for GA on the agreed date.

## Scope

- In: traffic share, canary thresholds, exit criteria (minimum claims, SLOs met, zero duplicates, no open high findings), go/no-go record.
- Out: phase 2.
- Depth: hosted.

## Acceptance

- [ ] DPIA signed (W2) and G24 closed before the first real customer
- [ ] Exit criteria met or GA moved with a recorded reason
- [ ] No duplicate or misattributed claim in the beta

Verification: Production, limited share.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G27-controlled-beta.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
