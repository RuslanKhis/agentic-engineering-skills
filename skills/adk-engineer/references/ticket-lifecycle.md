# The ticket lifecycle

Read before starting and again before finishing any ticket or plan goal, when
a ticket's Evidence starts with a `Progress:` block, or when the user runs
several tickets at once. A plan's tickets are worked on across many sessions; this keeps each
session small while the plan, not the session, holds the big picture.

## Start or resume

1. Read the ticket, its design and plan, as the main instructions say.
2. If Evidence starts with a `Progress:` block, this is a resume. Read the
   block, then `git status` and `git log` in the worktree it names, confirm
   the files it lists as uncommitted are present, and rerun its re-verify
   commands before writing anything new. Continue from its next step; do not
   redo finished acceptance items unless their checks now fail.
3. Confirm every goal in `blocked_by` is finished (`verified_local`,
   `verified_live` or `done`). If one is not, stop and say which, rather than
   building on unfinished work.
4. Run the `pass_to_pass` tests once before changing anything, so a later
   failure can be told apart from one that was already there.

## Check the estimate before editing

A ticket's estimate is human hours with a coding agent: hands-on plus review
and verify. Before editing, compare the work the acceptance cases need with
that estimate. If it is clearly larger (for example the high end would at least
double, or a calendar wait such as provider verification appears), say so
first. Build the largest useful slice that fits, and propose the remainder as
a new ticket with its own estimate instead of silently expanding the scope.
Write the human effort still owed for this change into the ticket's Evidence
and repeat it in the final message: hours to review and verify it, what to
check, and any step only a person can do (credentials, console setup,
approvals).

## Resources that charge

When a ticket creates a resource that charges while provisioned (a database
instance, a deployed vector index, a managed RAG database, minimum instances,
a reservation, a load balancer), write the deletion script beside the script
that creates it, in the same change: it deletes only what this ticket owns,
dependants before owners, refuses to run without the approved scope, and is
tested at least by a dry run. Record each such resource in the Evidence
section as one line, `<resource>: <absent | retained: reason | unknown>;
cleanup: <command>; verified: <how, when>`. When the ticket asks for a price
and the pricing page cannot be read in this session, leave the placeholder,
say so in Evidence and keep that acceptance item open; never fill it from
memory. A teardown goal or ticket completes only when the
resource list and, once it has caught up, the billing report show the
resources gone; a delete command returning successfully is where
verification starts.

## Stop before the acceptance cases pass

Context, time or a missing decision can end a session early. Before the last
reply, write at the head of the Evidence section:

```text
Progress:
  - done: A1 (local, python -m unittest tests.test_prefs), A2
  - in hand: A3, the forget route returns 204 but the cache keeps the value
  - next: clear the session-state copy in profile_loader.py, then rerun A3
  - uncommitted: app/profile.py, tests/test_prefs.py (worktree ../wt-G01)
  - re-verify: python -m unittest tests.test_prefs
```

Leave the status `in_progress`. End with the resume prompt:
`/adk-engineer Resume <ticket path> from its Progress block.` Remove the block
when the ticket completes.

## Finish

1. Write the Evidence and status as [Evidence and status](#evidence-and-status)
   says, including `actual:` with the human hours the person reports. Ask once if they have not said; write
   `not reported` rather than guessing. A manual verification item is
   recorded as `manual: <check> — confirmed by <person>, <date>` only when
   that person says they did it, otherwise `owed`; never tick it for them
   (humanlayer/humanlayer commit 77c7fe9, `.claude/commands/implement_plan.md`,
   Apache-2.0, read 2026-10-26).
2. For each contract this ticket evidenced, update its Evidence cell in the
   design's contracts table from `planned: …` to `evidenced: <tier>,
   <goal>/<acceptance>`. That cell is evidence, not a decision; change
   nothing else in the design.
3. Record a contract the work had to narrow or widen in the ticket's
   `contract_deltas`, and each ruling the design left open in `Rulings:`
   (what, why, cost if wrong). Do not edit the contract yourself; the designer
   takes it in at a checkpoint.
4. If the designer skill is installed, run its `scripts/plan_status.py` with
   the plan, ticket directory and design (resolve the script from the sibling
   `../adk-system-designer/` directory). Its last line is the next prompt.
   When it prints CHECKPOINT lines, end with that checkpoint prompt and the
   items it lists, not with the next ticket: the remaining tickets may rest on
   a contract that has just changed. Otherwise end with the next ready ticket,
   or the resume prompt for an interrupted one.

## Evidence and status

Write actual evidence and status into the ticket's Evidence section or the
plan's goal entry, using the tiers and outcomes of
[evidence labels](operating-rules.md#evidence-labels):

- one line for each design contract the goal cites: its ID, the tier reached
  (`offline`, `local`, `live` or `release`) and the acceptance cases that
  showed it;
- one line for each security rule it cites (ID, tier reached, acceptance
  cases);
- the companion skills loaded, with their pins;
- a numbered measurement record (`M<n>`: value, baseline, window, sample,
  method, owner, build) for every figure a pilot or production run produced,
  and an incident record (`I<n>`) for every incident, so that `adk-presenter`
  can cite them;
- an `actual:` line with the human hours the person reports (or
  `not reported`), and the human effort still owed (see the estimate section).

Set the ticket's status with the template's vocabulary (`verified_local` when
every acceptance case that can run offline has run here; `in_progress` with
the owed run named in Evidence when the SDK-tier cases are written but the SDK
is absent in this session; `verified_live` after the authorised run; `done`
when the owner accepts; `blocked` only for a decision or dependency outside
the ticket), and end with the run prompt for the next ready goal or ticket,
unless step 4 of Finish calls for the designer's checkpoint prompt: a contract
delta, an open ruling, an overrun, a blocked ticket or an orphaned contract
needs a decision.

## Run tickets in parallel

Only tickets that `plan_status.py` lists together under "Can run in parallel"
qualify: all their blockers are finished and their `touches` do not overlap.

1. Create one worktree per ticket from the same base commit, on a branch named
   after the goal: `git worktree add ../wt-G03 -b G03 <base>`.
2. Run each ticket in its own session in its own worktree. Each writes only
   its own ticket file and the paths in its `touches`; a session that finds it
   must write another ticket's path stops, sets `parallel_safe: no` in its
   ticket and says so.
3. Merge finished branches one at a time in dependency order, then by goal ID.
   After each merge, rerun every `pass_to_pass` test of the merged tickets
   before merging the next; a failure is fixed on that branch, not on the
   merged result.
4. Run `plan_status.py` after the last merge and follow its next prompt.

The person decides when to merge and commits; the sessions leave their changes
uncommitted unless asked otherwise.
