# Checkpoint a plan in progress

Read when the user asks for a checkpoint, when `adk-engineer` ends with the
checkpoint prompt, before a review goal, or for a stakeholder status update
between reviews.

Start with the skill's `scripts/plan_status.py --plan <plan> --tickets
<dir> --design <design> --capacity <phase hours>`; its CHECKPOINT lines are
the agenda, and each item is settled with the user:

- **Contract delta:** revise the contract's row in place, keep its ID, add
  `(revised <goal>, <date>): <change>`, and update the decisions, tickets,
  acceptance items and `pass_to_pass` lists that cite it.
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
`plan_status.py --phase <n> --gate` must pass: every phase goal finished,
every contract it cites evidenced or recorded as a gap or deferral, rulings
settled, deltas applied and every resource's state known. For a stakeholder
update between reviews, `--weekly --since <date>` drafts the status and RAID
log from the same records.
