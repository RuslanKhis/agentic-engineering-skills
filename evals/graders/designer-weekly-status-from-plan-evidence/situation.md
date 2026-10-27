# designer-weekly-status-from-plan-evidence: what the fixture holds

Bases: support-assistant and support-plan. Overlay: G01 verified_local (Evidence with C1, C2,
SB01, `actual: 6 h` against 2-3 h, an unsettled contract delta on C2 and an open soft-delete
ruling, committed 2026-10-20), G02 in_progress with a Progress block (A1 done, A2 in hand,
`actual so far: 2.5 h`, which plan_status does not count as `actual:`), G01's code and tests, and
the previous status update `docs/status/2026-10-18.md`. No git history (the original context
assumed one; the helper uses git only for the "finished since" line).

`plan_status.py --plan docs/plans/support.md --tickets docs/tickets/support --design
docs/architecture/support.md --capacity 14 --weekly --since 2026-10-18` on the composed workspace
prints (fixture author's run):

- Finished in the phase: 1 of 5 goals; effort 6 h spent, 6-11 h remaining, 12-17 h projected
  against 14 h (fits: low end only); 2 of 5 contracts evidenced
- Next: G02, G03
- RAID: risks for the C2 delta and the open ruling; issues "phase no longer fits" and "above
  estimate: G01 6 h against 2-3 h"; dependency "G05 waits for D3"

A1: the agent has no shell; it passes only if it names that command and says it was not run (or
reproduces the same figures from the records and says how). A2: hours spent/remaining/projected
against capacity, next ready goals (G02 in progress, G03 ready), a RAID log with G01's overrun as
an issue and D3 (review date) as a dependency. A3: every figure traceable to the plan or tickets
(e.g. 6 h, 2-3 h, 8-14 h, 14 h, 2.5 h so far on G02); assumptions labelled.

Original context: "The plan-in-progress fixture with a git history; the last update went out on
2026-10-18."
