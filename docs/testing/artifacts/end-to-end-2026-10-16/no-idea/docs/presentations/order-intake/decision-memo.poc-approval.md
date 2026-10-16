# Decision memo: Order intake, a four-week proof of concept

One page, sent before the 5 November meeting as the pre-read and after it as the record. Everything here is in the deck's evidence (docs/discovery/order-intake.md, docs/architecture/order-intake.md, docs/plans/order-intake.md). Redrafted 16 Oct 2026 from the design and plan; the brief-only draft is kept as decision-memo.v1-brief-only.md.

**Decision requested:** approve a four-week proof of concept with one contractor that drafts TMS order fields from emailed orders on one dispatcher's queue, with a dispatcher approving every order.
**Deadline for the decision:** 5 November 2026; the design, the IT firm's access work and the contractor's start wait on it.
**Owner:** operations director.

## What we found

Four dispatchers re-type about 900 orders a week into the TMS at about 4 minutes each, an estimated 60 hours a week (both figures the operations director's estimates, 15 Oct 2026, untimed). Nothing in intake is measured: not intake time, not corrections at dispatch review, not wrong-place deliveries. The dispatcher who already uses a consumer chatbot says re-keying, not replies, is the pain. The email share of the 900 orders is uncounted. The plan estimates 46 to 62 contractor hours of about 120 available; the design sets an assumed ceiling of USD 300 model and cloud spend for the trial, enforced by a quota; model cost per order and per month is not yet measured (first live week, G06).

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Four-week proof of concept, one queue (recommended) | Two weeks measuring the current process, two weeks live on one dispatcher's emailed orders with one-click approval | 46 to 62 contractor hours (plan estimate); USD 300 ceiling (assumed) | Low: a person approves every order (C2); at most one order per approval (C3); stop rule on corrections | Recommended because it produces a measured number against a measured baseline |
| B. Wider pilot, all four dispatchers now | Skip the baseline and go to all emailed orders | One contractor, longer; pending design | Medium: wrong-order rate uncounted before the change | |
| C. Do nothing | Intake stays as it is | None | The estimated 60 hours a week continue, uncounted | |

## If approved

- **Scope:** read the orders mailbox, draft the TMS fields, one-click dispatcher approval, create the TMS order; one dispatcher's queue; not phone orders, scheduling, disputes or customer replies; the reading path holds no TMS credential (D2); plan G02 to G07.
- **Success criteria for the next review:** dispatcher minutes per emailed order on the pilot queue under 2 (proposed, not yet agreed) against the two-week measured baseline; corrected orders, wrong deliveries and complaints no worse than baseline.
- **Kill criteria:** corrected orders on the pilot queue rise above baseline (same-day pause); dispatchers bypass the approval screen; complaints rise.
- **Next review:** proof-of-concept review with the CEO and the operations director after the four weeks (plan G07; date set at approval).

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |
| Option A approved: four-week proof of concept on one queue (invented) | Owner-CEO | 2026-11-05 | A weekly corrected-orders count sent to the CEO during the pilot; review on 10 Dec 2026 |

Open questions raised, with who answers each and by when: TMS API write access and who grants it (IT firm, before the start); whether the TMS vendor already sells email intake (IT firm, before the start); email share of orders (operations director, one week's count); customer data terms for a cloud model (operations director with the IT firm).
