---
goal: G02
title: Confirm the EU model, region, quota and price
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [adk-release-engineering, deploy-adk-on-google-cloud]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 9-15
  review_and_verify: 3-5
  total: 12-20
  calendar_waits: Vertex AI quota increase request (days to weeks); Google account team answer on data-processing terms
owner: ML engineer
status: ready
---

# G02 Confirm the EU model, region, quota and price

## Outcome

The pinned model and region are confirmed with dated sources, or a replacement is chosen before code depends on them. Implements D2, D6, O2; A7, A14.

## Scope

- In: ADR `adr-002-model-and-region.md`: refresh the model lifecycle snapshot; confirm `gemini-3.8-flash` availability on a Vertex AI endpoint in europe-west3 (or the nearest EU region), image input support, data-processing location terms, quotas, prices per token and image; Model Armor EU availability; a 20-call smoke test in the dev project.
- Out: Prompt quality (G07, G09).
- Depth: Production: provider facts enter the design only with source URL and date.
- Route: Vertex AI regional endpoint configuration in the ADK model setting; no code beyond a smoke script.
- Supporting skills: `adk-release-engineering` (model and judge pins and the retirement calendar); `deploy-adk-on-google-cloud` (region and quota for the serving project)
- Execution scope: Needs a dev GCP project with Vertex AI enabled and permission to make 20 calls.

## Acceptance

- [ ] ADR cites each provider fact with URL and access date
- [ ] Smoke test: 20 calls (text + image) succeed from the EU endpoint with the pinned ID; no alias used
- [ ] If the model is unavailable in the EU, a replacement is chosen with its lifecycle date beyond 2027-09
- [ ] Symbolic cost formula from the design filled with dated prices

Verification: Bounded live: dev project, at most 20 model calls, recorded output.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-eu-model-and-region-check.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
