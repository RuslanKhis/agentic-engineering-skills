---
stage: final-results
audience: business
minutes: 15
title: Guided product choice: the first production quarter against the baseline
sources: docs/plans/smb-self-serve-ads.md (phase 2 evidence), docs/discovery/smb-self-serve-ads.md, docs/architecture/smb-self-serve-ads.md
decision: Information only on the result; one decision asked: fund a discovery sprint for the next funnel step, or keep the service as it is
decider: Director of SMB Sales
date: 2027-04-14
---

## Guided product choice: the first production quarter, January to March 2027
Covers: title
Notes: G10 in the plan. Every number is from the plan's phase-2 evidence section, recorded 3 April 2027 and labelled invented for this trial.

---

## Live on every self-serve start for a quarter: completion 69.4% against 62%, cost $211 a month against $330 estimated, two incidents, no customer harm
Covers: summary
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (outcome, cost, incidents); baseline docs/discovery/smb-self-serve-ads.md §2; measured

- We measured: 69.4% of 2,310 starts reached creative upload, Q1 2027; baseline 62% (Q3 2026); refunds 2.9%
- We measured: $211 a month average; estimate was $330
- Two incidents, both served the fallback page; no wrong price, no wrong region

Notes: The bottom line: the guided product choice has run on every self-serve start for a quarter. Completion of the product-choice step was 69.4 percent of 2,310 starts, against the 62 percent baseline from the quarter before we started; refunds stayed at 2.9 percent. It cost 211 dollars a month on average against the 330 we estimated. There were two incidents, both of which showed the advertiser today's catalogue page instead of a recommendation; no one saw a wrong price or a wrong region. There is no big decision today; there is one small one at the end. Interrupt me whenever you like.

---

## Completion held at 68% to 70% in each of the three months, 7.4 points above the baseline on 2,310 starts
Covers: outcome
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (outcome row; G06/A2 query); baseline docs/discovery/smb-self-serve-ads.md §2; measured, counterfactual stated

- Chart: line by month, 68.1% (Jan, 740 starts), 69.9% (Feb, 731), 70.2% (Mar, 839); baseline 62% drawn flat; the pilot's control arm 63.1% marked
- Method: funnel export, all starts, read by the product owner; no control arm in production, so the comparison is the Q3 2026 baseline

Notes: The number and its method. The line is completion by month, 68.1, 69.9 and 70.2 percent, on 740, 731 and 839 starts; the flat line is the 62 percent baseline from the funnel export of the third quarter of 2026, measured the same way by the same product owner. One honest caveat: in production there is no control arm, so this is against last year's baseline, not against advertisers in the same weeks without the recommendation. The pilot's control arm in October measured 63.1 percent, which is the best evidence we have that the quarter did not simply get easier on its own.

---

## Adoption: 78% of starts typed a sentence and saw a recommendation; 44% of all starts picked a recommended product
Covers: adoption
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (adoption row; C5 log table); measured

- Offered on 100% of starts since 14 December 2026
- Active, defined as typed a sentence and saw at least one recommendation: 78%, 1,802 of 2,310
- Picked a recommended product: 44% of all starts, 1,016; the rest browsed or saw the fallback page

Notes: Adoption, with the definition on the slide because the word is slippery. Every start since 14 December has been offered the recommendation. We call a start active when the advertiser typed a sentence and saw at least one recommendation: that was 78 percent, 1,802 of 2,310. Forty-four percent of all starts went on to pick one of the recommended products; the others browsed as before or, in the two incidents, saw the fallback page. Both figures come from the log row written for every start.

---

## Cost: $211 a month on average against the $330 estimate, about $0.27 a start; 47 build hours against 30 to 60
Covers: cost
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (cost and people rows); estimate from production-approval-business.md slide 8; measured

- We measured: $198, $204, $231 by month (billing export); Cloud Run about $38 of each; about $0.27 a start live-only
- We estimated $330 a month and $0.46 a start in November; the estimate carried build-time spend, so it was high
- People: platform on-call 3 hours in the quarter; product owner and sales about 1 hour a week each (reported)

Notes: Second, the cost. The billing export says 198, 204 and 231 dollars for the three months, 211 on average, of which about 38 is hosting and the rest the model. The cost-per-start query puts it at about 27 cents a live start. We had estimated 330 a month and 46 cents a start in November; the estimate was high because it carried the build-time runs, which we said at the time. People: the platform team spent three hours on call across the quarter, and the product owner and the sales reviewer spend about an hour a week each, by their own report.

---

## Two incidents: a pricing outage and a quota hit; both showed the fallback page, one cost us a day at 58% completion
Covers: incidents
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (incidents table); measured

- 11 February, low: pricing service down 2 h 10 min; 63 starts saw "price on the next page"; no wrong price; no customer action
- 3 March, medium: a marketing campaign doubled starts; the model quota was hit; 142 starts saw the fallback page for 5 h 40 min; completion 58% that day; quota raised the same evening

