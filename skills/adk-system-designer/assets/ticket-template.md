---
goal: <G01>
title: <first useful behavior, in the user's words>
design: <path from the repository root to the architecture document>
plan: <path from the repository root to the implementation plan>
primary_skill: <one specialist, e.g. adk-tool-interface-design>
supporting_skills: [<only those this goal's boundaries need, each with its purpose in parentheses; a Google product to provision or operate as google/skills:<name> (purpose)>]
docs: [<reference pages the implementer reads first, as skill/references/file.md>]
blocked_by: [<goal IDs this ticket waits for and open decisions; status is ready when nothing outside this phase blocks it>]
touches: [<paths this ticket expects to change; the implementer adds any it creates>]
parallel_safe: <yes when no other ticket of this phase writes a path in touches and every goal in blocked_by is finished, else no>
contracts: [<design contract IDs this ticket proves, e.g. C1, C3>]
companion_skills: [<names, or empty>]
security: [<SB IDs this ticket proves, or empty>]
design_system: <path to DESIGN.md for UI tickets, or none>
contract_deltas: [<none, or a contract ID and its one-line revision when this ticket narrows, widens or withdraws one; a withdrawal needs a SHALL NOT acceptance item tagged with that ID>]
pass_to_pass: [<earlier tickets' acceptance items, as G01/A2, whose tests this ticket must keep passing: those whose touches or contracts overlap this ticket's, or empty; with no earlier tickets, the existing test ids instead; these are the evaluation skill's pass_to_pass tests>]
phase: <1, 2 or later>
type: <implementation | journey | presentation | teardown | discovery>
profile: <proof of concept / assignment / internal tool / MVP or pilot / production>
estimate:                # human hours, agent-assisted
  hands_on: <range, e.g. 1-2>
  review_and_verify: <range>
  total: <range>
  handoff: <none, or hours received from another owner's goal>
  calendar_waits: <the plan's value exactly: a wait ID or none>
owner: <person or role, when several people share the work>
status: ready            # ready | in_progress | blocked | verified_local | verified_live | done
---

# <G01> <title>

## Outcome

<What changes for the user, in one or two sentences. Link the decisions it
implements, e.g. D1, D3. Rulings the design left open and this ticket takes,
one line each.>

## Scope

- In: <modules, interfaces and behaviour this ticket changes>
- Out: <follow-up work that belongs to later tickets>
- Depth: <build at this profile's depth; the floor kept; controls left for
  later goals, by ID>

## Constraints

<One line: the decisions this ticket must not change (identity source,
transport, stack), by reference to AGENTS.md and the design. Omit when none.>

## Reference patterns

<Optional; omit when none. One entry per design studied elsewhere and
implemented ADK-natively: source and pin; the pattern; the ADK-native
mechanism used instead; the acceptance item it drives; the licence (study
only, or copied with attribution).>

## Resources created

<none, or one line per resource that charges while provisioned: resource and
configuration; idle cost per day with pricing date and URL; cleanup command;
how absence is verified; the teardown ticket or cost contract that owns its
lifetime. The deletion script is written and tested in this ticket, beside the
script that creates the resource. Usage spend this ticket causes without
provisioning (a judge run, a paid evaluation) is one more line with its cap.>

## Acceptance

- [ ] A1 WHEN <trigger> THE <app> SHALL <observable result> (C1)
- [ ] A2 IF <failure> THEN THE <app> SHALL <recovery> (C3)
- [ ] A3 <under condition> THE <app> SHALL NOT <forbidden effect> (C3, SB03)

<An item that proves a floor or a version pin rather than a contract is
tagged (floor). A security rule ID sits beside the contract it helps
prove. A box is ticked when the item's verification ran at the stated
tier.>

Verification, automated: <runnable command with the expected exit code, on
the project's pinned interpreter; offline, local or authorised live>.
Verification, manual: <none, or the person and what they check>. The agent never ticks a manual item; its Evidence line reads `manual: <check> — confirmed by <person>, <date>` in that person's words, or `owed`.
<When the SDK is absent in the session, the SDK-tier cases are written and
reported as not run; the status is then in_progress with the owed run named.>

## Evidence

<Filled in by the agent that carries the ticket out: files changed; for each
acceptance item the command, its exit code on the base commit (the commit
before the change, or for an incident the commit that had the defect; it must
fail there, since an item whose test already passes proves nothing) and after the change,
each `pass_to_pass` item's command and exit code after the change, and the commit SHA (or
"uncommitted") with the worktree path; one line per contract (C3: evidenced,
local, A2 and A3; a partial tier says which items ran where); one line per
security rule (SB03: evidenced, tier 1, A3); the companion skills loaded and
their pins, or each missing one as setup owed; a `Rulings:`
list of decisions the ticket did not settle (what, why, cost if wrong);
controls deliberately deferred; the state of each resource created (absent,
retained with reason, or unknown) with its cleanup command; measurement and
incident records as the plan template defines them (M1, I1); what remains
unverified; the human review and verification still owed (hours, and what to
check); steps only a person can do; and whether the work proved larger than
its estimate, with `actual: <human hours spent, as the person reports them, or
not reported>` on its own line. While the ticket is unfinished at the end of a
session, a `Progress:` block heads this section: acceptance items done, the item
in hand, the next step, uncommitted files and the worktree, and the commands
that re-verify what is done; it is removed when the ticket completes. Leave
empty when writing the ticket.>

## Run this ticket

```text
/adk-engineer Carry out <path to this ticket>. Read its design and plan,
use its primary and supporting skills and its companion skills at the pins
in AGENTS.md, keep its constraints and security rules, run its
verification locally, fill in the Evidence section and set status
(verified_local when every
acceptance case that can run offline has run here, in_progress with the owed
run named when the SDK is absent, verified_live after the authorised run,
done only when every acceptance item has fresh evidence and the owner
accepts). If Evidence starts with a Progress block, resume from it. Leave
changes uncommitted.
```
