---
stage: production-approval
audience: business
minutes: 15
title: Campaign assistant: proof-of-concept review and production decision
sources: docs/discovery/campaign-assistant.md, docs/architecture/campaign-assistant.md, docs/plans/campaign-assistant.md
decision: Fund the production build of the campaign assistant for single-business advertisers (agencies excluded), conditional on the two unrun acceptance cases passing and a production estimate approved by 13 November 2026
decider: Director of SMB Sales
date: 2026-10-30
---

## Campaign assistant: what the proof of concept measured, and the decision we ask for on 30 October
Covers: title
Notes: Summary first, discussion after. The question today is whether to fund the production build; our answer is yes, at a reduced scope and with two conditions, and the next twelve minutes show the evidence for and against that.

---

## The proof of concept met its two measured criteria; we recommend funding production for single-business advertisers once two unrun checks pass
Covers: summary
Evidence: G04/A1, G04/A3, G03/A3, G04/A2, docs/plans/campaign-assistant.md Summary; measured
Notes: Situation: small advertisers complete 31% of checkouts, and product choice is where most of them leave. Complication: the proof of concept measured 36% completion on 312 assisted sessions with refunds unchanged, but two acceptance cases were never run and the production cost is not estimated. Question: fund, extend or stop. Answer: fund, for single-business advertisers only, conditional on the two checks and an approved estimate. Pause here; if we lose the room after this slide, this slide is the argument.

- We measured: checkout completion 36% on 312 assisted sessions (10 to 23 October 2026) against the 31% baseline; refunds 3%, unchanged
- Not run: duplicate-order-on-retry (G03/A3) and expired-quote requote (G04/A2)
- Not estimated: production build hours and monthly running cost
- Ask: fund production at reduced scope, two conditions, decision by the Director of SMB Sales on 30 October 2026

---

## Two of the two outcome criteria agreed on 12 September were met, measured by portal analytics and finance on live advertisers
Covers: criteria-results
Evidence: G04/A1, G04/A3, docs/plans/campaign-assistant.md G04; measured
Notes: These are the criteria written into the plan before the build, not chosen afterwards. Completion was measured by the Analytics team from portal analytics; refunds by the finance export of 24 October. Both on assisted sessions only. Then move to the chart.

| Criterion | Threshold | Measured | Method and sample | Case |
| --- | --- | --- | --- | --- |
| Checkout completion on assisted sessions | at or above 34% on at least 300 sessions | 36% (112 of 312) | portal analytics, 10 to 23 October 2026, assistant offered to a random half of sign-ins | G04/A1 passed |
| Refunds on assisted orders | at or below the 3% baseline | 3% (3 of 112 orders) | finance export, 24 October 2026 | G04/A3 passed |

---

## Checkout completion moved from 31% to 36% on 312 assisted sessions; unassisted sessions in the same fortnight sat at 30%
Covers: criteria-results
Evidence: G04/A1, docs/discovery/campaign-assistant.md §2 baseline table; measured
Notes: Item comparison, three columns: the Q2 baseline, unassisted sessions in the measurement window, assisted sessions. Say the sample sizes out loud: 2,140 advertisers for the baseline, 312 assisted sessions for the result. Say also what we did not do: no significance test was run, and the plan records that. Five points on 312 sessions is a measured result with a wide margin, not a proven lift at scale; production measurement over a quarter is how we would know. Hand over: what did not work.

- Column chart: baseline 31% (663 of 2,140, Q2 2026); unassisted 30% (same window, context only); assisted 36% (112 of 312)
- Sample sizes printed on the chart
- No significance test run (plan G04 note)

---

## Two acceptance cases were never run, and one of them guards against a duplicate order
Covers: learned
Evidence: G03/A3, G04/A2, docs/plans/campaign-assistant.md R2; measured
Notes: This is the slide someone in the room already knows about, so we say it first. The duplicate-order check could not be run because the checkout sandbox cannot simulate a retry; the code is there, unexercised. The expired-quote check was not run because no live session hit the thirty-minute expiry and the synthetic case was not written. Neither is a failure; both are unknowns, and both become conditions of the ask. Eight of ten acceptance cases passed.

