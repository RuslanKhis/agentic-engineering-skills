# Decision memo: Order intake after a quarter in production

One page, sent before the 6 May 2027 results review as the pre-read and after it as the record. Everything here is in the deck's evidence (docs/plans/order-intake.md G08 and G09, invented and labelled; G02 baseline). Earlier memos: decision-memo.poc-approval.md (5 Nov 2026), decision-memo.production-approval.md (10 Dec 2026).

**Decision requested:** none on the system itself; one ask: approve a public case study and a four-week discovery on phone orders (plan Later list).
**Deadline for the decision:** 6 May 2027; nothing waits on it except the case study and the discovery start.
**Owner:** operations director.

## What we found

Over 25 January to 25 April 2027 on all four queues, dispatcher time per emailed order was a median 1.6 minutes on 8,640 orders (weekly medians 1.3 to 2.4; mailbox and TMS timestamps; G09) against the 4.4 measured on the pilot queue in November (G02; the other three queues were never shadow-measured). Corrected orders were 2.9% against 2.8%; wrong-place deliveries 11 in the quarter (0.13%). Cost averaged USD 221 a month over three bills against the USD 230 estimate, USD 0.077 per emailed order. All four dispatchers were active every week; 94% of emailed orders went through the approval screen. Two medium incidents (expired mailbox consent, 3 h 40 min; TMS outage, 2 h 10 min) were contained by the alert and the pending state; 41 orders were typed by hand and none lost. Not measured: complaints by queue; whether freed dispatcher hours (we estimate about 400 in the quarter) were reassigned.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Keep running; publish a case study; run discovery on phone orders (recommended) | The system is unchanged; the story is told with the IT firm's and Google's consent; four weeks of discovery on the 27% of orders by phone | About 8 hours of the operations director's time plus 3 to 4 for the study (estimate); no build | Low; the case study needs the IT firm's and the customers' names kept out | Recommended because the phone-order trigger set in October has been met and discovery costs no build |
| B. Keep running; no case study; no new work | Nothing changes | None | None | |
| C. Build phone-order intake without discovery | A second build on an unmeasured process | Unknown | High: no baseline, no measure | |

## If approved

- **Scope:** case study per the adk-presenter case-study template, sent to the Google Cloud account team through the IT firm; discovery on phone orders with the adk-discovery skill.
- **Success criteria for the next review:** phone-order discovery produces a measured baseline and a first use case or a reason not to build (proposed).
- **Kill criteria:** for the running system, unchanged: corrected orders above 2.8% on a queue pauses it.
- **Next review:** after the discovery, about June 2027, business audience.

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |

Open questions raised, with who answers each and by when: reassignment of freed dispatcher hours (operations director, by the next review); the other three queues' baselines, if the CEO wants them (not recoverable; stated as an assumption).