Notes: Two incidents, both handled by controls we designed in, one of which we set too tight. On 11 February the pricing service was down for two hours; 63 advertisers saw a product with "price on the next page" instead of a price, which is the designed behaviour, and nobody saw a wrong number. On 3 March a marketing campaign doubled the day's starts and the model quota, set from pilot traffic, ran out at twenty past two; 142 advertisers saw the plain catalogue page for five and a half hours, and completion that day was 58 percent. The quota was raised the same evening and is now set from the forecast.

---

## What changed in the workflow: one sentence replaces browsing forty products, and sales reports escalations down from about 35 to about 22 a week
Covers: outcome
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (escalations, reported); docs/discovery/smb-self-serve-ads.md §4 workflow before and after; measured and reported kept apart

- Delivered: the advertiser types one sentence; a person still confirms every purchase; sales review flagged cases weekly
- Reported, not logged: escalations about 22 a week in March against about 35 in Q3 2026 (sales lead)
- Not delivered: a log of escalations; it stays a report until one exists

Notes: The workflow change is the one we proposed in October and it is now routine: the advertiser types a sentence instead of browsing forty products, and a person still confirms every purchase at booking. The sales lead reports escalations about product choice down from about 35 a week to about 22. I want to be clear about the voice there: that is reported, not measured, because escalations are still not logged; the number I can stand behind is the completion rate. The one real case on the spine: a bakery owner in March typed "weekend promotion, east of town", saw two local products, picked one and booked without calling anyone; that is one log row, labelled as an example.

---

## What we would do differently: set the quota from a forecast, log escalations from day one, keep a control arm for the first month
Covers: next
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (lessons recorded, open after the quarter); recorded lessons

- The quota from pilot traffic failed under a normal marketing event (3 March)
- Escalations were never logged, so the secondary benefit stays a report
- No control arm in production, so the quarter's lift is against last year's baseline, not concurrent

Notes: Three things we would do differently, each from the record. First, the quota: we set it from the pilot's traffic and a normal marketing day broke it; it is now set from the forecast. Second, escalations: we never built the log, so the number everyone likes most is the one I can least defend. Third, the control arm: we switched it off at go-live, so the quarter's lift is against last year's baseline; keeping ten percent of starts in control for the first month would have cost little and answered the question properly.

---

## The team: one developer, the product owner, the platform team and six sales staff
Covers: team
Evidence: docs/plans/smb-self-serve-ads.md phase 1 and 2 evidence (hours, people); docs/discovery/smb-self-serve-ads.md §6

- Developer: built the pilot in 58 hours and production in 47; the product owner labelled 30 and then 60 cases; the platform team hosts it and took three hours on call; sales review flagged cases weekly; sponsor: the Director of SMB Sales

Notes: Credit, before the ask. One developer built the pilot in 58 hours and took it to production in 47. The product owner labelled every evaluation case, thirty and then sixty, and reads the measure every week. The platform team hosts it, took the two incidents, and spent three hours on call in the quarter. The six sales staff review the flagged cases. The Director of SMB Sales sponsored it and pays the model bill from the self-serve budget line.

---

## Next: keep it as it is, or fund a two-week discovery for the next funnel step; we recommend the discovery; Director of SMB Sales, 14 April
Covers: next, ask
Evidence: docs/discovery/smb-self-serve-ads.md §3 portfolio (O2, O3); docs/architecture/smb-self-serve-ads.md §4 identity row; docs/plans/smb-self-serve-ads.md open after the quarter; options estimated

- A. Fund a two-week discovery for the next step (creative upload loses 12%, pricing 9%, from the Q3 2026 funnel): AI engineer's time only (recommended)
- B. Keep the service as it is: no new spend; add an escalation log and a one-month control arm when the next release ships
- C. Personalise per advertiser from account data: reopens the design's identity and data scope; not estimated
- Decider: the Director of SMB Sales, 14 April; nothing decided means B

Notes: Three options and a recommendation. A, fund a two-week discovery for the next funnel step; the October brief ranked creative upload and pricing next, losing 12 and 9 percent, and the discovery would cost my time, not the developer's. B, keep the service as it is, and add the escalation log and a short control arm with the next release. C, personalise recommendations from account data, which reopens the design's identity and data scope and has no estimate. We recommend A. The Director of SMB Sales decides today, 14 April; if nothing is decided, B happens by default and nothing is lost.

---

## Questions we expect, with the record's answer
Covers: questions, appendix
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence; docs/architecture/smb-self-serve-ads.md D3

- How many cases is this based on? 2,310 starts, 951 orders, Q1 2027; measured
- What if the model changes? `gemini-3.8-flash` pinned, no shutdown announced as of 31 March 2027 (D3); the release gate re-runs 60 cases
- Vanity count: 1,802 sentences typed in the quarter; not an outcome
- Who is accountable for a wrong recommendation? The confirming person at booking; the product owner for the weekly review; the platform on-call for outages

Notes: Appendix for the question period.
