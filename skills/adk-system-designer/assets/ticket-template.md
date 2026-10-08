---
goal: <G01>
title: <first useful behavior, in the user's words>
design: <relative path to the architecture document>
plan: <relative path to the implementation plan>
primary_skill: <one specialist, e.g. adk-tool-interface-design>
supporting_skills: [<only those this goal's boundaries need>]
blocked_by: [<goal IDs or open decisions, empty when ready>]
status: ready
---

# <G01> <title>

## Outcome

<What changes for the user, in one or two sentences. Link the decisions it
implements, e.g. D1, D3.>

## Scope

- In: <modules, interfaces and behaviour this ticket changes>
- Out: <follow-up work that belongs to later tickets>

## Acceptance

- [ ] <happy path, observable>
- [ ] <important failure path>
- [ ] <forbidden effect that must not happen>

Verification: <runnable command or test boundary; say offline, local
integration or authorised live>.

## Evidence

<Filled in by the agent that carries the ticket out: files changed, commands
run with results, what remains unverified. Leave empty when writing the ticket.>

## Run this ticket

```text
/adk-engineer Carry out <path to this ticket>. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
