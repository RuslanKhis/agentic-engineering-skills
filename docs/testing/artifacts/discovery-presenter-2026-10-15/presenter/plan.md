# Implementation plan: campaign assistant proof of concept

From `docs/architecture/campaign-assistant.md`. Profile: proof of concept,
4 weeks, one developer (Russ). Written 12 September 2026; evidence sections
updated 24 October 2026.

## Schedule check

- Available: 4 weeks × 0.5 FTE = about 80 hours (one developer, half time).
- Planned: G01 12 h, G02 10 h, G03 14 h, G04 20 h (including the two-week
  measurement window) = 56 h. Buffer 24 h.
- Calendar: build 15 September to 9 October 2026; measurement 10 to 23
  October 2026; review 30 October 2026 (the wait the next phase depends on).
- Cut line: G01 to G04 ship; G05 does not start until the review decides.

## Goals

### G01 Eligible products only (C1) — COMPLETE, 11 h

- A1 For 20 test advertisers across 4 regions, every product named by the
  agent is in the rights service's list for that advertiser — PASSED (0 of
  20 named an unlisted product; log `evidence/g01-a1.json`).
- A2 An advertiser asking for an ineligible product is told it is not
  available and offered the eligible ones — PASSED (5 of 5).

### G02 Quote relay (C2) — COMPLETE, 9 h

- A1 Every price the agent states equals the signed quote — PASSED (40 of 40
  quotes in the test set).
- A2 "Give me a discount" produces no altered price — PASSED (10 of 10).

### G03 Confirmed purchase (C3, C4) — COMPLETE, 15 h

- A1 `create_order` is refused without a confirmation token for the current
  quote — PASSED (8 of 8).
- A2 The order created matches the confirmed quote's product and price —
  PASSED (8 of 8).
- A3 A repeated confirmation after a network retry creates no second order
  (C4) — NOT RUN. The checkout sandbox could not simulate the retry; the
  idempotency key is implemented but unexercised.

### G04 Measured lift (D4) — COMPLETE, 23 h

Build measured: tag `poc-0.3` (commit 4f2e1c9), the same build the review
demo shows. Measurement by the Analytics team from portal analytics, 10 to 23
October 2026, assistant offered to a random half of sign-ins.

- A1 Checkout completion on assisted sessions at or above 34% on at least 300
  sessions — PASSED: **36%** (112 completed of 312 assisted sessions) against
  the **31%** baseline (Q2 2026, 2,140 advertisers). Unassisted sessions in
  the same window: 30% (not an acceptance case; recorded for context).
- A2 An expired quote is requoted before confirmation (D5) — NOT RUN. No
  session in the window hit the 30-minute expiry, and the synthetic case was
  not written.
- A3 Refunds on assisted orders at or below the 3% baseline — PASSED: **3%**
  (3 of 112 orders; finance export of 24 October 2026), unchanged.

No significance test was run on the lift; the sample is 312 sessions.

### G05 Production hardening — PLANNED

Scope from the deferred-controls table: observability and on-call, per-session
budgets, evaluation set in CI with repeats, the two NOT RUN cases above, and
whatever the agency-delegation decision needs. Hours: not estimated; depends
on the review's scope decision. Per-month production cost: not estimated.

## Cost record

| Item | Amount | Source |
| --- | --- | --- |
| Human hours, G01 to G04 | 58 h (planned 56 h) | timesheet, 15 Sep to 24 Oct 2026 |
| Model and cloud spend | $142 | Cloud Billing, project `campaign-poc`, 15 Sep to 24 Oct 2026 |

## Risks recorded

- R1 The lift may not hold outside the two-week window or at full volume
  (sample 312 sessions). Control: production measurement over a quarter.
- R2 C4 unexercised (G03/A3): a retry could create a duplicate order and a
  refund. Control: run the case in the checkout sandbox before production.
  Owner: Russ.
- R3 Agency delegation undecided; C1 cannot hold for agency logins. Control:
  exclude agencies until decided. Owner: Ad Products lead.

## Summary

G01 to G04 complete. Checkout completion measured at 36% on 312 assisted
sessions (10 to 23 October 2026) against the 31% baseline; refunds 3%,
unchanged. 8 of 10 acceptance cases passed; G03/A3 (duplicate order on
retry) and G04/A2 (expired quote requoted) NOT RUN. Cost: 58 human hours,
$142 model and cloud. G05 planned, unscoped and unestimated until the review
on 30 October 2026 decides.
