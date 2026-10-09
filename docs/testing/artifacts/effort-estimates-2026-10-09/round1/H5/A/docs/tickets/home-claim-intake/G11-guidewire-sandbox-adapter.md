---
goal: G11
title: Claims and photos reach the Guidewire sandbox through the real adapter with the same exactly-once behaviour
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G02, G10]
phase: 1
profile: production
estimate: 64-100 h
status: blocked
---

# G11 Claims and photos reach the Guidewire sandbox through the real adapter with the same exactly-once behaviour

## Outcome

`CloudApiAdapter` implements `GuidewireClient` against the sandbox using the replay contract from G02, and the G10 contract tests pass against it. Implements D5, I3, I4 in the design.

## Scope

- In: Adapter, auth client with token caching, rate-limit handling, mapping of Guidewire errors to transient/permanent/uncertain, contract test suite runnable against fake and sandbox.
- Out: Production Guidewire credentials (G16 with the Guidewire team).
- Depth: Build; floor: credentials never in prompts, events or logs; sandbox only.
- Route: `app/guidewire/cloud_api.py`; secret name from config; VPC/private connectivity per G02.
- Prerequisites: G02, G10; sandbox credentials issued to the team; user authorisation for sandbox writes.
- Supporting skills:
  - `adk-tool-auth-and-secrets`: OAuth client credentials from Secret Manager, read vs write client separation, rotation
- Execution scope: Requires Guidewire sandbox credentials and explicit authorisation for sandbox claim creation.

## Acceptance

- [ ] The contract suite passes against the sandbox: create draft, attach documents, submit, read claim number.
- [ ] A forced client-side timeout after create is reconciled by the G02 mechanism without a second claim in the sandbox.
- [ ] Forbidden: the adapter cannot be configured with a production endpoint from a non-production environment.

Verification: Authorised live: contract suite against the sandbox with a bounded number of claims; offline: same suite against the fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-guidewire-sandbox-adapter.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
