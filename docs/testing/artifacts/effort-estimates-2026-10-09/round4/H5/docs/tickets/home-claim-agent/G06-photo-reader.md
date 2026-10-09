---
goal: G06
title: Photos are described as structured damage observations the customer can correct
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [adk-agent-instructions, adk-agent-security, adk-agent-evaluation]
blocked_by: [G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 30-52
  review_and_verify: 8-14
  total: 38-66
  calendar_waits: none
  wait_days: 0
owner: ML
status: proposed
---

# G06 Photos are described as structured damage observations the customer can correct

## Outcome

Implements D9's reader: a tool-less model call that turns a photo into validated `PhotoObservation` data; instructions inside photos cannot act.

## Scope

- In: `app/photos/reader.py`: one model call, no tools, `output_schema=PhotoObservation` with `refusal`; one repair attempt then 'unprocessed'; code writes observations to the draft; reader instruction versioned; photo set of 60-100 labelled staff-staged and licensed images.
- Out: Use of historical claim photos (waits for DPIA); Model Armor (G32).
- Depth: Production depth. Floor: pinned model; bounded calls; no tool on the reader.

## Acceptance

- [ ] Scripted prose, fenced JSON and schema-valid-but-wrong outputs each produce the designed outcome
- [ ] A photo with written instructions yields observations only and never changes other draft fields
- [ ] Damage-type agreement with labels is reported on the photo set
- [ ] The captured model request shows zero tools and the schema

Verification: Offline scripted tests; bounded live run on Vertex EU ≤ 300 calls on the dev project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G06-photo-reader.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
