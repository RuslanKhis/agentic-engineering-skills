# spec-kit, OpenSpec, Conductor and HumanLayer alignment — 26 October 2026

Source note: [comparison](../research/spec-tools-comparison-2026-10-26.md).

## Changed journey

`adk-system-designer`, checking a plan against the code before a phase
review; `adk-engineer`'s Finish step for manual checks.

## Fresh-agent trial

A fresh agent with only the skill packages copied the designer's
plan-in-progress fixture into a git repository, committed it as the
phase's base, then built a phase whose records all said finished while the
code disagreed: a later commit undid contract C1's owner check and skipped
its test, a withdrawn capability (`bulk_delete`) stayed bound, a file
outside every ticket's `touches` trusted an `X-User-Id` header, and an
OAuth manual check was ticked with no person or date. It then ran the
designer's checkpoint as asked, editing nothing.

| Step | Result |
| --- | --- |
| `plan_status.py` (report) | exit 0, "nothing ready": no sign of trouble |
| `--gate --base <base>` | exit 1: the out-of-`touches` file (and two empty package files) |
| `--gate --base` with a bad commit | exit 1, "diff not verified" |
| fresh-context review | CRITICAL: C1 contradicted, the header trust, `bulk_delete` still bound; WARNING: the unconfirmed OAuth check, thin evidence |

All four planted defects were caught: the script caught one, the review the
other three. Ease: 3 of 5.

## Frictions and fixes (same day)

1. No prompt shipped for the judgement half. Fixed: `assets/code-review-prompt.md`.
2. The gate required the review goal itself to be finished, so it could
   never pass before that goal. Fixed: presentation and teardown goals are
   excepted, with the test updated.
3. A decision blocker (`D3`) never clears in `plan_status.py`. Not changed:
   existing behaviour outside this source, noted for the designer's next
   review.
4. No script checked manual confirmations. Fixed: the gate fails on a
   manual line without a named person and date, or marked owed (tested).
5. No script checked withdrawals, and no design-cell format was given.
   Fixed: the gate requires a `SHALL NOT` item tagged with the withdrawn ID
   (tested), and the cell format is stated.
6. Empty package files failed the gate. Fixed by the existing rule, now
   stated: implementers add the files they create to `touches`.
7. `check_tickets.py` flags `parallel_safe` on finished tickets. Not
   changed: outside this source.
8. The plain report gave false comfort. Fixed: its "nothing ready" prompt
   points to the gate and the review.
9. The fixture lacks a **Resume here** and change table. Not changed: a
   test fixture, not guidance.
10. The checkpoint text was one dense paragraph. Fixed: four numbered steps.

## Limits

The review's grading is a prompt pattern; its quality was observed once.
