---
goal: G04
title: The Friday demo cannot overspend, runs the same versions as rehearsal, and has a fallback
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G03]
phase: 1
profile: proof of concept
estimate: 0.25 h
status: blocked (by predecessor goals; ready in design)
---

# G04 The Friday demo cannot overspend, runs the same versions as rehearsal, and has a fallback

## Outcome

Before Friday there is a spend stop on the key used by `adk web`, a one-line record of the versions you rehearsed with, and a short demo script with a fallback. Implements D5 and the floor items for spend and pinning.

## Scope

- In: set a request or token quota on the API key's project and a budget alert at the assumed US$25 (you set both in the console; the agent does not run cloud commands). Write `docs/demo.md` with the model ID, the `google-adk` version, the index build date and the G03 results file name. Add 5 demo questions taken from G03 passes, plus 1 not-covered question, and the fallback: open the G03 results table if the API fails. Also list the excluded scanned pages from G01's report, if any.
- Out: per-user allowances, an operator stop and release manifests (phase 2).
- Depth: minimal. A budget alert alone only notifies; the quota is the stop.

## Acceptance

- [ ] `docs/demo.md` records the model ID, the ADK version and the G03 results file, and the running code uses the same model ID (grep `agent.py`).
- [ ] The key's project shows a quota and a budget alert. A screenshot or setting value is noted in Evidence, with no key value.
- [ ] One full rehearsal of the 6 demo questions in `adk web` matches the G03 outcomes.
- [ ] Forbidden: the API key appears in no tracked file (`git grep` for its prefix returns nothing).

Verification: local, manual. The rehearsal is about 18 model calls on the paid key.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G04-demo-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
