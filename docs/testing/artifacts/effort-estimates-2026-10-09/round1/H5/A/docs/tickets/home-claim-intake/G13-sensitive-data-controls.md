---
goal: G13
title: Personal data stays minimal, in the EU, out of telemetry, and is deleted on schedule
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G03, G05]
phase: 1
profile: production
estimate: 80-120 h
status: blocked
---

# G13 Personal data stays minimal, in the EU, out of telemetry, and is deleted on schedule

## Outcome

A data map and controls: output release check (coverage/payout promises, card numbers, other customers' identifiers), input screening decision, telemetry content off, retention and erasure jobs, and DPIA inputs for the DPO. Implements D2, D6, D8, I6, I7, I8 in the design.

## Scope

- In: `docs/integration/data-map.md`; `app/guardrails/release.py`; optional Model Armor integration if G03 confirms an EU endpoint; scheduled deletion of sessions (90 d) and photos (30 d); erasure procedure; fail-closed behaviour when screening is unavailable.
- Out: Face redaction (P2-04).
- Depth: Build; floor: fail closed on release check failure.
- Route: Release check wraps the API's message emission after the Runner finishes the turn; deletion job as a Cloud Run job configured in G16.
- Prerequisites: G03 (residency of screening services), G05.
- Supporting skills:
  - `adk-agent-observability`: content-capture gates and log allow-list
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] A scripted reply promising payment is replaced with the fixed text and the metric increments.
- [ ] Retention job deletes sessions older than 90 days and photos 30 days after attach, verified on local data; erasure removes a customer's sessions, drafts and staged photos and leaves terminal operation audit rows per policy.
- [ ] Forbidden: an in-memory exporter and log capture show no message content, photo bytes or policy numbers during a full scripted filing.

Verification: Offline tests; DPO review of the data map.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-sensitive-data-controls.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
