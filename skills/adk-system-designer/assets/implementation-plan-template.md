# Implementation plan: <application or change>

Status: draft / ready goals identified / in progress / complete with evidence
Architecture: <relative link to the canonical design>
Continuation source of truth: <this plan, existing spec or tracker>

## Summary for the reader

At most one page, for the person who decides; figures come from the schedule
check, other facts are referred to by ID:

- **Profile and phase 1:** <profile; what phase 1 delivers and to whom>
- **Effort and finish:** <phase 1 human hours against capacity; finish range in
  working days against the date; fits / low end only / no>
- **Largest risks:** <three, each with its owner or mitigating goal>
- **Decisions needed from you:** <the open decisions that block or move dates>
- **Next prompt:** <the run prompt for the first ready goal>

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

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | <the profile's "done"> | <G01 to G0n> | <range> | <people × hours × focus; reserve> |
| 2, harden or graduate | <graduation conditions for the next audience> | <IDs> | <range> | <when the team has time> |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify), assumptions for the stated team. Calendar waits (reviews,
grants, provider verification) are listed on their goals, not added to hours.
With several people, add a load table:

| Person or role | Goals | Hours | Their capacity |
| --- | --- | --- | --- |

Schedule block, the single machine-readable source of each estimate (the
designer's `scripts/check_schedule.py` reads it; tickets copy it):

```yaml
- goal: G01
  phase: 1
  hands_on: 1-2          # human hours, agent-assisted
  review: 0.5-1
  total: 1.5-3
  owner: Dev A
  blocked_by: []
  calendar_waits: none   # or what, e.g. security review
  wait_days: 0           # working days the wait adds, as a range if unsure
  handoff: 0             # hours in total for picking up work from another person
  contracts: [C1, C3]    # design contracts this goal's acceptance proves
  security: [SB01, SB05] # web security rules this goal's acceptance proves, if any
  mentions_only: []      # IDs (or wait) the prose names without depending on them
  type: implementation   # implementation | journey | presentation | teardown | discovery
  status: planned        # when no ticket exists; a ticket's status replaces it
```

Longest dependent chain and finish range: <from the schedule check, with the
command and date it was run>. Record effort in each goal's
evidence (`actual:` hours) and move the cut line when phase 1 runs over; the
designer's `scripts/plan_status.py` adds the hours spent to the hours remaining
and says when the phase no longer fits. If time may run out
early, the goals are ordered so each completed one is still useful.

## Implementation map

| Contract / decision | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |

Use actual inspected paths where available; label a greenfield layout as proposed.
Explain ordinary application enforcement alongside framework/service choices.

## Web stack and companion skills

Only when the design has a web interface or HTTP API. Deviations from the
designer's web application defaults link their decision. The first goal writes
this table into the project's AGENTS.md; afterwards keep only the link.

| Companion | Source and install | Pin | Load when | Scope notes |
| --- | --- | --- | --- | --- |

## Goals and dependencies

| ID and goal | Phase | Type: discovery / implementation / presentation | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |

Use stable IDs and readable names. State may be proposed, ready, blocked,
in progress or complete. Ready describes resolved prerequisites, not new authority.
Each implementation goal is a useful end-to-end slice. Leave dependent future
goals coarse when an unresolved decision could change their scope. A
presentation goal sits at each phase boundary that needs someone's decision
(`Primary skill: adk-presenter`, one per audience); it depends on the goals
whose evidence it presents, and the decision date is a calendar wait that the
next phase's goals depend on. Before each presentation goal that presents
built work sits a journey goal (type journey, `Primary skill:
adk-agent-evaluation`, with Playwright as companion for a web interface) that
runs the design's journey end to end and every `pass_to_pass` test; passing
tickets one at a time does not show that the whole path works. A phase whose resources are not carried
forward ends with a teardown goal (`Primary skill:
deploy-adk-on-google-cloud`) that runs every cleanup command recorded under
**Resources created**, checks dependants and retention, and reads the billing
report; its acceptance lists each resource as absent, or retained with a
reason and an owner.

### G01 — <first useful behavior or precise decision>

- **Phase and estimate:** <1, 2 or later>; human hours, agent-assisted:
  hands-on <range>, review and verify <range>, total <range>; calendar
  waits <none, or what and how long>; owner <person or role>
- **Outcome, contracts and decisions:** <what changes for the user; the
  contracts it proves (C IDs) and decisions it implements (D IDs)>
- **Scope:** <included behavior and excluded follow-up work>
- **Depth:** <profile depth for the concerns this goal touches; the floor it
  keeps; specialist controls deliberately left for a later goal>
- **Implementation route:** <ADK/application components, interfaces and inspected
  or proposed modules; required infrastructure and compatibility checks>
- **Resources created:** <none, or one line per resource that charges while
  provisioned: resource and configuration; idle cost per day with pricing date
  and URL; cleanup command; how absence is verified; the teardown goal or cost
  contract that owns its lifetime>
- **Prerequisites:** <goal/decision IDs, dependencies, setup or provider guarantee>
- **Primary skill:** <one specialist that leads this goal>
- **Supporting skills:** <only those this goal's boundaries need, each with its
  purpose; a Google product to provision or operate as `google/skills:<name>
  (purpose)`>
- **Companion skills:** <names, or none>
- **Design system:** <path to DESIGN.md for UI goals, or none>
- **Security rules:** <SB IDs this goal proves, each cited by an acceptance
  item, or none>
- **Acceptance:** <numbered A1, A2 ...: observable success, important failure and
  forbidden-effect cases, each naming the contract and security rule it
  proves (A2 → C3, SB03); grid cells cite them as G01/A2>
- **Verification:** <public test boundary, runnable command if known, required
  fixtures; distinguish offline, local integration and authorized live/hosted evidence>
- **Execution scope:** <what is already authorized; exact external prerequisites
  still needed for this goal>
- **Status and evidence:** <planned, in_progress, blocked, verified_local,
  verified_live or done; then record files, actual commands,
  results and limitations, with one line per contract: C3 evidenced, local, A2.
  A pilot or production run adds numbered measurement records (M1: value,
  baseline, window, sample, method, owner, build) and incident records (I1:
  date, severity, effect, response, fix), which presentations cite by ID;
  one record per line, fields separated by semicolons, dates in ISO form
  (`M3: metric <name>; value <v>; baseline <b>; window 2026-09-01 to
  2026-09-30; ...`; an I record ends `status open` or `status closed
  <date>`), the shape the presenter's value-report check reads>
- **Run this goal:** `/adk-engineer Carry out <goal ID> from <plan path>. Read <design
  path>, use the goal's primary and supporting skills, verify its acceptance cases
  locally and record evidence here.`

Repeat for currently actionable goals. When tickets are written, the ticket is
the goal's home: keep only the goals table here, with a link to each ticket,
instead of these entries. Status and evidence are then written only in tickets
(parallel sessions would otherwise collide on this file); `plan_status.py`
reads them back for the current view. Discovery goals state the question,
bounded investigation, expected decision/evidence and what it unblocks.
Fill every field with real values; the designer knows the goal ID, skills and
acceptance cases when it writes the plan. To hand goals to a tracker or to
another session, copy each into the [ticket template](ticket-template.md).

## Later

Deferred items not yet written as goals, one line each:

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |

At MVP profile and above this table always holds the recurring cost review
(trigger: a date, the first bill, or a volume step) and the decommission item
(who deletes what, dependants and retention included, when the application
retires); the goal that reads the first live bill against the cost contract
is a phase goal, not a Later item.

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

Refreshed at each checkpoint; between checkpoints `scripts/plan_status.py`
prints the current next prompt from the tickets' actual statuses.

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
