---
goal: G12
title: Customer data is minimised, kept 30 days and erasable
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-memory-architecture]
blocked_by: [G05, G07]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 22-36
  review_and_verify: 8-14
  total: 30-50
  calendar_waits: none
owner: Lead
status: blocked
---

# G12 Customer data is minimised, kept 30 days and erasable

## Outcome

Implements D10 and I6, and supplies the DPIA (W1) with its data-flow evidence.

## Scope

- In: Data-flow table per boundary (ingress, model, tools, sessions, GCS, logs, traces, Guidewire), with region. Model Armor screening of user text (fail closed per turn) if G01 confirms EU availability. Retention jobs (30 days, A13). DSAR erasure that waits for pending operations. Structured log schema with IDs only.
- Out: Telemetry exporter config (G16).
- Depth: Build. Old data is not assumed sanitised by new policy.

Supporting skills and why:
- adk-memory-architecture (erasure across sessions, drafts and artifacts)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The erasure request removes sessions, drafts, photos and model copies for that customer, and is held until any PENDING/UNCERTAIN op is terminal (test).
- [ ] Retention job deletes 31-day-old abandoned drafts and photos, and keeps a 29-day-old one.
- [ ] A Model Armor outage (fake) fails the turn closed with the designed message. No unscreened text reaches the model.
- [ ] The data-flow table lists an EU region for every store and processor, or flags the gap.

Verification: Offline tests with fakes. The DPIA evidence is reviewed by the Lead.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-sensitive-data-retention-erasure.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
