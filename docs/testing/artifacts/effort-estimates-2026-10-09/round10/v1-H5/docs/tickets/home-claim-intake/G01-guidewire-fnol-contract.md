---
goal: G01
title: Know exactly how a claim is created, completed and looked up in our Guidewire non-prod tenant
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-agent-interoperability]
blocked_by: [W1]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 16-24
  review_and_verify: 4-6
  total: 20-30
  calendar_waits: none on this goal; waits on W1 before it
owner: Eng B
status: blocked
---

# G01 Know exactly how a claim is created, completed and looked up in our Guidewire non-prod tenant

## Outcome

A written, sandbox-proven contract for the Guidewire ClaimCenter Cloud API
calls the executor and reconciler will make: create the FNOL claim, attach
documents, submit, and look a claim up by our `operation_id`. Settles open
decision O2 and the mechanism of D3; confirms A2, A16, A17 or records what
differs.

## Scope

- In: `docs/integrations/guidewire-fnol.md` with endpoints, required fields
  for a home FNOL, the field that carries `operation_id`, replay behaviour of
  a repeated create, error codes and their class (invalid, transient,
  uncertain), rate limits, token lifetime; recorded sample requests and
  responses with synthetic data under `tests/fixtures/guidewire/`; the
  policy-entitlement read the identity work needs. A one-page question list
  for the Guidewire team if the tenant lacks an external-reference field.
- Out: the adapter code (G10); load behaviour (G20).
- Depth: discovery with bounded live calls on the non-prod tenant only,
  synthetic data only. Stop when every row of the design's Guidewire grid
  row has evidence or a named gap.

## Acceptance

- [ ] Create, attach, submit and lookup each shown working on non-prod with a recorded request and response.
- [ ] Repeating a create with the same `operation_id` is observed and its outcome recorded (duplicate, rejection or second claim); D3 updated if a second claim is possible.
- [ ] A lookup by `operation_id` returns the claim created by a request whose response was discarded.
- [ ] No production endpoint or real customer data is touched; the client secret is never written to the repository.

Verification: authorised live calls against the Guidewire non-prod tenant
from a developer machine, with the request log attached; fixtures replayed
offline by a test that loads them.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
