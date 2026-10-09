# Implementation plan: <application or change>

Status: draft / ready goals identified / in progress / complete with evidence
Architecture: <relative link to the canonical design>
Continuation source of truth: <this plan, existing spec or tracker>

## Destination and constraints

State the useful end result, non-goals, accepted stack and current authorization.
Link accepted decisions and unresolved assumptions. Record inspected repository
paths and versions separately from proposed modules or unverified interfaces.
Name the pinned model, judge and prompt versions the goals inherit from the
design; a goal that changes one of them is a release, not a side effect.
Keep credentials and private resource identifiers out of a shared artifact.

## Delivery profile and capacity

Profile: <proof of concept / assignment / internal tool / MVP or pilot /
production>, linked to the design's delivery constraints.

| Phase | Delivers | Goals | Estimate (focused hours) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | <the profile's "done"> | <G01 to G0n> | <range> | <people × hours × focus; reserve> |
| 2, harden or graduate | <graduation conditions for the next audience> | <IDs> | <range> | <when the team has time> |

Estimates are assumptions for the stated team; record actual effort in each
goal's evidence and move the cut line when phase 1 runs over. If time may run
out early, the goals are ordered so each completed one is still useful.

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |

Use actual inspected paths where available; label a greenfield layout as proposed.
Explain ordinary application enforcement alongside framework/service choices.

## Goals and dependencies

| ID and goal | Phase | Type: discovery / implementation | Estimate | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |

Use stable IDs and readable names. State may be proposed, ready, blocked,
in progress or complete. Ready describes resolved prerequisites, not new authority.
Each implementation goal is a useful end-to-end slice. Leave dependent future
goals coarse when an unresolved decision could change their scope.

### G01 — <first useful behavior or precise decision>

- **Phase and estimate:** <1, 2 or later; focused-hour range for the stated team>
- **Outcome and linked decisions:** <what changes for the user; design links>
- **Scope:** <included behavior and excluded follow-up work>
- **Depth:** <profile depth for the concerns this goal touches; the floor it
  keeps; specialist controls deliberately left for a later goal>
- **Implementation route:** <ADK/application components, interfaces and inspected
  or proposed modules; required infrastructure and compatibility checks>
- **Prerequisites:** <goal/decision IDs, dependencies, setup or external contract>
- **Primary skill:** <one specialist that leads this goal>
- **Supporting skills:** <only those this goal's boundaries need, each with its purpose>
- **Acceptance:** <observable success, important failure and forbidden-effect cases>
- **Verification:** <public test boundary, runnable command if known, required
  fixtures; distinguish offline, local integration and authorized live/hosted evidence>
- **Execution scope:** <what is already authorized; exact external prerequisites
  still needed for this goal>
- **Status and evidence:** <planned initially; later record files, actual commands,
  results and limitations>
- **Run this goal:** `/adk-engineer Carry out <goal ID> from <plan path>. Read <design
  path>, use the goal's primary and supporting skills, verify its acceptance cases
  locally and record evidence here.`

Repeat for currently actionable goals. Discovery goals state the question,
bounded investigation, expected decision/evidence and what it unblocks.
Fill every field with real values; the designer knows the goal ID, skills and
acceptance cases when it writes the plan. To hand goals to a tracker or to
another session, copy each into the [ticket template](ticket-template.md).

## Later

Deferred items not yet written as goals, one line each:

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |

## What the reviewer reads

At most three documents, named, that establish method, results and limits:

| Document | Establishes |
| --- | --- |
| <report or design> | Method and accepted decisions |
| <living evaluation summary> | Latest result per case, linked to raw run records |
| <this plan or the tracker> | Remaining limits and deferred controls |

Raw run records, ledgers and checkpoint logs are data under a data directory;
they are linked from the summary, never read as documents.

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |

For a chosen Wayfinder continuation, these questions seed decision planning.
Include destination, project conventions and applicable skills; link an existing
map if present. Preserve accepted decisions. This section does not create tickets.

## Resume here

- **Next goal:** <ID and readable name, and why it is ready>
- **Read first:** <canonical design, plan/spec, relevant project instructions>
- **Next action:** <first concrete inspection, decision or implementation step>
- **Continuation prompt:**

```text
/adk-engineer Carry out <goal ID and name> from <plan path>.
Read <design path> and preserve its accepted decisions.
Use <primary skill> with <supporting skills>.
Work within <authorized scope>, verify <acceptance cases>, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in <plan path>.`
Adapt the prompt for further planning when a decision blocks implementation.
After adopting a tracker/spec, point here to its canonical goals and statuses.
