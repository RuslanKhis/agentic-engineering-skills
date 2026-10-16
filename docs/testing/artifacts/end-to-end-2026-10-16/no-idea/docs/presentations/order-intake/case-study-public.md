---
stage: case-study
audience: public
minutes: 10
title: Emailed orders in 1.6 minutes instead of 4.4: an order-reading assistant built with Google Gemini
sources: docs/presentations/order-intake/case-study.md (draft), docs/plans/order-intake.md (G02, G09; evidence invented and labelled), docs/architecture/order-intake.md
decision: Information for the Google Cloud account team; ask whether the story is one Google would produce
decider: Google Cloud account manager (via the IT firm; name not given)
date: 2027-06-10
---

## Emailed orders in 1.6 minutes instead of 4.4: an order-reading assistant built with Google Gemini
Covers: title
Evidence: docs/plans/order-intake.md G02, G09 (measured)
Notes: A regional carrier measured its order intake for two weeks, then put a reading assistant in front of four dispatchers. This is what it did on 8,640 orders over a quarter, and what we would like to ask you.

---

## Four dispatchers re-typed about 900 free-text emailed orders a week, and nobody had measured it
Covers: challenge
Evidence: docs/discovery/order-intake.md §1, §2 (reported estimates, Oct 2026); docs/plans/order-intake.md G02 (measured baseline)

- About 300 customers, 300 email formats; five groups of fields re-keyed per order
- Estimated 4 minutes an order; measured in shadow mode: 4.4 minutes median on 318 orders
- Corrected orders and wrong deliveries uncounted until the baseline fortnight

Notes: The challenge was ordinary clerical work that nobody had timed. The first thing built was a clock: two weeks of timestamps on every emailed order before any model touched one.

---

## One model call drafts the order; a dispatcher approves every one; ordinary code writes it
Covers: solution
Evidence: docs/architecture/order-intake.md §2, D1, D2, C2, C3, C5

- A Google Cloud Agent Development Kit (ADK) agent with a fixed output schema and no tools, running Gemini through Vertex AI
- Draft beside email; one-click approval bound to the exact payload; one order per approval
- Cloud Run, Firestore, Secret Manager; email text never in logs; at most two model calls per email

Notes: The model decides only what the email says. Everything with an effect, which mail is read, when an order is created, how much is spent, is code the model cannot reach. That split is the reason the dispatchers trusted it.

---

## Over a quarter, 1.6 minutes an order on 8,640 orders, with corrected orders flat at 2.9%
Covers: results
Evidence: docs/plans/order-intake.md G09 outcome and adoption (measured, 25 Jan to 25 Apr 2027); G02 baseline (one queue)

- Weekly medians 1.3 to 2.4 against the 4.4 baseline; baseline measured on one of the four queues
- Corrected at review 2.9% against 2.8%; wrong-place deliveries 0.13%
- 4 of 4 dispatchers active every week; 94% of emailed orders through the approval screen

Notes: Same clock before and after: mailbox received to order created. The caveat is on the slide: the before was measured on one queue, and the other three are assumed to have matched it.

---

## Cost came in at about USD 200 to 250 a month, under USD 0.10 an order, against the estimate
Covers: results
Evidence: docs/plans/order-intake.md G09 cost (billing exports Feb to Apr 2027, measured; shown as a range for publication)

- Three monthly bills within the range; estimate before production was USD 230
- About 90 contractor hours to build the pilot and the production step; two prompt revisions since

Notes: The exact figures are in the internal draft; the public version carries a range at the sponsor's choice. The build was one contractor, part time, with the hosting firm providing access and the test environment.

---

## What did not improve: freed hours not yet reassigned, complaints unchanged, one queue trained twice
Covers: results
Evidence: docs/plans/order-intake.md G09 (adoption, outcome caveats); measured

- About 400 dispatcher hours over the quarter (we estimate: 2.8 minutes x 8,640), not reassigned yet
- Complaints counted firm-wide only, 55 to 63 a week, unchanged
- One dispatcher kept typing in February; a second training hour fixed it

Notes: Published stories rarely say this part, and the sponsor wants it said: the saving is in minutes, not yet in money, and the complaint line did not move either way.

---

## Next: discovery on phone orders, a customer order form, and a story if Google wants one
Covers: next
Evidence: docs/plans/order-intake.md Later list (phone orders 27% of orders, G09); case-study.md submission pack

- Four-week discovery on phone orders, approved 6 May 2027; no build promised
- Order form for the five largest customers, a process change
- Ask: would Google produce the story; logo use for the firm's site (requires Google consent); no announcement or event

Notes: The one ask: whether this is a story your reference team would produce, and what you need from us. The pack lists our approvals and their dates; the firm, the hosting firm and the customers stay unnamed until each consents.

---

## Appendix: publishable status per number and the approvals still open
Covers: appendix
Evidence: docs/presentations/order-intake/case-study.md results table and submission pack

- As is: minutes per order, corrected orders, adoption; as a range: cost; omitted: incidents
- Open: sponsor read-through, legal and communications review (no in-house function), diagram scrub by the hosting firm, two quotes unapproved
- Relationship: billing account held by the hosting firm; agreement type and partner tier to confirm

Notes: Held for questions.
