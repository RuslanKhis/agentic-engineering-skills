# Decision memo: campaign assistant, production build

One page, sent before the 30 October 2026 review as the pre-read and after it
as the record. Everything here is in the deck's evidence
(`production-approval-business.md`); nothing new appears in this memo.

**Decision requested:** Fund the production build of the campaign assistant
for single-business advertisers (agencies excluded), conditional on
acceptance cases G03/A3 and G04/A2 passing and a G05 estimate (hours, cost
per month) approved by 13 November 2026.
**Deadline for the decision:** 30 October 2026; the plan's G05 does not start
until it is made, and the developer is reassigned if nothing is decided.
**Owner:** Russ Khissami (developer); sponsor Director of SMB Sales.

## What we found

Checkout completion on assisted sessions was 36% (112 of 312 sessions, 10 to
23 October 2026, portal analytics; plan G04/A1) against the 31% baseline (663
of 2,140 advertisers, Q2 2026; discovery brief §2); refunds were 3% of
assisted orders (3 of 112; G04/A3), unchanged from the baseline. Both
criteria agreed in the plan on 12 September were met. The proof of concept
cost 58 human hours and $142 of model and cloud spend (plan cost record).
Two acceptance cases were not run: G03/A3, a repeated confirmation after a
retry creating no second order (contract C4), and G04/A2, an expired quote
being requoted (D5). Not measured: statistical significance of the lift (no
test was run on 312 sessions), effect on sales-desk requests, cost per month
at full adoption, and the hours production hardening (G05) needs.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Fund production at reduced scope with two conditions | Build G05 for single-business advertisers; agencies excluded until the delegation decision; launch only after G03/A3 and G04/A2 pass | Not estimated (G05); estimate due 13 November 2026 | Lift measured on 312 sessions over two weeks may not hold (R1); C4 untested until the condition is met (R2) | Recommended because both agreed criteria were met and every open item is a named check or estimate, not a failure |
| B. Extend the proof of concept two weeks | Run G03/A3 and G04/A2, write the G05 estimate, decide again on 13 November | About the same work as A's conditions, plus a two-week wait | Same evidence at the next review; developer time spent waiting on a decision | Reasonable if the decider will not fund without the estimate in hand |
| C. Stop | Keep code (`poc-0.3`), evaluation cases and documents; no production | None further | Baseline stays at 31% completion | Not recommended by the measured result |

## If approved

- **Scope:** G05 (observability and on-call, per-session budgets, evaluation
  set in CI with repeats, the two unrun cases), single-business advertisers
  only, by the Platform team and Russ; hours to be estimated by 13 November
  2026. Cut line: nothing beyond the deferred-controls table.
- **Success criteria for the next review:** checkout completion on assisted
  sessions at or above 34% over a full quarter of production; refunds at or
  below 3% (proposed; same thresholds as G04).
- **Kill criteria:** completion at or below 31% over the quarter, or refunds
  above 3% (proposed, not yet agreed).
- **Next review:** after the G05 estimate (13 November 2026, Director of SMB
  Sales); production results after the first full quarter.

Pre-wiring record: `pre-wiring.md` in this folder.

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |
| | | | |

Open questions raised, with who answers each and by when.
