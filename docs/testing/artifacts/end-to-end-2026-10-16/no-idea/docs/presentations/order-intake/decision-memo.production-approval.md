# Decision memo: Order intake, from pilot to all four dispatchers

One page, sent before the 10 December 2026 meeting as the pre-read and after it as the record. Everything here is in the deck's evidence (docs/plans/order-intake.md phase-1 evidence, invented and labelled; docs/architecture/order-intake.md). The proof-of-concept approval memo of 5 November is kept as decision-memo.poc-approval.md.

**Decision requested:** build order intake for all four dispatchers' emailed orders, a dispatcher approving every order, at about USD 230 a month (estimate) and 16 to 24 contractor hours (plan G08).
**Deadline for the decision:** 10 December 2026; the IT firm's January slots and the contractor's availability wait on it.
**Owner:** operations director.

## What we found

Dispatcher time per emailed order on the pilot queue fell from a measured 4.4 minutes (318 orders, 9 to 22 Nov, mailbox and TMS timestamps; plan G02) to 1.7 minutes (331 orders, 23 Nov to 6 Dec; G06/A1), under the 2-minute threshold agreed on 5 November. Orders corrected at dispatch review were 3.0% against 2.8% in the baseline, within the margin on this sample, and wrong-place deliveries were one in each period (G06). The pilot's model and cloud bill was USD 34.50 (billing export 7 Dec; G06). What did not work: 47 of 331 drafts needed an edit before approval, mostly dates and instructions; 12 came back "enter manually"; and one safety case, a lost TMS reply after approval (G05/A4), was never run because no test environment exists. Not measured: latency, complaints by queue, cost at four queues. The contractor spent 71 hours against an estimate of 46 to 62.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Build for all four dispatchers (recommended) | Same mailbox read in full, three more dispatchers trained by Maria, missed-mail alert, pinned release; G05/A4 run first in the IT firm's test environment | 16 to 24 contractor hours (G08, estimate); about USD 230 a month (estimate from G06 spend) | Low: a dispatcher approves every order (C2), one order per approval (C3); open: customer data terms for 280 customers (O4) | Recommended because the result held for two weeks on the same clock as the baseline and the counter-metric did not move |
| B. Extend the pilot to a second queue for four weeks | A second measured result before scaling | About 8 contractor hours (estimate); pilot-level spend | The result arrives in February; the IT firm's January slots are lost | |
| C. Stop | Maria's queue returns to typing; code, 50 test cases and 47 corrections kept | None | The measured 2.7 minutes an order on one queue is given back | |

## If approved

- **Scope:** G08: all emailed orders in the shared mailbox, traces, a missed-mail alert within the hour, release manifest with pinned model and prompt, O4 closed; built by the contractor, hosted by the IT firm; 16 to 24 hours.
- **Success criteria for the next review:** minutes per emailed order under 2 as the weekly median on each queue (proposed, not yet agreed); corrected orders no worse than 2.8% per queue; cost at or under USD 230 a month after the first bill (proposed).
- **Kill criteria:** corrected orders above 2.8% on any queue pauses that queue the same day; a duplicate TMS order from a repeated approval stops all queues until G05/A4 passes; a customer contract clause routes that customer to manual entry.
- **Next review:** results review with the CEO after 90 days of four-queue production (plan G09), late April 2027, business audience.

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |
| Option A approved: build for all four dispatchers (invented) | Owner-CEO | 2026-12-10 | G05/A4 passes in the IT firm's test environment before four queues go live; weekly corrected-orders count continues; results review after 90 days |

Open questions raised, with who answers each and by when: TMS test environment (IT firm, by 15 Jan 2027); on-call owner for the missed-mail alert (IT firm, by 15 Jan); customer data terms for the remaining customers (operations director, before four queues go live); whether freed dispatcher hours are reassigned (operations director, after the first production month).
