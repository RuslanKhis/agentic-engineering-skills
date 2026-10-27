---
stage: production-approval
audience: business
minutes: 15
title: Campaign shopping assistant, proof of concept review
sources: docs/discovery/campaign-assistant.md, docs/architecture/campaign-assistant.md, docs/plans/campaign-assistant.md
decision: Choose between stopping, extending the pilot with the missing safeguards, and building for production now; we recommend extending the pilot
decider: Clare Hollis (Chief Digital Officer)
date: to be confirmed (not in the record)
---

## Campaign shopping assistant: proof of concept review
Covers: title
Evidence: docs/plans/campaign-assistant.md M1, M4, M5; measured

Three of four agreed criteria met. Refunds unproven. Spend £386.

Notes: There is no recorded demo, so none is shown; the numbers come from the live campaign run. Build v0.4.0 produced the checkout and refund figures; the catalogue-accuracy figure comes from the earlier build v0.3.2. The answer comes first, discussion after, and you can interrupt me at any point to go to the decision. I am asking Clare Hollis to choose between three options, and I recommend we extend the pilot rather than build for production today. The reason is one number, which I will come to: one refund in thirteen orders.

---

## The proof of concept met three of four agreed criteria; we recommend extending the pilot, not building for production yet
Covers: summary
Evidence: docs/architecture/campaign-assistant.md S1-S4; docs/plans/campaign-assistant.md M1, M3, M4, M5; measured

- Situation: checkout completion was 3.1% in Q2 campaigns; shoppers left without size, material or delivery answers.
- Complication: refunds on assistant orders are unproven, and two safeguards were never tested.
- Answer: extend the pilot at a larger share of sessions.

Notes: Today, a shopper on a campaign page who cannot find a size or a delivery date either leaves or uses the contact form, and the answer arrives after the discount has ended. The baseline for completing a checkout was 3.1 percent in Q2. We built an assistant that answers from the catalogue and the delivery service, and ran it on 10 percent of landing-page sessions for three weeks. We measured three of the four criteria you agreed on 26 August as met: checkout completion, answer accuracy and spend. The fourth, refunds, is not met on its point estimate and cannot be settled on the sample we have. So the recommendation is to extend rather than build, and I will give three reasons.

---

## Criteria agreed on 26 August, and what we measured against each
Covers: criteria-results
Evidence: docs/architecture/campaign-assistant.md S1-S4; docs/plans/campaign-assistant.md M1, M3, M4, M5; measured

| Criterion | Threshold | Measured | Method and sample | Result |
| --- | --- | --- | --- | --- |
| S1 Checkout completion, assistant sessions | at least 3.6% | 4.2% (M1) | web analytics, 312 sessions | met |
| S2 Refund rate, assistant orders | not above 6.4% | 1 of 13 orders, 7.7% (M4) | order system, refunds to 24 Oct | not met; sample far too small |
| S3 Answers matching the catalogue | at least 95% | 96.5% (M3) | offline test, 200 questions, build v0.3.2 | met; earlier build |
| S4 Spend | within £1,500 | £386 (M5) | billing export | met |

Notes: Here is the table, spoken once. S1: 4.2 percent on 312 assistant sessions, against a threshold of 3.6; met. S3: 96.5 percent on 200 test questions against 95; met, but measured on build v0.3.2, not the v0.4.0 that ran on the campaign. S4: £386 against £1,500; met. S2, the refund rate: one refund among 13 orders from assistant sessions. That is 7.7 percent, we calculate, against a limit of 6.4. By the letter of the criterion it is not met. In fairness, one order is the difference between 7.7 percent and zero, so it is a warning, not a verdict. Three of four, then, with the fourth open.

---

## Checkout completion was 4.2% on assistant sessions against a 3.1% baseline, but only 0.8 points above the same-campaign control
Covers: criteria-results
Evidence: docs/plans/campaign-assistant.md M1, M2; docs/discovery/campaign-assistant.md §4; measured; estimate (interval)

- We measured: 4.2% with the assistant (312 sessions), 3.4% without (27,600 sessions), 3.1% in Q2.
- We estimate: 13 checkouts out of 312; the plausible range is roughly 2.5% to 7.0%, which includes the 3.6% threshold and the 3.4% control.

Notes: This is the number that matters most, so I want to be careful with it. Against the Q2 baseline the lift is 1.1 points. But the campaign itself ran better than Q2: sessions without the assistant completed at 3.4 percent. Against that fair comparison the lift is 0.8 points. And 4.2 percent on 312 sessions is about 13 checkouts. We estimate that the true rate could plausibly sit anywhere from about 2.5 to 7 percent, a range that includes the control. So the honest reading is: encouraging, passes the agreed threshold, but not yet distinguishable from chance. One more caveat: people who chose to open a chat may be more ready to buy than the average shopper. The record does not say how the control group was built, so I cannot rule that out.

---

