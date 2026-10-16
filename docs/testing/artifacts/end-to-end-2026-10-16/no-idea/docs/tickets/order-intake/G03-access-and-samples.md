---
goal: G03
title: The IT firm grants the access the pilot needs and 50 paired samples exist
design: ../../architecture/order-intake.md
plan: ../../plans/order-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [deploy-adk-on-google-cloud]
blocked_by: []
contracts: [C5]
phase: 1
profile: proof of concept
estimate:
  hands_on: 2-3
  review_and_verify: 1
  total: 3-4
  calendar_waits: up to one week on the IT firm
owner: contractor, with the IT firm
status: ready
---

# G03 Access and evaluation samples

## Outcome
TMS API order creation confirmed with a credential in Secret Manager; Graph read-only permission on the pilot mailbox; gemini-3.8-flash on Vertex in australia-southeast1 verified; 50 past emails paired with TMS orders. Closes O1 to O3 (D4).

## Acceptance
- [ ] A1 readback shows model, region and credential names, no secret values (C5)
- [ ] A2 50 pairs stored outside logs
- [ ] A3 a written answer on O4, or an owner and a date

Verification: authorised live readback on the IT firm's project; no paid calls.

## Run this ticket
```text
/adk-engineer Carry out docs/tickets/order-intake/G03-access-and-samples.md. Read its design and plan, use its skills, run its verification, fill in Evidence and set status. Leave changes uncommitted.
```
