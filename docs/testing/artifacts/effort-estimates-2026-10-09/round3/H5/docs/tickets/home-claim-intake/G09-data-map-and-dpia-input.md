---
goal: G09
title: The DPO has what they need to sign off the pilot
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 12-20
  review_and_verify: 3-5
  total: 15-25
  calendar_waits: DPO workshop scheduling
owner: Eng E
status: ready
---

# G09 The DPO has what they need to sign off the pilot

## Outcome

Implements the D8 analysis; feeds O4 and O5.

## Scope

- In:
  - Data map across ingress, model context, tool arguments/results, session events, photos, ledger, logs, traces
  - Content-capture policy for telemetry; logging filter specification
  - Retention proposal; DPIA technical annex; AI-interaction disclosure text proposal
  - Malware scanning approach for uploads
- Out: Building screening, retention and erasure (G16)
- Depth: Documents plus a logging filter specification; no real data.

## Acceptance

- [ ] DPIA annex submitted, with every data class owned
- [ ] Open retention and AI Act questions logged with owners
- [ ] No data class flows to a sink without a stated policy

Verification: DPO receipt of the submission; document review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-data-map-and-dpia-input.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
