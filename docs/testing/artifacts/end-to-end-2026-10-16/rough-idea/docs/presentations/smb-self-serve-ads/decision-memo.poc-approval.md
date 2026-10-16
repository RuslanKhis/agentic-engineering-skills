# Decision memo: guided product choice for small advertisers, proof-of-concept approval

One page, sent before the meeting of 29 October 2026 as the pre-read and after it as the record. Everything here is in the deck's evidence (`poc-approval-business.md`); nothing new appears in a memo. Redrafted from the brief, the design (`docs/architecture/smb-self-serve-ads.md`) and the plan (`docs/plans/smb-self-serve-ads.md`, G01); the brief-only draft is `poc-approval-business.brief-only.md`.

**Decision requested:** approve a four-week, one-developer proof of concept of a guided product recommendation in the self-serve purchase flow, on live traffic from week two.
**Deadline for the decision:** 29 October 2026; the developer's booking and the four-week window wait on it.
**Owner:** the AI engineer, for the Director of SMB Sales (sponsor).

## What we found

Product choice is the largest drop in the self-serve funnel: of 2,140 purchase starts in Q3 2026, 38% left at that step, against 12% at creative upload, 9% at pricing and 6% at booking (funnel export, Q3 2026, brief §2). Advertisers face about 40 products across formats and regions with no way to tell which fits; sales absorbs about 35 escalations a week (reported, brief §2). We hypothesise that a one-sentence description turned into one to three fitting products with reasons lifts completion above 62% without raising refunds from 3% (brief §4). The plan fits: phase 1 developer goals G02 to G06 need 31.5 to 57 of 72 available hours (plan summary); the pilot runs on 50% of all starts, about 250 treated in three live weeks, margin about six points (design D4, estimated); catalogue access and the caller identity are confirmed by the platform team; the sponsor's budget line pays after the pilot. Not yet estimated: model and cloud cost per start and per month (allowance under 500 EUR, capped; G04 measures 30 cases). Not yet agreed: D6's evaluation thresholds.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Run the proof of concept | One developer, four weeks, live traffic from week two, measured report against 62% | 31.5 to 57 developer hours plus 13.5 to 27 presentation hours (plan, estimated); money under a 500 EUR quota, per start not yet estimated | Out-of-region or wrong-price recommendation; both controlled by code and the existing services | Recommended because the step with the most people behind it has its data at hand and a person already confirms every purchase |
| B. Wider pilot (all starts, all regions) | Same build, full traffic | Same hours; about twice the model calls; no estimate | No hosting sign-off; no cost model yet | |
| C. Do nothing | Keep the funnel as it is | None | Product choice keeps losing 38%; 35 escalations a week continue | |

## If approved

- **Scope:** a guided product recommendation only; reads catalogue, pricing and inventory; no writes; no creative, pricing or booking automation; a person confirms every purchase. Built by one developer, 2 to 27 November 2026 (invented dates), live from 9 November; the cut line is below all of phase 1, G04 shrinks to 15 cases first if the work runs high.
- **Success criteria for the next review:** product-choice completion above 62% in the proof-of-concept window, from the funnel export, read by the product owner; refunds at or below 4% of orders (brief §4 threshold sentences; the offline thresholds in D6 are proposed, not yet agreed).
- **Kill criteria:** completion does not rise above 62% in the window; or refunds above 4%, which switches the recommendation off.
- **Next review:** production decision review, leadership and the platform team, 11 December 2026 (W4, invented date, two weeks after the pilot ends); results review after one quarter in production (G10).

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |
| Option A approved: run the proof of concept (invented, recorded at stage 5) | Director of SMB Sales | 2 Oct 2026 (early; invented) | Live on 50% of starts; refunds above 4% switch it off; production review two weeks after the pilot ends |

Open questions raised, with who answers each and by when: retention of the logged sentence (platform team, before G05); D6 thresholds (product owner, in G04); the ADK pin (developer, in G02).
