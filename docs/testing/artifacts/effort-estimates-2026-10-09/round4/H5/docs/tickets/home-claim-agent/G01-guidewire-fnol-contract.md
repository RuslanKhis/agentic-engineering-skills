---
goal: G01
title: Settle the Guidewire FNOL contract we file claims against
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 14-24
  review_and_verify: 4-6
  total: 18-30
  calendar_waits: Guidewire sandbox credentials and API docs from the Guidewire platform team
  wait_days: 5-10
owner: Eng B
status: ready
---

# G01 Settle the Guidewire FNOL contract we file claims against

## Outcome

The team knows exactly how to create, attach to, submit and look up a Homeowners claim in ClaimCenter, and how Guidewire treats a repeated request, so G10 can guarantee one claim per confirmed draft. Implements D3 and the provider side of I2.

## Scope

- In: Sandbox HTTP experiments in a throwaway script outside `app/`; `docs/integration/guidewire-fnol-contract.md`; recorded responses as fixtures; a fake Guidewire spec for G10.
- Out: The worker (G10), production access (G22, G23).
- Depth: Production depth for evidence. Floor: no credentials or tokens in the note or fixtures; sandbox only.

## Acceptance

- [ ] The note records version, endpoints, required Homeowners fields, document limits, rate limits, error codes and the OAuth flow, each with a sandbox request/response as evidence or a named gap
- [ ] A duplicate-create experiment (same payload, same key or reference, twice) records whether Guidewire replays, rejects or duplicates
- [ ] The decision 'key replay' versus 'lookup by external reference' is written down for G10, with its evidence
- [ ] No secret, token or customer data appears in the repository

Verification: Bounded live on the Guidewire sandbox, ≤ 50 requests; nothing in production.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