## What did not work: refunds are unproven, and two safeguards were never tested
Covers: learned
Evidence: docs/plans/campaign-assistant.md M4, G02/A3, G03/A3; measured

- Refunds: 1 of 13 assistant orders (7.7%) against a 6.4% limit; 30-day window not complete.
- Not run: shopper pointed to checkout if the delivery service is down (G02/A3).
- Not run: assistant hidden when a day's spend reaches £60 (G03/A3); storefront flag not delivered.

Notes: Three things did not work, and each has an answer. First, refunds. We have 13 assistant orders; a rate from 13 orders ranges from about 1 percent to 33 percent, so we cannot say either way. Orders ran to 19 October and refunds were counted to 24 October, so most orders have not had their full 30 days; the last ones reach it on 18 November. The answer is to wait for that date and to enlarge the sample. Second, two acceptance cases were never run. If the delivery service is down, we have not shown the assistant sends shoppers to checkout; there is no test stand-in for an outage. And the £60 daily spend stop: the spend alert works, but hiding the assistant at the cap needs a flag from the storefront team that was not delivered. Actual spend never came near the limit, but the safeguard is not proven.

---

## What we learned changes the plan: the pilot is too small to settle refunds, and the record has gaps to close
Covers: learned
Evidence: docs/plans/campaign-assistant.md M1, M3, M4, G03/A3; docs/architecture/campaign-assistant.md C4, D3, D5; measured; assumption

- At 10% of sessions we got 13 assistant orders in three weeks; refunds will not resolve at that rate.
- The accuracy test ran on v0.3.2; the campaign ran v0.4.0.
- The design lists the spend stop (C4) as evidenced; the plan says not run.

Notes: Three findings change the plan. One: at a 10 percent share we got 13 orders in three weeks. Waiting longer at that share will not settle a refund rate; we need a larger share of sessions, which is your call. Two: the accuracy test was run on the earlier build, so it should be repeated on the build that ran live. Three: a housekeeping point. The design document lists the £60 spend stop as evidenced, but the plan records the matching case as not run. The plan is the more recent record, and I have treated it as correct; the design needs correcting.

---

## Recommended scope: keep to the campaign pages, finish the two safeguards, and hold production until the refund evidence is in
Covers: production-scope
Evidence: docs/architecture/campaign-assistant.md D3, D4, D5, D6; docs/plans/campaign-assistant.md D6; assumption

- Design option for production (D5): every campaign page and the account area; not decided.
- The account area conflicts with D3: no customer account data is read.
- D6 open: may Pinwheel Studio edit offer text without Bramble sign-off? Owner Clare Hollis.

Notes: The design sketched production as every campaign page plus the account area, and marked it undecided. We have no evidence about the account area, and it contradicts the rule we built on, that the assistant reads no customer account data. So I would not take that to production on this evidence. What I recommend is the same campaign pages, with the two missing safeguards delivered and the refund evidence completed. There is also one open decision that is yours: whether the creative agency, Pinwheel Studio, may edit campaign briefs and offer text without Bramble's sign-off. Today Bramble's e-commerce team edits that file. It matters before production, because the offer text is what the assistant says to shoppers.

---

## The proof of concept cost £386 against the £1,500 allowed
Covers: cost
Evidence: docs/plans/campaign-assistant.md M5, G01-G04 spend and actual hours; docs/architecture/campaign-assistant.md S4; measured; estimate

- We measured: £386 (model £235, cloud £151), 1 Sept to 24 Oct; 19.5 build hours across G01 to G04.
- We estimate: £284 run cost over 312 assistant sessions is about £0.91 a session (model alone about £0.60).
- Production running cost: not yet measured.

Notes: The spend was measured from the billing export: £386 in total, of which £235 for the model and £151 for cloud hosting, a quarter of the £1,500 allowed. The three-week campaign run alone cost £284. Dividing that by the 312 assistant sessions, we estimate about 91 pence a session, of which about 60 pence is the model. Both figures are a snapshot: the cloud part may not scale with sessions, and the run was small. Build effort was 19.5 hours against a plan of 15 to 22. What I cannot give you is a production monthly cost, because that depends on scope and volume nobody has chosen. For an extension at the same share, we would expect a cost of the order of the run, £284 for three weeks; it grows with the share of sessions.

---

## Three risks the extension must close, each with a control and an owner
Covers: risks
Evidence: docs/plans/campaign-assistant.md G02/A3, G03/A3, M4, D6; docs/architecture/campaign-assistant.md C2, C4; assumption (owners marked proposed)

| Risk | Control | Owner |
| --- | --- | --- |
| Refunds rise on assistant orders | Re-measure at 30 days on a larger sample | Raj Patel (measures M4) |
| Spend cap does not hide the assistant | Storefront flag, then run G03/A3 | Storefront team; name proposed: Raj Patel |
| Delivery service down: no fallback shown | Build an outage test double, run G02/A3 | Larkspur Digital (Tom Reid) |

