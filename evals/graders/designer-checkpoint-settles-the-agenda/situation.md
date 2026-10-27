# designer-checkpoint-settles-the-agenda: what the fixture holds

Bases: support-assistant (app) and support-plan (design, plan, tickets G01-G05). Overlay:

- `docs/tickets/support/G01.md`: status verified_local, A1-A3 ticked, Evidence with C1, C2,
  SB01 lines, `actual: 6 h` (estimate total 2-3), `contract_deltas: [C2: forget also clears
  the cached copy of the language in session state (user:language), not only the stored row]`,
  and one unsettled ruling: forget is a soft delete kept 30 days (why, cost if wrong given).
- `docs/plans/support.md`: capacity cut to 10 h after reserve (change log 2026-10-16). With G01's
  6 h actual plus 6-11 h for G02-G05, phase 1 projects 12-17 h against 10 h: it no longer fits.
- `docs/architecture/support.md` is unchanged from the base: C2 still reads "after forget, the
  next session does not use the language" with Evidence `planned: forget test, local`.
- G01's code (app/preferences.py, app/server.py, app/store.py, app/prompts.py,
  tests/test_preferences.py) implements save, forget as a soft delete and the session-state clear.

What `plan_status.py --capacity 10` reports on the composed workspace (run by the fixture author):
CHECKPOINT lines for the C2 delta the design has not taken in, the unsettled ruling, G01's overrun
and the phase no longer fitting.

Assertion map:
- A1: the agent cannot run plan_status.py (no shell in the run); it passes A1 only if it names the
  command, says it could not run it, and builds the same agenda (delta, ruling, overrun, fit) from
  the records, settling each item with the user (or recording the question and assumption).
- A2: C2 revised in place in docs/architecture/support.md, keeping the ID, with a revised-by-G01
  note; tickets citing C2 (G04's contracts and pass_to_pass G01/A3) checked or updated.
- A3: the soft-delete ruling becomes a numbered decision (D4) or is rejected, and the ticket's
  ruling line is marked settled or rejected.
- A4: G02-G05 re-estimated, check_schedule.py rerun (or named as not runnable here), a cut-line
  proposal that keeps the floor, change-log and Resume-here updated, ending with the next prompt.

Original context: "Design, plan and tickets as in the plan-in-progress fixture: G01 verified_local
with a contract delta on C2, an open soft-delete ruling, actual 6 h against 2-3 h; phase
capacity 10 h."
