---
goal: G01
title: Confirm platform, model and EU availability facts, and request every external wait on day 1
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [deploy-adk-on-google-cloud, adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 6-10
  review_and_verify: 2-4
  total: 8-14
  calendar_waits: none
owner: Lead
status: ready
---

# G01 Confirm platform, model and EU availability facts, and request every external wait on day 1

## Outcome

Turns the provisional facts behind D7, D8 and D10 into dated, sourced facts or a recorded fallback, and starts every external wait so none of them gates the schedule late (O2, O4, O5).

## Scope

- In: A decision note `docs/architecture/evidence/G01-platform-facts.md` (proposed path) with URL and access date for each of: `gemini-3.8-flash` in the chosen EU Vertex region with image input and `output_schema`; Cloud Run, Cloud SQL, Cloud Tasks, Model Armor and SDP in that region; CIAM token claims (stable customer ID, audience, signing keys). Requests sent for W1 (DPIA), W2 (Guidewire sandbox), W4 (Vertex quota), W5 (GCP projects) and the W3 pen-test slot.
- Out: Provisioning (G04). The Guidewire API contract (G02).
- Depth: Discovery only. Stops when every item has a source or a named fallback. The model choice uses the `model-lifecycle-*.json` table refreshed from the official pages, not memory.

Supporting skills and why:
- deploy-adk-on-google-cloud (region and service availability)
- adk-tool-auth-and-secrets (CIAM token claims)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Every fact in the note has a URL and an access date. Anything unverifiable is marked provisional, with its fallback (e.g. `gemini-3.5-flash` and a migration before 2027-05-19).
- [ ] The requests for W1, W2, W4 and W5 and the W3 booking exist, each with an owner and a date. Their real lengths are written back into the plan's schedule block if they differ.
- [ ] If the model or Model Armor is unavailable in the EU, D8/D10 in the design are updated and marked accordingly. The design must not silently keep an unavailable choice.

Verification: Document review against the official pages. No cloud resources are created. Bounded live check only if authorised: one Vertex EU call with an image, under a call cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-platform-model-discovery.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
