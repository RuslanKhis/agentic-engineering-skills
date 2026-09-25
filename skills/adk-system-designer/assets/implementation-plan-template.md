# Implementation plan: <application or change>

Status: draft / ready goals identified / in progress / complete with evidence
Architecture: <relative link to the canonical design>
Continuation source of truth: <this plan, existing spec or tracker>

## Destination and constraints

State the useful end result, non-goals, accepted stack and current authorization.
Link accepted decisions and unresolved assumptions. Record inspected repository
paths and versions separately from proposed modules or unverified interfaces.
Keep credentials and private resource identifiers out of a shared artifact.

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |

Use actual inspected paths where available; label a greenfield layout as proposed.
Explain ordinary application enforcement alongside framework/service choices.

## Goals and dependencies

| ID and goal | Type: discovery / implementation | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |

Use stable IDs and readable names. State may be proposed, ready, blocked,
in progress or complete. Ready describes resolved prerequisites, not new authority.
Each implementation goal is a useful end-to-end slice. Leave dependent future
goals coarse when an unresolved decision could change their scope.

### G01 — <first useful behavior or precise decision>

- **Outcome and linked decisions:** <what changes for the user; design links>
- **Scope:** <included behavior and excluded follow-up work>
- **Implementation route:** <ADK/application components, interfaces and inspected
  or proposed modules; required infrastructure and compatibility checks>
- **Prerequisites:** <goal/decision IDs, dependencies, setup or external contract>
- **Skills:** <one primary; supporting skills and purpose; availability checked
  or still to check>
- **Acceptance:** <observable success, important failure and forbidden-effect cases>
- **Verification:** <public test boundary, runnable command if known, required
  fixtures; distinguish offline, local integration and authorized live/hosted evidence>
- **Execution scope:** <what is already authorized; exact external prerequisites
  still needed for this goal>
- **Status and evidence:** <planned initially; later record files, actual commands,
  results and limitations>

Repeat for currently actionable goals. Discovery goals state the question,
bounded investigation, expected decision/evidence and what it unblocks.

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
Use adk-engineer to continue <goal ID and name> from <plan path>.
Read <design path> and preserve its accepted decisions.
Use <primary skill> and <supporting skill, if relevant>.
Work within <authorized scope>, verify <acceptance cases>, and update
the plan with actual evidence and remaining blockers.
```

Adapt the prompt for further planning when a decision blocks implementation.
After adopting a tracker/spec, point here to its canonical goals and statuses.
