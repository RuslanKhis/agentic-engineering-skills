---
goal: G34
title: One Guidewire client files, submits, looks up and attaches with a single retry owner
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01]
phase: 1
profile: production
estimate:
  hands_on: 12-17
  review_and_verify: 4-6
  total: 16-23
  calendar_waits: none
owner: Eng D
status: proposed
---

# G34 One Guidewire client files, submits, looks up and attaches with a single retry owner

## Outcome

The shared HTTP client and the claims and documents adapter that G04, G08
and G09 call, built against the G01 fake while live access is pending.
Implements the adapter part of D6 and D7. Handoff: 2 h from Eng B on the
contract note.

## Scope

- In: `app/guidewire/client.py` (OAuth client credentials from Secret
  Manager, token cache, 10 s timeout, Retry-After parsing, error mapping to
  `retryable`, `correctable`, `unknown`, `auth`), `app/guidewire/claims.py`
  (create draft claim with dedup key and our reference, submit, lookup by
  reference), `app/guidewire/documents.py` (upload with our document
  reference, list a claim's documents), a contract test suite runnable
  against the fake and, later, non-prod.
- Out: retry scheduling and deadlines (the operation in G08 owns them);
  policy search mapping (G04).
- Depth: production; the client never retries by itself, so retries are
  counted once.

## Acceptance

- [ ] A1 Create sends the dedup key and our reference on every attempt of the same step; submit and lookup by reference return typed results; tests pass against the fake.
- [ ] A2 Every fault of the fake maps to one documented class (`retryable`, `correctable`, `unknown`, `auth`); a timeout after sending a create maps to `unknown`, never `retryable`.
- [ ] A3 The token is cached until shortly before expiry; a 401 triggers one refresh; credentials are read from Secret Manager and never logged.
- [ ] A4 A 429 result carries the parsed Retry-After to the caller; the client itself makes exactly one HTTP attempt per call.

Verification: offline — `pytest tests/guidewire` against the G01 fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G34-guidewire-adapter.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
