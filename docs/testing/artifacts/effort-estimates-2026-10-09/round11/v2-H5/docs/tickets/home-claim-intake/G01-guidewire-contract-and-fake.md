---
goal: G01
title: We know exactly how to file a home claim in ClaimCenter, and can test against a faithful fake
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-agent-interoperability]
blocked_by: []
phase: 1
profile: production
estimate:
  hands_on: 10-14
  review_and_verify: 2-4
  total: 12-18
  calendar_waits: none
owner: Eng B
status: ready
---

# G01 We know exactly how to file a home claim in ClaimCenter, and can test against a faithful fake

## Outcome

Discovery with a stopping condition: a written Guidewire contract taken from
the ClaimCenter Cloud API documentation and the insurer's integration team,
plus a local fake server that the build goals test against while live access
is pending. Implements the contract side of D6, D7 and D10.

## Scope

- In: `docs/integrations/guidewire-claimcenter.md` (contract note);
  `app/guidewire/fake/` (proposed) — an HTTP fake for policy search, draft
  claim create, submit, document upload, claim lookup by our reference, with
  switchable faults (slow, 4xx, 5xx, 401, 429, response dropped after commit,
  malformed body).
- Route: read the Cloud API reference for the tenant's ClaimCenter release;
  ask the integration team for the home line-of-business FNOL mapping,
  loss-cause codes and the field available for our external reference.
- Out: live calls (G25); the production adapter's retry policy (G08).
- Depth: production; the fake must model a committed write whose response
  is lost, because I3 depends on it.
- Stopping condition: ten working days, or earlier when A1–A4 are met. Any
  item the documentation does not settle is listed as a G25 question.

## Acceptance

- [ ] A1 The contract note records the ClaimCenter release and Cloud API version, each endpoint used (policy search, draft claim create, submit, documents, lookup by reference) with request and response shapes, and its documentation source and date.
- [ ] A2 The fake implements those endpoints and every fault above, including the documented request-deduplication header (expected `GW-DBTransaction-ID`; record what the documentation actually says) and lookup by our reference; its own tests pass.
- [ ] A3 Required FNOL fields for home claims and the loss-cause and room code lists are recorded as the source for the `ClaimDraft` schema (D10).
- [ ] A4 A recorded decision on the step order create draft → submit → attach documents (D7), or the alternative the documentation forces, with its consequence for G08 and G09.

Verification: offline — `pytest tests/guidewire_fake/`; the contract note is
reviewed by Eng A and the integration team.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-guidewire-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