- G03/A3 NOT RUN: a repeated confirmation after a network retry creates no second order (contract C4); risk is a duplicate order and a refund
- G04/A2 NOT RUN: an expired quote is requoted before confirmation (decision D5)
- 8 of 10 acceptance cases passed; none failed

---

## What we learned changes the production plan in three places: agencies, retries and measurement
Covers: learned
Evidence: docs/architecture/campaign-assistant.md open decision; R1, R2, R3; D4
Notes: Three recorded findings. One, agency logins cannot be rights-filtered today, so production must exclude them until the Ad Products lead decides on delegation. Two, the retry path must be exercised in the checkout sandbox before any production order. Three, the two-week measurement is the only evidence of lift; production needs a quarter-long measurement built in from the first day. These are the plan's own risk entries, not new claims.

- Agency delegation is undecided (design open decision, R3); production scope excludes agencies
- Duplicate-order protection unexercised (R2); must pass before launch
- Lift measured over two weeks only (R1); production measures for a quarter

---

## Production scope: single-business advertisers in the existing checkout, offered to all sign-ins, sponsored by the Director of SMB Sales
Covers: production-scope
Evidence: docs/architecture/campaign-assistant.md delivery profile and floor; docs/plans/campaign-assistant.md G05; docs/discovery/campaign-assistant.md §6
Notes: The workflow change is small by design: the assistant sits before the existing checkout and every purchase still passes the existing confirmation. The sales desk keeps refund review as today. What is new is that the desk's unblock requests about product choice should fall; we have not measured that and will not claim it. The sponsor is the Director of SMB Sales, as recorded in the brief.

- Users: single-business advertisers; agencies excluded until the delegation decision
- Workflow change: assistant offered at product choice; checkout confirmation unchanged; sales desk keeps refund review
- G05 scope: observability and on-call, per-session budgets, evaluation set in CI with repeats, the two unrun cases
- Not measured: effect on sales-desk unblock requests (would be measured in production)

---

## The proof of concept cost 58 hours and $142; production hours and monthly cost are not yet estimated
Covers: cost
Evidence: docs/plans/campaign-assistant.md cost record; G04/A1 for the session count; G05; estimate
Notes: Actuals first. Fifty-eight human hours against fifty-six planned, and one hundred and forty-two dollars of model and cloud spend over the whole project, from the billing export. We estimate a per-session figure by division: about forty-six cents per assisted session, which includes build-time spend, so it is an upper bound. What we cannot give you today is the production number: the plan says G05 hours and monthly cost are not estimated until the scope is decided, and that is why the ask is conditional. The estimate comes back to you by 13 November.

- We measured: 58 human hours (planned 56); $142 model and cloud, 15 September to 24 October 2026
- We estimate: about $0.46 per assisted session ($142 ÷ 312 sessions, build-time spend included, so an upper bound)
- Not yet estimated: production build hours; running cost per month at full adoption (G05, after the scope decision)

---

## Three risks, each with a control and an owner, and one of them is already a condition of the ask
Covers: risks
Evidence: R1, R2, R3, docs/plans/campaign-assistant.md risks; docs/architecture/campaign-assistant.md deferred controls
Notes: Read the table left to right, consequence first. The duplicate-order risk is the one that turns into a refund and a complaint; its control is a test, and the test is a condition. The agency risk is contained by exclusion. The measurement risk is contained by measuring in production for a quarter.

| Risk | Consequence | Control | Owner |
| --- | --- | --- | --- |
| R2 Retry creates a duplicate order (C4 unexercised) | Refund, complaint | Run G03/A3 in the checkout sandbox before launch | Russ |
| R3 Agency login cannot be rights-filtered (C1) | Ineligible product sold | Exclude agencies until the delegation decision | Ad Products lead |
| R1 Lift may not hold at volume (312-session sample) | Build pays back less than expected | Quarter-long measurement in production; kill criterion at the next review | Director of SMB Sales |

---

## A person confirms every purchase and the sales desk reviews every refund; the model never sets a price or decides eligibility
Covers: risks
Evidence: C1, C2, C3, docs/architecture/campaign-assistant.md floor and contracts; G01/A1, G02/A1, G03/A1
Notes: Where people validate the output. The advertiser confirms each purchase against a quote; the pricing service sets every price and the rights service decides what is shown; the sales desk reviews refunds as it does today. Each of these is a contract with a passed acceptance case behind it. Accountability for a wrong answer to a customer sits with the sponsor, as the brief records.

