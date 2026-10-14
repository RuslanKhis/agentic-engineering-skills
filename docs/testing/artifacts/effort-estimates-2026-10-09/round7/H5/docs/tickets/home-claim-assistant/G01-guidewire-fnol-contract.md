---
goal: G01
title: Record the Guidewire FNOL contract we will build against
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 10-16
  review_and_verify: 2-4
  total: 12-20
  calendar_waits: none
owner: Eng B
status: ready
---

# G01 Record the Guidewire FNOL contract we will build against

## Outcome

A written contract for creating a homeowners FNOL and attaching documents in ClaimCenter, plus recorded request/response fixtures, so G05 and G09 can start before the sandbox exists. Answers O2 as far as documentation and the integration team allow. Implements D5's prerequisites.

## Scope

- In: required and optional FNOL fields for homeowners, field mapping table from our draft, the external-reference field and whether it is searchable, idempotency support, document upload limits, rate limits, error codes and timeouts; fixtures under `tests/fixtures/guidewire/`.
- Out: any code calling Guidewire (G09), sandbox confirmation (G10).
- Depth: discovery; stop when each O2 item is answered or marked "needs sandbox" for G10.

## Acceptance

- [ ] `docs/integrations/guidewire-fnol.md` lists every field G05 needs with type, required flag and source
- [ ] Each O2 item is answered with a cited Guidewire document/version or marked for G10
- [ ] No credentials or tenant URLs appear in the document or fixtures

Verification: Offline: document review by Eng A and the Guidewire integration contact.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
