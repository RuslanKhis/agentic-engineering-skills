# Checkpoint a plan in progress

Read when the user asks for a checkpoint, when `adk-engineer` ends with the
checkpoint prompt, before a review goal, or for a stakeholder status update
between reviews.

Start with the skill's `scripts/plan_status.py --plan <plan> --tickets
<dir> --design <design> --capacity <phase hours>`; its CHECKPOINT lines are
the agenda, and each item is settled with the user:

- **Contract delta:** revise the contract's row in place, keep its ID, add
  `(revised <goal>, <date>): <change>`, and update the decisions, tickets,
  acceptance items and `pass_to_pass` lists that cite it. A withdrawn
  contract is proved absent, not only recorded: the ticket that withdraws it
  carries a `SHALL NOT` acceptance item, tagged with the old contract ID,
  that tests the old behaviour is gone. In ADK a removed capability often
  survives as a tool still bound to an agent, a sub-agent still routable or a
  scope still granted (OpenSpec treats a removed requirement the code still
  implements as critical, `verify-change.ts`).
- **Ruling:** accept it as a numbered decision or reject it, and mark the
  ruling line in the ticket `settled: D<n>` or `rejected: <reason>`.
- **Overrun or a phase that no longer fits:** re-estimate the unfinished
  tickets from the evidence, rerun `check_schedule.py`, and move the cut line
  with the user rather than cutting the floor.
- **Blocked ticket or orphaned contract:** name what unblocks it, or give the
  contract a goal, or record `gap:` or `deferred:` with its trigger.

Update stale design Evidence cells to `evidenced: <tier>, <goal/acceptance>`,
add the changes to the plan's change table, refresh **Resume here**, rerun
`check_tickets.py`, and end with the next prompt `plan_status.py` prints.
Preserve accepted decisions the agenda does not touch. Before a review goal,
close the phase in four steps:

1. `plan_status.py --phase <n> --gate` passes: every phase goal finished
   (the presentation goal it precedes and a teardown after it excepted),
   every contract it cites evidenced or recorded as a gap or deferral,
   rulings settled, deltas applied, every withdrawn contract proved absent by
   a `SHALL NOT` acceptance item tagged with its ID, every manual check
   confirmed by a named person and date, and every resource's state known.
2. The same gate with `--base <commit>`, the commit the phase started from
   (record it in **Resume here** when the phase opens): every file changed
   since then sits inside some ticket's `touches`. Implementers add the files
   they create, empty package files included. A diff that cannot be read
   fails the gate as not verified, never as passed.
3. A read-only review in a fresh context with
   [the plan-versus-code prompt](../assets/code-review-prompt.md): ticked
   boxes are not evidence that the code still does what the contracts say,
   so the reviewer reads the code and tests behind each evidenced or
   withdrawn contract and grades each gap (missing, partial, contradicting,
   unrequested) CRITICAL, WARNING or SUGGESTION. It fixes nothing (github/spec-kit
   commit 67e0f72, `templates/commands/converge.md`, and Fission-AI/OpenSpec
   commit 6d04a1b, `src/core/templates/workflows/verify-change.ts`, both
   MIT, read 2026-10-26; the phase base commit after
   gemini-cli-extensions/conductor commit 6e8f9a8, Apache-2.0, `workflow.md`).
4. Its findings join the agenda; a CRITICAL finding keeps the phase open.

A withdrawn contract's design Evidence cell reads `evidenced: <tier>,
<goal>/<SHALL NOT item>`, because the item proves the behaviour is gone.

For a stakeholder update between reviews, `--weekly --since <date>` drafts the status and RAID
log from the same records.
