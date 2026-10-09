---
goal: G08
title: We can measure whether the agent files complete, correct claims without saying what it must not
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-release-engineering, protect-adk-sensitive-data]
blocked_by: [G01]
phase: 1
profile: production
estimate: 120-180 h
status: blocked
---

# G08 We can measure whether the agent files complete, correct claims without saying what it must not

## Outcome

A labelled dev set (≈ 150 simulated conversations across loss types and both languages, ≈ 300 labelled photos, ≥ 40 adversarial cases) with a harness reporting field accuracy, completeness, photo enum accuracy and policy-violation count, plus a pinned judge prompt. Implements D1, D2, D10, I6 in the design.

## Scope

- In: `evals/` cases and labels; user simulator personas; metrics; `evals/SUMMARY.md`; thresholds proposed for G18; data-sourcing note approved by the DPO.
- Out: CI wiring (G18), instruction iteration (G09).
- Depth: Build with gated evaluation; floor: no real customer data without DPO approval; synthetic first.
- Route: ADK evaluation with scripted and simulated users; judge `gemini-3.8-flash` with `evals/judge/v1.md`.
- Prerequisites: G01; DPO decision on historical data use.
- Supporting skills:
  - `adk-release-engineering`: eval-set hashing and a gate that fails by exit code
  - `protect-adk-sensitive-data`: sourcing and anonymising historical FNOL narratives and photos
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls. Live judged runs need an authorised Vertex project and the eval budget.

## Acceptance

- [ ] The harness runs the full set and writes per-metric results and per-case records; a missing case is reported as missing, not passed.
- [ ] The adversarial slice includes coverage-promise, injury-detail, cross-customer and injected-photo cases with deterministic assertions where possible.
- [ ] Forbidden: no unapproved real personal data in the repository; judge model ID is pinned, not an alias.

Verification: Offline harness test with a scripted model; bounded live run within the eval budget when authorised.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G08-evaluation-dev-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
