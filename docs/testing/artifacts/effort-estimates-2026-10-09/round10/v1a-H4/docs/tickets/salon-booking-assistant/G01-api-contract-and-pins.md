---
goal: G01
title: We know exactly what the booking API, the site login and the ADK pin give us
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 0.5-1
  total: 2.5-4
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 We know exactly what the booking API, the site login and the ADK pin give us

## Outcome

A short decision note, `docs/architecture/salon-booking-assistant-g01.md`,
settles open decisions O2 and O3 and picks the D3 confirmation mechanism. The
design is updated where an assumption (A5, A7, A8) proves wrong. Discovery
only. Stop after the note: no application code.

## Scope

- In: read the booking API spec and staging. Check idempotency-key support,
  whether reschedule is atomic, the error codes for a taken slot, a closed
  cancellation window and a foreign appointment, and whether the API enforces
  ownership with the customer token. Read how the site issues the customer
  JWT (issuer, JWKS URL, claims). Pick the google-adk pin (working assumption
  2.8.0) and confirm that tool confirmation works with `DatabaseSessionService`
  at that pin. If it does not, choose propose/commit. Re-read the Gemini model
  and deprecation pages for `gemini-3.8-flash` (D7) and record the date and
  the Vertex price per million tokens.
- Out: any implementation; G06 proceeds in parallel on the assumed pin and
  adopts this note's pin when it lands.
- Depth: a decision note with sources and dates. No staging writes beyond one
  booking, move and cancel on a test customer, done with the team's go-ahead.

## Acceptance

- [ ] The note answers O2 and O3 with evidence (spec section or staging response).
- [ ] The ADK pin, model ID, lifecycle date and price are recorded with their source and access date.
- [ ] D3 mechanism chosen (ADK confirmation or propose/commit) with the reason.
- [ ] No credentials or customer data appear in the note.

Verification: a reviewer reads the note against the API spec. Any staging calls
are listed with their effects (live, authorised test customer only).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-api-contract-and-pins.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
