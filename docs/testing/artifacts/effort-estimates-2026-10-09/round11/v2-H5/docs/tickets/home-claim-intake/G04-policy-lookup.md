---
goal: G04
title: The customer picks one of their own home policies for the claim
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [safe-api-tool-calls]
blocked_by: [G01, G03, G34]
phase: 1
profile: production
estimate:
  hands_on: 8-12
  review_and_verify: 4-6
  total: 12-18
  calendar_waits: none
owner: Eng B
status: proposed
---

# G04 The customer picks one of their own home policies for the claim

## Outcome

Code (not the model) lists the customer's home policies in force at the loss
date; the customer picks one; the agent sees only a summary. Implements D6.
Handoff: 1 h from Eng E on the identity middleware and 1 h from Eng D on
the shared Guidewire client (G34).

## Scope

- In: `app/policies/` lookup service using the shared Guidewire client from
  G34, `GET /v1/drafts/{id}/policies`, `PUT /v1/drafts/{id}/policy`,
  policy summary (product, insured address, in-force dates) in session state.
- Route: mapping customer → Guidewire contact uses the identifier agreed in
  G01; tested against the G01 fake.
- Out: the re-check just before filing (G08/A7).
- Depth: production.

## Acceptance

- [ ] A1 A customer with two in-force home policies at the loss date sees both and selects one; the model request contains only that policy's summary.
- [ ] A2 A customer with no in-force home policy at the loss date gets the designed message with the phone route; confirm stays disabled.
- [ ] A3 Policy search slow, unavailable or rate limited (fake) → at most 2 attempts within 5 s honouring Retry-After, then "we cannot check your policy right now; your draft is saved"; conversation continues, confirm disabled.
- [ ] A4 A request selecting a policy number not returned for this customer is refused and logged as a security event without the policy number in the log.
- [ ] A5 A 401 from Guidewire refreshes the client token once; a second 401 raises an alert and stops retrying.
- [ ] A6 An unexpected payload (missing in-force dates, unknown product) is treated as unavailable, never as "no policy".
- [ ] A7 A 400 or 403 from policy search is reported as "we cannot check your policy right now", alerts on 403, and is never shown as "no policy".

Verification: offline — `pytest tests/policies` against the G01 fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-policy-lookup.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
