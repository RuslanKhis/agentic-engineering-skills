---
goal: G01
title: Find out exactly how to create a home FNOL claim with photos in our ClaimCenter, safely and only once
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 12-18
  review_and_verify: 2-3
  total: 14-21
  calendar_waits: Guidewire claims-IT workshop and sandbox client
owner: Eng A
status: ready
---

# G01 Find out exactly how to create a home FNOL claim with photos in our ClaimCenter, safely and only once

## Outcome

Settles open decision O1, on which D5 (durable submission ledger) and invariant I2 (at most one claim per confirmed submission) rest. Discovery goal: the output is a decision document, not code.

## Scope

- In:
  - ClaimCenter Cloud API endpoints for draft claim, document upload and submit; required home-FNOL fields (loss cause codes, policy reference, loss address, reporter); replay or idempotency mechanism (header or searchable external reference); document size and type limits; rate limits; error shapes; maintenance windows
  - Workshop with claims IT; request a sandbox OAuth client scoped to FNOL creation and document upload (request on day 1)
  - Output: `docs/integration/guidewire-fnol-contract.md` and a secret-free recorded request/response set for the G06 fake
- Out: Writing the adapter (G06); production client (G14)
- Depth: Discovery only; sandbox credentials only, stored per `adk-tool-auth-and-secrets`; no production access. Stopping condition: two weeks, then unresolved items go back to O1 with an owner.

## Acceptance

- [ ] Contract document answers every scope question with a cited source
- [ ] Replay behaviour verified by one duplicate sandbox call, or recorded as "unsupported, reconcile by external reference"
- [ ] No credential, token or customer data appears in the document or recordings

Verification: Reviewed document; bounded sandbox calls (authorised live, sandbox only).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
