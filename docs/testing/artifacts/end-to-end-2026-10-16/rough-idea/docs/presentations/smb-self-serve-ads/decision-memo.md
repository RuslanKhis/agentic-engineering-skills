# Decision memo: guided product choice, results after the first production quarter

One page, sent before the meeting of 14 April 2027 as the pre-read and after it as the record. Everything here is in the decks' evidence (`final-results-business.md`, `final-results-technical.md`); nothing new appears in a memo. Earlier memos: `decision-memo.poc-approval.md`, `decision-memo.production-approval.md`. All figures are from the plan's phase-2 evidence section, invented for this trial and labelled so.

**Decision requested:** information on the quarter; one decision: fund a two-week discovery for the next funnel step (business), and keep a 10% control arm for one month with an escalation log on the next release (technical).
**Deadline for the decision:** 14 April 2027; the next release and the discovery sprint wait on it; nothing decided means the service runs on as it is.
**Owner:** the AI engineer, for the Director of SMB Sales (sponsor).

## What we found

Product-choice completion was 69.4% over Q1 2027, 1,603 of 2,310 starts, against the 62% baseline of Q3 2026 (funnel export, read by the product owner; plan phase 2 evidence), steady by month at 68.1%, 69.9% and 70.2%; there is no control arm in production, so the comparison is against last year's baseline and the pilot's October control arm (63.1%). Refunds 2.9% of orders, 28 of 951. Adoption: 78% of starts typed a sentence and saw a recommendation; 44% picked one. Cost $211 a month on average against the $330 estimate, about $0.27 a live start. Two incidents: a pricing outage absorbed by the designed fallback (11 Feb, low) and a quota exhausted by a marketing day (3 Mar, medium; 142 starts, completion 58% that day; quota now set from the forecast). The CI gate blocked one release (17 Feb). Not measured: escalations (reported down from about 35 to about 22 a week); tokens per request not summarised; variance of the evaluation set.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Discovery for the next step; next release honours the arm field, 10% control for a month, escalation log | Two-week discovery (AI engineer); 8 to 12 developer hours (estimate) | No new model spend; 10% of starts lose the recommendation for a month | A month of lower completion on 10% of starts | Recommended because the quarter's result is against last year's baseline and the second benefit is unlogged |
| B. Keep the service as it is | No release beyond maintenance | None | The two gaps stay | |
| C. Personalise per advertiser from account data | Reopens the design's identity and data scope | Not estimated | New data boundary; no measure yet | |

## If approved

- **Scope:** discovery sprint on creative upload (12%) and pricing (9%) from the Q3 2026 funnel; next release: `arm` honoured, 10% control, escalation log; owners: AI engineer, developer, product owner.
- **Success criteria for the next review:** completion in the treatment arm above the control arm over the month, on all starts; escalations per week measured from the log (proposed, not yet agreed).
- **Kill criteria:** unchanged: refunds above 4% switch the recommendation off.
- **Next review:** results review after the control month, product owner and platform team; a case study if results are approved for sharing (G11).

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |

Open questions raised, with who answers each and by when: SDP screening trigger (platform team, on the first finding of personal data); tokens per request summary (developer, next quarterly report).
