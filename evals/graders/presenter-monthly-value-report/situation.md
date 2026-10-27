# presenter-monthly-value-report: what the fixture holds

Original context (rewritten because it named the two record problems A3 checks for):
"A brief with outcome measure, baseline, counter-metric and threshold sentences; a plan whose M
records include one outcome record without a baseline and one August window, and one September
incident record."

Composition: base claims-docs plus an overlay replacing the brief, the design (acceptance date
moved to 2026-08-06) and the plan (pilot live since 2026-08-25).

| Item | Where |
| --- | --- |
| Brief outcome, baseline, counter-metric, thresholds, decider | `docs/discovery/claims.md` §4 and §6: baseline 21 minutes; counter-metric re-routing 9%; two threshold sentences; decider Helen Okafor; senior owner Priya Shah; ceiling £900 a month |
| Outcome record without a baseline | `docs/plans/claims.md` M2 (13 minutes, September) has no baseline field; the baseline exists separately as M1 (kind baseline) and in the brief, but M2 itself does not carry it, so `check_value_report.py` reports "outcome: M2 has no baseline" |
| Stale window | M3 re-routing rate window 2026-08-25 to 2026-08-31; there is no September re-routing record, so the counter-metric for September is not measured |
| September incident | I1 2026-09-16 severity 2, closed 2026-09-19 |
| Cost per outcome | M6 £512 over M7 1,184 claims = about £0.43 per claim; M8 is an assumption (projection) |
| Adoption | M5 12 of 14 active, with a definition |

Verified on 2026-10-27: a report citing M2 under Outcome and M3 under Counter-metric makes
`check_value_report.py` exit 1 with exactly those two errors.

A3 needs a shell to run the checker; credit a report that names the missing baseline and the
stale August window as problems (and says the checker was not run) rather than hiding them.
A4: the call must name Helen Okafor and rest on a figure or threshold (e.g. M2 13 minutes vs the
15-minute threshold); a "scale" call is wrong while the counter-metric is unmeasured for September.

Changed on 28 October 2026 (Phase 11): A3 now carries its own no-shell escape in the assertion text, because judges graded the run step literally despite the note above. In a run without a shell, credit naming `check_value_report.py`, reporting it as not run, and naming both problems (M2's missing baseline field and the August-only M3 window); a claim that the step ran, with no output to show for it, is still a FAIL.
