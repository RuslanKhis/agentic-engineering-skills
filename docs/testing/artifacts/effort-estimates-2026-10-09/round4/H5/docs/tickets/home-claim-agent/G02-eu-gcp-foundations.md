---
goal: G02
title: Stand up EU dev/staging projects and confirm model residency and prices
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 20-32
  review_and_verify: 6-10
  total: 26-42
  calendar_waits: EU projects and Vertex quota from the cloud platform team
  wait_days: 3-5
owner: Eng E
status: ready
---

# G02 Stand up EU dev/staging projects and confirm model residency and prices

## Outcome

Dev and staging exist in one confirmed EU region with least-privilege identities. We know whether the pinned model is served on the regional Vertex endpoint, and the cost figures carry sources. Implements D6, D7, D8 and I7.

## Scope

- In: `infra/` (Terraform or reviewed runbooks): projects, `gcp.resourceLocations`, `gateway-sa`, `submitter-sa`, Cloud SQL, photo bucket, Tasks queue, empty Secret Manager entries, static egress IP, budget alerts. Updates D7 and the cost section of the design.
- Out: Production projects (G23, G25); application code.
- Depth: Production least privilege. Floor: no keys in files; EU only; budget alerts exist. CMEK only if policy requires it (record the answer).

## Acceptance

- [ ] A readback lists every resource in the chosen EU region and nothing elsewhere
- [ ] One call to the pinned model on the regional EU endpoint succeeds (or the fallback pin is chosen and recorded); a config test rejects a global endpoint
- [ ] Each service account's roles match the design table; `gateway-sa` cannot read the Guidewire secret
- [ ] Prices for the model, SDP, Cloud SQL and Tasks are recorded in the design with URL and access date

Verification: Authorised live on the dev project; readback commands recorded in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G02-eu-gcp-foundations.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
