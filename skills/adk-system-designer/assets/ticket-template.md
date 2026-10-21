---
goal: <G01>
title: <first useful behavior, in the user's words>
design: <relative path to the architecture document>
plan: <relative path to the implementation plan>
primary_skill: <one specialist, e.g. adk-tool-interface-design>
supporting_skills: [<only those this goal's boundaries need; a Google product to provision or operate as google/skills:<name>>]
blocked_by: [<goal IDs or open decisions, empty when ready>]
contracts: [<design contract IDs this ticket proves, e.g. C1, C3>]
phase: <1, 2 or later>
profile: <proof of concept / assignment / internal tool / MVP or pilot / production>
estimate:                # human hours, agent-assisted
  hands_on: <range, e.g. 1-2>
  review_and_verify: <range>
  total: <range>
  calendar_waits: <none, or what and how long>
owner: <person or role, when several people share the work>
status: ready
---

# <G01> <title>

## Outcome

<What changes for the user, in one or two sentences. Link the decisions it
implements, e.g. D1, D3.>

## Scope

- In: <modules, interfaces and behaviour this ticket changes>
- Out: <follow-up work that belongs to later tickets>
- Depth: <build at this profile's depth; the floor kept; controls left for
  later goals, by ID>

## Acceptance

- [ ] A1 <happy path, observable> (C1)
- [ ] A2 <important failure path> (C3)
- [ ] A3 <forbidden effect that must not happen> (C3)

Verification: <runnable command or test boundary; say offline, local
integration or authorised live>.

## Evidence

<Filled in by the agent that carries the ticket out: files changed, commands
run with results, one line per contract (C3: evidenced, local, A2 and A3),
controls deliberately deferred, what remains unverified, the human review and
verification still owed (hours, and what to check), steps only a person can do, and whether the work proved larger than its estimate. Leave
empty when writing the ticket.>

## Run this ticket

```text
/adk-engineer Carry out <path to this ticket>. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
