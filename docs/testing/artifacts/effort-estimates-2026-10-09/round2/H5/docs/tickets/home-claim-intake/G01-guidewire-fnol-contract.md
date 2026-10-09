---
goal: G01
title: Guidewire FNOL, document and policy-lookup contract is known and recorded as fakes
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 18–30
  review_and_verify: 6–10
  total: 24–40
  calendar_waits: Guidewire sandbox tenant + integration user with FNOL roles from the Guidewire admin team, 2–4 weeks (request in week 1; doc reading starts immediately)
owner: E1
status: ready
---

# G01 Guidewire FNOL, document and policy-lookup contract is known and recorded as fakes

## Outcome

The team knows, with sandbox evidence, how to create, submit and look up an FNOL claim, attach documents, search policies for a customer and prevent duplicates, so G08 is built against a verified contract. Decisions D3, D9.

## Scope

- In: Read the tenant's Cloud API release docs; on the sandbox: create draft claim, submit, add document, look up claim by external reference, policy search; repeat a create with the same duplicate-prevention key; record status codes and error bodies; write `docs/integration/guidewire-fnol-contract.md` and recorded fixtures for the fake adapter (`tests/fixtures/guidewire/`).
- Out: Adapter code (G08); production tenant access (G20).
- Depth: Production: replay and lookup semantics are verified, not assumed. Floor: sandbox only, no production tenant, secret in Secret Manager or local keychain, never in the repo.
- Route: Bounded investigation with stopping condition: stop when each of the six operations has a recorded request/response pair and the duplicate-key behaviour (same key, same payload; same key, changed payload; key after N hours) is observed, or after 40 h with the gaps written as decisions.
- Supporting skills: `adk-tool-auth-and-secrets` (integration-user OAuth2 client-credentials flow and secret placement)
- Execution scope: Sandbox calls are authorised once the Guidewire admin team issues the integration user; no production tenant.

## Acceptance

- [ ] Contract note lists endpoint, required fields, auth scope and error classes for: create draft, submit, add document, get by external reference, policy search, get claim
- [ ] Duplicate-prevention behaviour observed for same key/same payload and same key/changed payload, with retention window stated or marked unknown
- [ ] Recorded fixtures contain no real personal data and no credentials (grep check)

Verification: Authorised live calls against the Guidewire sandbox only; fixture scan `grep -rEi 'secret|token|bearer' tests/fixtures/guidewire` returns nothing.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
