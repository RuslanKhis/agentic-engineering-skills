# Independent plan review

Give this to a reviewer with a fresh context: a subagent where the host
supports one, otherwise a new session the user starts. The reviewer did not
write the plan. Replace the paths before sending.

```text
Review a delivery plan you did not write. Read, in full:
the design <design path>, the plan <plan path> and the tickets <tickets dir>.
Do not edit them. Report findings only.

The schedule block in the plan is the plan as it will run, and
<SKILL_DIR>/scripts/check_schedule.py computes its figures. Check:

1. Prerequisites. For every acceptance item (G04/A2) and every grid cell,
   ask what must exist before it can be checked: another goal's output, data,
   an environment, access, credentials, an outside approval or a booking.
   Compare each answer with the schedule (blocked_by, waits). List every
   prerequisite the schedule lacks, including ones the text describes without
   a goal ID ("once the widget works", "evidence for the DPIA pack").
2. Settled mentions. For each mentions_only entry, ask both directions: does
   the mentioning goal need the other, or does the other need it? List any
   that hide a real dependency or wait.
3. Claims. Rerun the helper with the plan's stated parameters, and run every
   remedy, fallback and negative or comparative claim ("only a later date
   works", "under half loaded") as a what-if on a copy. List each claim that
   the output does not support.
4. Coverage. List grid cells whose cited acceptance item does not test what
   the cell claims, and n/a reasons that are wrong.
5. Effect. For each finding, model it on a copy of the schedule and give the
   finish range with it, so the author can see which findings change "fits".

Return a table: finding, evidence (file and text), effect on finish, and
suggested fix. Keep it to the findings; do not restate the plan.
```

The author then settles every finding: fix the plan, or record why it does not
apply in the plan's change table. Rerun the helper after the fixes and quote
its figures in the summary.
