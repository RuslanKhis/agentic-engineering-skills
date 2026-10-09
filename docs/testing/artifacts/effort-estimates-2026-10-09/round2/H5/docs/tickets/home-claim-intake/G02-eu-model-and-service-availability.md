---
goal: G02
title: EU model, quota and protection-service availability decided, with dated sources
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [deploy-adk-on-google-cloud, protect-adk-sensitive-data]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 8–14
  review_and_verify: 4–6
  total: 12–20
  calendar_waits: Vertex AI EU regional quota request 1–2 weeks (does not block the decision)
owner: ML
status: ready
---

# G02 EU model, quota and protection-service availability decided, with dated sources

## Outcome

D4, D5 and D10 become decided or are revised: the chosen EU region serves `gemini-3.8-flash` (and fallback `gemini-3.5-flash`) with image input, data-use terms are recorded, Model Armor and SDP are available in-region, and prices are dated for the cost formula.

## Scope

- In: Official docs lookup with URL and access date; 20 bounded live calls per model in an authorised sandbox project (text + image); record token counts for a typical turn and photo; refresh the lifecycle snapshot date; write `docs/architecture/decisions/eu-model-and-region.md`.
- Out: Quality measurement (G10/G16); provisioning environments (G04).
- Depth: Production: every provider fact cited and dated. Floor: pinned model IDs, no `global` endpoint, call cap on the live check.
- Route: Investigation stops when region, model, fallback, protection services and price per 1M tokens are recorded with sources, or when the preferred region fails, in which case the next EU region is tried once and the decision escalated.
- Supporting skills: `deploy-adk-on-google-cloud` (Cloud Run vs Agent Runtime availability and region for D4); `protect-adk-sensitive-data` (SDP and Model Armor regional availability for D10)
- Execution scope: Read-only docs plus ≤ 50 model calls in a sandbox project the user names; no IAM changes.

## Acceptance

- [ ] Decision note names region, agent model, reader model, fallback, judge candidate, each with lifecycle date and source URL + access date
- [ ] Live check: text and 4-image request succeed on the EU regional endpoint; request log shows the regional host, not global
- [ ] If the preferred model is unavailable in-region, the note records the alternative and the design rows D4/D5 to update

Verification: Bounded live check in the sandbox project, ≤ 50 model calls total, cost recorded.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-eu-model-and-service-availability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
