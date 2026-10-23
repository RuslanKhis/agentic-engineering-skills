# Phase D designer and engineer trials — 23 October 2026

*Four fresh-agent trials that decided the memo's designer proposals.*

## Setup

One synthetic design (a support triage assistant: four contracts, four
decisions, one open decision, internal-tool profile) in two identical
project copies. Designer trial A wrote the plan and tickets with the current
ticket template; designer trial B with a prototype carrying every proposal
(`touches`, `parallel_safe`, `constraints`, `docs`, `reference_patterns`,
`contract_deltas`, EARS acceptance wording, a split verification line,
per-item evidence with a `Rulings:` list and a `done` rule, lead-method and
companion lines in the run prompt). Engineer trials A and B then carried out
each set's first ticket (route a ticket to a queue, C1) with the skills, no
SDK installed. All four ran in subagents with fresh context, no network and
no credentials; the designer trials were interrupted once by a usage limit
and resumed. The hypothesis table and rulings are in the
[research note](../research/phase-d-designer-proposals-2026-10-23.md).

## Results

| Trial | Output | Ease |
| --- | --- | --- |
| Designer A (current) | Plan, four tickets, schedule helper exit 0 after fixes; C4 ticketed as a floor | 3 of 5 |
| Designer B (prototype) | Plan, four tickets (C4 deferred to phase 2 behind an open decision), schedule helper exit 0 after four corrective runs; every proposed field filled | 3 of 5 |
| Engineer A (ticket from A) | Tool, SDK-free routing policy, agent, app, strict scripted double, 21 tests (16 run, 5 SDK-tier not run), helpers run, evidence filled, status set | 3 of 5 |
| Engineer B (ticket from B) | Tool, SDK-free policy, agent, strict scripted double, 20 tests (15 run, 5 SDK-tier not run), three linters run, evidence filled with twelve rulings, status set | 4 of 5 |

What the engineers said helped in B and lacked in A: supporting skills with
their purpose, the `docs` list, EARS items mapping one-to-one onto tests,
the designer's rulings written in Outcome, and the evidence checklist with
`Rulings:`. What both engineers lacked: a status for "implemented, offline
green, SDK tier owed", a rule for ticking boxes, the interpreter the
verification command assumes, and the pin's home. What B found redundant:
the lead-method and companion lines repeated in every ticket, and the
`constraints` pointer. What both designers lacked: a definition of
`blocked_by` that lets a dependency-ordered phase be ticketed in full, a path
base for `design:` and `plan:`, an exact-copy rule for `calendar_waits`, a
`handoff` field, a non-contract acceptance tag, and a home for usage spend.

## Changes made

- The ticket template rewritten with the adopted proposals and the shared
  repairs (717 words, from 432).
- The handoff reference: one ticket per goal of the phase; one lead method
  per ticket with companions for human-only steps; where a project's standing
  agent instructions live.
- The designer skill's ticket sentence aligned.
- The engineer skill: the status rule for the SDK-absent case.
- The tool-interface skill: the scripted double's shape named and the
  greenfield baseline rule; a pointer to the 2.12.0 Runner shapes.
- The schedule helper: trailing comments on list values parsed, with a test.

## What this does not establish

No ticket was carried out with the SDK present, so the Runner-tier wording
of the acceptance items was never executed; the rewritten template was not
itself re-trialled after adoption, so its word count and field definitions
rest on the prototype trial plus the two engineer readings.
