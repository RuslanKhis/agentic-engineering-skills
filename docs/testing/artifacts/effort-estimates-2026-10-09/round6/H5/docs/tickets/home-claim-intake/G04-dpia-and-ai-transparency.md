---
goal: G04
title: Have the DPIA signed and the retention and AI-notice rules settled
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 8-12
  review_and_verify: 3-5
  total: 11-17
  calendar_waits: DPO review and DPIA sign-off
  wait_days: 15-25
owner: Dev E
status: ready
---

# G04 Have the DPIA signed and the retention and AI-notice rules settled

## Outcome

The DPO has the data-flow inventory and signs the DPIA, fixing retention, lawful basis, photos of people and the AI Act Art. 50 notice wording. Implements D8, D14, I6; Q12; open decision 3; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Data-flow inventory from the design's data table and sinks; special-category handling (injury goes to a human); retention periods; transparency notice text.
- Out: Implementing retention jobs (G15) and UI notice (G22).
- Depth: Production; floor: no real data used before sign-off except the approved anonymised extract (G12).

## Acceptance

- [ ] Inventory covers every store and telemetry sink in the design.
- [ ] DPO sign-off, or its conditions, recorded with date.
- [ ] Design D14 and Q12 updated with the agreed periods and notice text.

Verification: Document review; sign-off record.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-dpia-and-ai-transparency.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
