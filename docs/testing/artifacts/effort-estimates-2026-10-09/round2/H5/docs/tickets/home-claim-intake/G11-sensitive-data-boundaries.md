---
goal: G11
title: Customer text is screened before storage and nothing personal reaches logs
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G03, G07, G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 32–54
  review_and_verify: 16–26
  total: 48–80
  calendar_waits: none
owner: E2
status: blocked
---

# G11 Customer text is screened before storage and nothing personal reaches logs

## Outcome

SDP masks payment and national-ID data before persistence, Model Armor screens input and output, the response-release check enforces I4, telemetry carries no content, and retention/erasure jobs run. D10, I4, I6, I10.

## Scope

- In: Ingress screening in the `/turns` handler before `Runner`; release check after the final event; fail-closed behaviour; log allowlist; retention job (Cloud Scheduler → Cloud Run job) for sessions, drafts, photos; erasure endpoint for the DPO process.
- Out: Threat model and pentest (G15).
- Depth: Production. Floor: no content in logs.
- Route: SDP `deidentify` with an inspect template in the EU region; Model Armor template; ADK telemetry gates off.
- Supporting skills: `adk-agent-observability` (content-free spans and log allowlist verification)
- Execution scope: Dev project.

## Acceptance

- [ ] An IBAN typed by the customer is masked in stored events and the customer is told
- [ ] SDP unavailable: message rejected with retry text, nothing persisted
- [ ] Canary PII string in a turn appears in no log entry or span attribute (scan)
- [ ] Retention job deletes a 31-day-old abandoned draft, its session and photos; a 29-day-old one survives

Verification: Offline with fakes for SDP/Model Armor; authorised dev check against the real services.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-sensitive-data-boundaries.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