- Advertiser confirmation bound to the quote (C3; G03/A1 passed, 8 of 8)
- Prices only from the pricing service (C2; G02/A1 passed, 40 of 40 quotes)
- Only rights-filtered products shown (C1; G01/A1 passed, 0 of 20 advertisers saw an unlisted product)
- Sales desk reviews refunds; sponsor accountable (discovery brief §6)

---

## Timeline: conditions closed by 13 November, production scope and estimate approved, first quarter-long measurement from launch
Covers: production-scope, timeline
Evidence: docs/plans/campaign-assistant.md schedule check and G05; estimate
Notes: We estimate the dates; the record holds only the review date. The two unrun cases and the G05 estimate come back within two weeks of the decision. Build dates follow the estimate, not this slide. Say plainly that nothing on this slide beyond 30 October is measured.

- 30 October 2026: decision (recorded in the plan as the wait the next phase depends on)
- By 13 November 2026 (estimate): G03/A3 and G04/A2 run; G05 hours and monthly cost estimated; delegation decision requested from the Ad Products lead
- Build and launch dates: set by the G05 estimate, not yet known

---

## Decision: stop, extend the proof of concept, or fund production at reduced scope; we recommend funding with two conditions, Director of SMB Sales, 30 October 2026
Covers: ask
Evidence: G04/A1, G04/A3, G03/A3, G04/A2, G05; docs/presentations/campaign-assistant/decision-memo.md
Notes: Three real options. Option A, fund production for single-business advertisers, conditional on the two cases passing and an estimate you approve by 13 November; we recommend it because the two measured criteria were met and the open items are checks, not failures. Option B, extend the proof of concept by two weeks to close the checks first and decide again; it costs a two-week wait and the same work. Option C, stop; the proof of concept's code and evaluation set are kept. If nothing is decided today the next review is in two weeks and the developer is reassigned. You receive the one-page memo now and the decision record after.

- A. Fund production at reduced scope with two conditions (recommended)
- B. Extend the proof of concept two weeks to run G03/A3 and G04/A2, then decide
- C. Stop; keep code and evaluation set
- Decider: Director of SMB Sales; date: 30 October 2026; if undecided: re-review in two weeks

---

## Appendix: the baseline, who measured it and when
Covers: questions
Evidence: docs/discovery/campaign-assistant.md §2; measured
Notes: For the question "what is the baseline and who measured it".

- Portal analytics export, Q2 2026 (1 April to 30 June), pulled by the Analytics team on 14 August 2026
- 2,140 advertisers started checkout; 663 completed; 31%
- Product choice lost 38%, creative upload 12%, payment 19%

---

## Appendix: what the result rests on, and what was not measured
Covers: questions
Evidence: G04/A1, G04/A3, docs/plans/campaign-assistant.md G04 and G05; measured
Notes: For "how many users is this based on", "what would make you stop" and "what does it cost per month".

- 312 assisted sessions, 10 to 23 October 2026, random half of sign-ins; 112 completed; 3 refunds of 112 orders
- Not measured: statistical significance of the lift; effect on sales-desk requests; cost per month at full adoption (G05 would estimate it)
- Stop if: production measurement over a quarter shows completion at or below the 31% baseline, or refunds above 3% (kill criteria proposed in the memo, not yet agreed)

---

## Appendix: what happens if the model's price or behaviour changes, and who signed off
Covers: questions
Evidence: docs/architecture/campaign-assistant.md deferred controls and D2; docs/discovery/campaign-assistant.md §6; assumption
Notes: For "what if the model changes" and "who has signed off". The honest answer on model change is that the proof of concept has no evaluation set in CI; that is a G05 item. On sign-off, the design was reviewed by the Platform team lead and the Head of Pricing on 9 September 2026.

- Model price or behaviour change: no CI evaluation set yet (deferred control, G05); prices and eligibility are never computed by the model (D2), so a model change cannot change a price
- Sign-off so far: design reviewed by the Platform team lead and the Head of Pricing (design header); sponsor is the Director of SMB Sales
