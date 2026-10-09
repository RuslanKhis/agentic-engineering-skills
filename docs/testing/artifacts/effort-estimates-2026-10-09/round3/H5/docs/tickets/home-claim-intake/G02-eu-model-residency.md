---
goal: G02
title: Confirm the pinned Gemini model and protection services run in an EU region for our use
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [protect-adk-sensitive-data]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 5-8
  review_and_verify: 1-2
  total: 6-10
  calendar_waits: Vertex AI EU quota request
owner: ML
status: ready
---

# G02 Confirm the pinned Gemini model and protection services run in an EU region for our use

## Outcome

Settles O2 for D8 (residency) and D9 (`gemini-3.8-flash` on a regional EU Vertex endpoint).

## Scope

- In:
  - Confirm `gemini-3.8-flash` on europe-west3 or europe-west4, with image input and `output_schema` support
  - Quotas and dated EU prices
  - Model Armor and SDP EU locations
  - Refresh the lifecycle table date; name a fallback model if unavailable
  - Draft `app/config/release.yaml` manifest with pinned IDs
- Out: Screening implementation (G16); eval runs (G07)
- Depth: Discovery; at most 20 live requests on synthetic inputs.

## Acceptance

- [ ] Sources cited with access dates for each fact
- [ ] One successful EU-regional call with an image and a response schema
- [ ] A named fallback model and its lifecycle date if the preferred model is not available in the EU region

Verification: Bounded authorised live calls in a non-production project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-eu-model-residency.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
