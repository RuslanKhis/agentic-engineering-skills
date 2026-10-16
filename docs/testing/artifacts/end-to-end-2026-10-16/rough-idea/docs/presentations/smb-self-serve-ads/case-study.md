# Case study draft: Northlight Media lifts self-serve product-choice completion from 62% to 69% with a guided product recommendation, Built on Google Cloud

Status: internal draft; not yet sent. The submission pack below is an ask to the Google Cloud account team (Jonas Weber, invented) to route to customer reference marketing and the Cloud Brand team; it is not a submission. Every company fact, name and figure in this draft is invented for this trial and labelled so in the plan.
Attribution phrase: "Built on Google Cloud" (Google Cloud products used, no implementation guidance from Google); Gemini and the Google Cloud Agent Development Kit (ADK) are named in plain text. The design calls the system a service with one bounded model judgement, so this draft says "service", not "agent".
Sources: docs/plans/smb-self-serve-ads.md (phase 1 and phase 2 evidence), docs/architecture/smb-self-serve-ads.md, docs/discovery/smb-self-serve-ads.md

Every number cites its evidence line; every quote carries its approval status; every sentence naming a Google product uses plain text or the attribution phrase. Unapproved sentences are marked `[draft]`.

**Subtitle:** Small businesses buying advertising on Northlight Media's self-serve platform left most often at product choice; a one-sentence description now returns one to three fitting products with reasons, and more of them reach the next step.

## Results

| Result | Before | After | Window | Sample | Method | Evidence | Publishable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Product-choice completion (starts reaching creative upload) | 62% (Q3 2026) | 69.4% | 1 Jan to 31 Mar 2027 | 2,310 starts | funnel export, all starts, read by the product owner; no concurrent control arm | plan phase 2 evidence, outcome row (G06/A2 query) | as is |
| Same measure in the pilot, against a concurrent control | 63.1% (control, 298 sessions) | 70.8% (treatment) | 10 to 23 Oct 2026 | 312 treated sessions | funnel export joined per arm on start id | plan phase 1 evidence, G06/A2 | as is |
| Refund rate (guardrail) | 3% | 2.9% | Q1 2027 | 951 orders | order system | plan phase 2 evidence, counter-metric row | as is |
| Model and cloud cost | estimate $330 a month | $211 a month average | Q1 2027 | 3 months of billing | billing export; cost-per-start query | plan phase 2 evidence, cost row | range: "about $200 to $250 a month" |
| Advertisers who typed a sentence and saw a recommendation | n/a | 78% of starts | Q1 2027 | 2,310 starts | log table joined on start id (C5) | plan phase 2 evidence, adoption row | as is |

The public version shows the completion rows, the refund row and the adoption row; cost appears as the range.

## About Northlight Media

Northlight Media is a regional media group in Rotterdam with about 900 staff (invented). It sells display, audio and local video advertising to small businesses through a self-serve platform, with a person confirming every purchase before it is booked (brief §1).

## The challenge

In the third quarter of 2026, 2,140 small-business advertisers started a self-serve purchase on the platform and 38% of them left at product choice, more than the next three steps together: creative upload lost 12%, pricing 9% and booking 6% (funnel export, Q3 2026; brief §2). The step offered about 40 products across formats and regions with no way to tell which one fitted a local promotion; advertisers opened a chat with sales, who handled about 35 such escalations a week, or left (brief §2, reported).

Leadership had asked for "AI so that small businesses can buy advertising from us more easily" without saying where (brief §1). A one-day discovery with the platform product owner put the drop where the funnel said it was, chose product choice as the first use case because the data was at hand and a person already confirmed every purchase, and set the measure, the baseline and the guardrail before anything was built: completion of the product-choice step against 62%, with refunds at 3% as the stop rule (brief §4). Earlier attempts had not been made; the catalogue had simply grown.

## The solution

In the advertiser's words: type one sentence about the promotion, see one to three products that can run where you are, each with a reason, pick one, and go on to upload your creative; a person still confirms the purchase at booking (design §2).

The service is a stateless HTTP service on Cloud Run in the platform team's own project, invoked only by the platform's service account (design D2). Code reads the product catalogue through the platform's API and filters it to products that can run in the advertiser's region and format; one `LlmAgent` built with the Google Cloud Agent Development Kit (ADK), using a pinned Gemini model with a fixed output schema and no tools, ranks one to three of those candidates and writes a reason for each; code then validates every product id and reason against the candidate list, attaches price and availability from the existing pricing and inventory services, and logs the request, the candidates, the output and the build tag to a BigQuery table (design §2, contracts C1 to C5). The model never sees a price and cannot write to any platform system; at most two model calls are made per start and a project quota caps monthly spend (design C2, C4). Human approval points: the advertiser chooses, a person confirms every purchase, and sales staff review flagged recommendations weekly with the product owner (brief §4).

