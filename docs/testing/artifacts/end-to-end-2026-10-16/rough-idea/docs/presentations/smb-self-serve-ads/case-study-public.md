---
stage: case-study
audience: public
minutes: 10
title: Northlight Media: guided product choice for small advertisers, Built on Google Cloud
sources: docs/presentations/smb-self-serve-ads/case-study.md, docs/plans/smb-self-serve-ads.md (phase 1 and 2 evidence), docs/architecture/smb-self-serve-ads.md
decision: Information for the Google Cloud account team; the ask is to route the submission pack to customer reference marketing
decider: Jonas Weber, Google Cloud account manager (invented)
date: 2027-04-21
---

## Northlight Media: guided product choice for small advertisers, Built on Google Cloud
Covers: title
Notes: Meeting version of `case-study.md`; every figure is in that draft with its evidence line. Company facts invented for this trial.

---

## The challenge: 38% of 2,140 small-business advertisers left the self-serve purchase at product choice in Q3 2026
Covers: challenge
Evidence: docs/discovery/smb-self-serve-ads.md §2 funnel table; measured, funnel export Q3 2026

- Product choice lost 38%; creative upload 12%, pricing 9%, booking 6%
- About 40 products across formats and regions; about 35 escalations a week to sales (reported)

Notes: Northlight Media sells advertising to small businesses through a self-serve platform. In the third quarter of 2026, 2,140 advertisers started a purchase and 38 percent left at product choice, more than the next three steps together, because about forty products across formats and regions gave no way to tell which one fitted. Sales took about 35 such escalations a week. The discovery set the measure and the baseline before anything was built: completion of that step, against 62 percent.

---

## The solution: one sentence in, one to three fitting products with reasons out; code filters, a Gemini model ranks, a person still confirms
Covers: solution
Evidence: docs/architecture/smb-self-serve-ads.md §2, C1 to C5, D1, D2; docs/presentations/smb-self-serve-ads/case-study.md solution section

- Cloud Run service in the platform project; catalogue filtered in code by region and format
- One Google Cloud Agent Development Kit (ADK) `LlmAgent` with a pinned Gemini model, fixed output schema, no tools; price and availability from the existing services, never from the model
- Logged per start to BigQuery; evaluated on 30 then 60 labelled cases as a release gate

Notes: The advertiser types one sentence, "weekend promotion for my bakery in the east of town", and sees one to three products that can run where she is, each with a reason. Code filters the catalogue first; one model call ranks the candidates and writes the reasons; code checks every id and reason against the list and attaches the price from the pricing service. The model never sees a price and cannot write anywhere. A person confirms every purchase, as before. The service runs on Cloud Run in the platform team's project and logs every start to BigQuery, which is how the result is measured.

---

## Results: completion 69.4% on 2,310 starts over Q1 2027 against 62%; in the pilot 70.8% against a 63.1% control; refunds 2.9%
Covers: results
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (outcome, counter-metric, adoption rows), phase 1 evidence (G06/A2); measured

- Chart: baseline 62% (Q3 2026) flat; pilot control 63.1% (298) and treatment 70.8% (312), Oct 2026; production 68.1, 69.9, 70.2% by month (740, 731, 839 starts)
- 78% of starts typed a sentence and saw a recommendation; 44% picked one; cost about $200 to $250 a month (range)

Notes: Three numbers. Over the first production quarter, 69.4 percent of 2,310 starts reached the next step against the 62 percent baseline, measured by the same funnel export and the same product owner; there was no control arm in production, so that is against last year's baseline. In the October pilot, with a concurrent control, 70.8 percent of 312 treated sessions got through against 63.1 of 298 control sessions, above the margin from chance on that sample. Refunds stayed at 2.9 percent. Cost ran about two hundred to two hundred and fifty dollars a month.

---

## What did not improve and what is still being measured: escalations are reported, not logged; two incidents; no control arm in production
Covers: results
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (escalations row, incidents table, open after the quarter); reported and measured kept apart

- Escalations reported down from about 35 to about 22 a week; not logged
- Incidents: a 2 h pricing outage absorbed by the fallback; a quota sized from pilot traffic exhausted by a marketing day, 142 starts on the fallback page, that day 58%
- Evaluation set runs once per release; no variance figure

Notes: The story is better for saying what did not work. Escalations to sales are reported down from about 35 to about 22 a week, but they are not logged, so that is a report. Two incidents: a two-hour pricing-service outage that the designed fallback absorbed with no wrong price shown, and a day when a marketing campaign exhausted a model quota we had sized from pilot traffic, leaving 142 advertisers with the plain catalogue page and that day at 58 percent. And the evaluation set runs once per release, so there is no variance figure.

---

## What's next: a discovery for the next funnel step and a one-month control arm with an escalation log; nothing promised beyond the plan
Covers: next
Evidence: docs/plans/smb-self-serve-ads.md open after the quarter; docs/presentations/smb-self-serve-ads/decision-memo.md options; not yet decided

- Discovery on creative upload (12%) and pricing (9%) from the Q3 2026 funnel
- Next release: 10% control arm for one month; escalation log
- Not planned: per-advertiser personalisation (reopens the data scope)

Notes: What's next is what the plan holds and nothing more: a two-week discovery on the next funnel steps, creative upload and pricing, and on the next release a one-month control arm on ten percent of starts with an escalation log, so the two numbers we cannot defend today become measured. Personalisation from account data is not planned, because it would reopen the data boundary the design kept narrow.

---

## The ask: route the submission pack to customer reference marketing; legal, communications and the security review are pending on our side
Covers: next, ask
Evidence: docs/presentations/smb-self-serve-ads/case-study.md submission pack; n/a for the numbers: none on this slide

- Pack: numbers with evidence lines, one quote (draft, not approved), diagram pending security review, attribution "Built on Google Cloud"
- Requires Google consent: story production, logo use, a joint announcement
- Owner: Jonas Weber (Google), the AI engineer (Northlight)

Notes: The ask for this meeting: route the pack to customer reference marketing and the Cloud Brand team. On our side the sponsor has approved; legal, communications and the security review of the diagram are pending, and the quote is a draft. Anything beyond a plain-text mention of Google Cloud, the logo, a joint announcement or story production, requires Google's consent and is listed that way in the pack.