Notes: Three risks, each with a control and an owner. The refund risk: Raj Patel's team already measures it from the order system. The spend risk: the daily cap is in place as an alert, and the missing piece is the storefront flag; the record names a team but no person, so I have proposed Raj Patel to chase it, and he should confirm. The delivery risk: Larkspur Digital builds the outage test, and runs the case. I would add that the offer-text question, D6, is a fourth risk, and it is with Clare Hollis.

---

## A shopper confirms every basket add; no person reviews answers, and no governance pack exists
Covers: risks
Evidence: docs/architecture/campaign-assistant.md C1, C3, D3; docs/plans/campaign-assistant.md G03/A1, G03/A2; measured; n/a: no governance pack recorded

- Basket adds need the shopper's confirmed size and quantity (C3); out-of-stock sizes are refused (G03/A2).
- Product answers come from the catalogue, with a link (C1).
- No customer account data is read (D3).

Notes: The assistant answers from the catalogue and adds to the basket only after the shopper confirms size and quantity, and it refuses out-of-stock sizes. Those cases passed locally on 24 September. Nobody reviews individual answers before the shopper sees them; the control is that answers come from the catalogue entry. There is no governance pack in the record, so I cannot show a system card. Clare Hollis is the accountable sponsor.

---

## The refund evidence is complete on 18 November; every later date is for you to set
Covers: production-scope
Evidence: docs/plans/campaign-assistant.md M4 (orders to 19 Oct, 30 days); assumption

- 19 October: the campaign run ended.
- 18 November: the last order has had 30 days (we calculate).
- To be set: extension start and review date.

Notes: The last assisted orders were on 19 October, so their 30-day refund window closes on 18 November. That gives a first checkpoint: we can re-read the refund figure then, even before any extension. I have not invented later dates; the extension's start and review date are for the decision.

---

## Decision: stop, extend the pilot, or build for production; we recommend extending
Covers: ask
Evidence: docs/architecture/campaign-assistant.md S1-S4; docs/plans/campaign-assistant.md M1, M4, M5; assumption

| Option | What it means | Our view |
| --- | --- | --- |
| Stop | Keep the code and test set; no further spend | Safe, but forfeits an encouraging result |
| **Extend (recommended)** | Larger share of campaign sessions; deliver G02/A3 and G03/A3; re-run accuracy on v0.4.0; re-measure refunds | Cost estimate about £284 per three weeks at the same share; scales with share |
| Build for production now | Every campaign page; account area undecided (D5) | Refunds unproven; two safeguards untested |

Decider: Clare Hollis. Date: to be confirmed. If nothing is decided, no new evidence accrues.

Notes: The options. Stop: we keep the code and the test set and spend nothing more. Extend: a larger share of sessions, the two missing safeguards, accuracy re-tested on the live build, refunds re-measured. We estimate the cost at about £284 for three weeks at the same share; more sessions would cost more. Build for production now: I do not recommend it, because refunds are unproven and two safeguards were never tested. The decision is Clare Hollis's, and I need it on a date she sets. Credit: Larkspur Digital built and measured the assistant, Raj Patel's team supplied the analytics and order data, and the storefront team ran the 10 percent split. Now to questions, and then I will restate the decision.

---

## Expected questions and where the record answers them
Covers: questions
Evidence: docs/plans/campaign-assistant.md M1-M5; docs/discovery/campaign-assistant.md §4; n/a: question bank; measured

| Question | Answer from the record |
| --- | --- |
| What is it worth in pounds? | Not yet measured: the record has no order value; the extension would add it |
| What would production cost per month? | Not yet measured; depends on scope (D5) and volume |
| Is the 0.8-point lift real? | Not distinguishable from chance on 312 sessions (13 checkouts); extension tests it |
| Are assistant users just keener buyers? | Not ruled out; the record does not say how the control was built |
| How many shoppers used the assistant? | 312 sessions (M1); 10% of landing-page sessions were eligible (D2) |
| Was customer data used? | No customer account data is read (D3) |
| Was the demo the measured build? | No demo; M1 and M4 are build v0.4.0, M3 is v0.3.2 |

Notes: Reference only; not spoken. Any answer not in the record is "I don't know; I will find out and send it to Clare Hollis by a date she names."

---

## Acceptance cases: six passed, two not run
Covers: appendix
Evidence: docs/plans/campaign-assistant.md G01-G03; measured

| Goal | Passed | Not run |
| --- | --- | --- |
| G01 page | A1 (within 2 seconds), A2 (10% split) | none |
| G02 answers | A1 (catalogue match), A2 (delivery API) | A3 (delivery API down) |
| G03 basket | A1 (confirm), A2 (out of stock) | A3 (hide at £60 a day) |

Notes: Reference only. Most G02 and G03 passes were local, not live; G01 passed local and live.