Evaluation: an offline set of 30 cases labelled with the product owner, with thresholds agreed before the run (zero out-of-region recommendations; the advertiser's actual product among the recommendations in at least 70% of cases), then a four-week proof of concept on half of live starts with the other half as a control arm (design D4, D6). In production the set was refreshed to 60 cases from the service's own logs and runs as a release gate in CI; it blocked one release (plan phase 2 evidence, evaluation gate row).

Architecture diagram: `[to be drawn from design §2; reviewed for secrets, internal hostnames and customer data before it leaves the repository; security review pending]`

## What changed

Over the first production quarter, 69.4% of 2,310 purchase starts reached creative upload against the 62% baseline of the quarter before the project began, measured the same way by the same product owner; by month it was 68.1%, 69.9% and 70.2% (plan phase 2 evidence). There was no control arm in production, so the quarter's figure is against last year's baseline; in the October pilot, with a concurrent control, 70.8% of 312 treated sessions reached the next step against 63.1% of 298 control sessions, a lift above the margin from chance alone on that sample, with no formal significance test run (plan phase 1 evidence, G06/A2). Refunds stayed at 2.9% of orders (plan phase 2 evidence). In the quarter, 78% of starts typed a sentence and saw a recommendation, and 44% of all starts picked one of the recommended products (plan phase 2 evidence, adoption row).

The service cost about $211 a month on average in model and cloud spend against an estimate of $330, about $0.27 a live start (plan phase 2 evidence, cost row; published as a range). It was built by one developer new to ADK in 58 hours for the pilot and 47 for production, with the product owner labelling every evaluation case (plan phase 1 and 2 evidence).

What did not improve or is still being measured: escalations to sales are reported by the sales lead as down from about 35 to about 22 a week but are not logged, so that figure is a report, not a measurement (plan phase 2 evidence, escalations row); the evaluation set runs once per release, so there is no variance figure; two incidents occurred, a two-hour pricing-service outage absorbed by the designed fallback and a day on which a marketing campaign exhausted a model quota sized from pilot traffic, leaving 142 advertisers with the plain catalogue page for five and a half hours and that day's completion at 58% (plan phase 2 evidence, incidents table).

> "Our advertisers used to face forty products and a chat window. Now they tell us what they want to promote and see two or three that fit, and more of them get to the next step." — Director of SMB Sales, Northlight Media. Approval: draft, not approved. `[draft]`

## What's next

The plan holds a two-week discovery for the next funnel step (creative upload and pricing, which lost 12% and 9% of starts in Q3 2026) and, on the next release, a one-month 10% control arm and an escalation log so the secondary benefit can be measured (plan, decision memo of 14 April 2027; options, not yet decided). Per-advertiser personalisation is not planned; it would reopen the design's identity and data scope (design §4). Nothing here is promised beyond what the plan holds.

---

Industry: Media and advertising · Location: Rotterdam, Netherlands (invented) · Products: Google Cloud Agent Development Kit (ADK), Gemini, Vertex AI, Cloud Run, BigQuery

## Submission pack (not published)

| Item | Status | Owner | Date |
| --- | --- | --- | --- |
| Relationship and Google contact | online agreement, no Partner Advantage tier, no startup programme; account manager Jonas Weber (invented) | AI engineer | recorded 14 Apr 2027 |
| Executive sponsor approval | approved by the Director of SMB Sales (invented) | Director of SMB Sales | 10 Apr 2027 |
| Legal review | not yet reviewed | legal (name to be confirmed) | requested 15 Apr 2027 |
| Communications review | not yet reviewed; company name and location to be confirmed for publication | communications (name to be confirmed) | requested 15 Apr 2027 |
| Security review of diagram and data flows | pending; diagram not yet drawn | platform team lead | before sending |
| Numbers: publishable status per row | completion, pilot, refunds, adoption as is; cost as a range; all cite the plan's evidence lines | product owner (numbers), AI engineer (citations) | 14 Apr 2027 |
| Quotes: written approval | one quote drafted, not approved; media clearance not requested | Director of SMB Sales | before sending |
| Attribution language chosen; wording lint passed | "Built on Google Cloud"; `check_deck.py --prose` on this file: see `checks/stage7-case-study-prose.txt` | AI engineer | 14 Apr 2027 |
| Open asks for Google (logo, announcement, story, Next session, Marketplace) | requires Google consent: story production by customer reference marketing; logo use; a joint announcement; no Next session or Marketplace interest (the service is not a product) | Jonas Weber (Google), AI engineer | when sent |
| Timeline: start, launch, measurement window, publication target | discovery 15 Oct 2026; pilot 10 to 23 Oct 2026; production 14 Dec 2026; measurement window Q1 2027; publication target to be set with Google | AI engineer | 14 Apr 2027 |
| Derived assets wanted: one-pager by default; talk proposal, blog draft, sanitised sample (CLA) on request | one-page leave-behind: the subtitle, the Results table's publishable rows, the solution paragraph in the advertiser's words, the attribution line; a meeting deck `case-study-public.md` for the account team; no talk, blog or sample requested | AI engineer | 14 Apr 2027 |
| Contacts: spokesperson, technical lead, marketing owner, Google contact, where the pack was sent | spokesperson: Director of SMB Sales; technical lead: the developer; marketing owner: to be named by communications; Google contact: Jonas Weber; not yet sent | AI engineer | before sending |

Interview questions for the sponsor (30 to 60 minutes, sent in advance), generated from the gaps above: why product choice mattered more than revenue reporting suggested; what the six sales staff do with the hour a week they no longer spend on product-choice escalations; what the confirming person noticed about the recommendations; what you would tell a peer about keeping a control arm; which company facts may be published.
