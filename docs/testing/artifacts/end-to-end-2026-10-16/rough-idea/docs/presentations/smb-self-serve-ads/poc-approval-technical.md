---
stage: poc-approval
audience: technical
minutes: 30
title: Guided product recommendation service: what the platform team hosts and what we need from you
sources: docs/architecture/smb-self-serve-ads.md, docs/plans/smb-self-serve-ads.md, docs/tickets/smb-self-serve-ads/G02.md, docs/discovery/smb-self-serve-ads.md
decision: Grant platform project access, read-only catalogue credentials and a week-two integration slot for a four-week proof of concept on Cloud Run
decider: Platform team lead (hosting); Director of SMB Sales decides the proof of concept on 29 Oct 2026
date: 2026-10-29
---

## Guided product recommendation service: what the platform team hosts and what we need from you
Covers: title
Notes: Technical version of G01; the business decision is taken the same day.

---

## One stateless Cloud Run service in your project: code filters, one model call ranks, your services price; the pilot tests a lift from 62%
Covers: summary
Evidence: docs/architecture/smb-self-serve-ads.md §2, D1, D2; docs/discovery/smb-self-serve-ads.md §4 baseline measured

- Request: account id, region, sentence, start id, arm; response: one to three product ids with reasons, price and availability attached by code
- One `LlmAgent` with an output schema and no tools; `gemini-3.8-flash` pinned; at most two calls per start
- Hypothesis under test: completion of product choice above 62% (funnel export, Q3 2026) on half of starts

Notes: The summary first. We want to run one stateless HTTP service in your project on Cloud Run. Your platform calls it with the account id, the region, the advertiser's sentence, the start id and the arm; it filters the catalogue in code, makes one model call to rank up to three candidates, attaches price and availability from your pricing and inventory services, and returns. The pilot tests whether that lifts product-choice completion above 62 percent on half of the starts. The rest of this deck is the design by path, what we ask of you, and what you get back if it stops.

---

## The service reads the catalogue, pricing and inventory, writes nothing, and holds no end-user identity
Covers: scope
Evidence: docs/architecture/smb-self-serve-ads.md §1 (data and effects, confirmed), D2, §4 depth table

- In scope: one request per start; read-only credentials; the opaque account id and region as trusted context from your service identity
- Out of scope: writes of any kind, end-user sign-in, sessions, memory, creative, pricing, booking
- Kept at every depth: no secrets in source, pinned model, spend stop, a person confirms every purchase

Notes: The boundary is narrow. The service reads three of your APIs with read-only credentials and writes only its own log row. It holds no end-user identity: your platform has already signed the advertiser in and passes the opaque account id and region under its own service identity. No sessions, no memory, no tools. The floor holds at every depth: no secrets in source, a pinned model, a spend stop, and the human confirmation at booking stays where it is.

---

## Architecture: platform to Cloud Run service to catalogue, model, pricing and inventory, with a log row per start
Covers: architecture
Evidence: docs/architecture/smb-self-serve-ads.md §2 diagram, D1, D2, D5

- Platform (signed-in advertiser) → `POST /recommend` on Cloud Run, IAM invoker limited to the platform's service account
- Code: catalogue read → filter(region, format) → candidates (at most about 40) → model ranks → validators → pricing and inventory enrichment
- Code: one row per start to a BigQuery table in your project (start id, arm, candidates, output, build tag)

Notes: Here is the path, from the design's diagram. Your platform calls the service; only your service account may invoke it. Code reads the catalogue, filters to the region and format, and hands at most about forty candidates to the model in the prompt; the model returns up to three ids with reasons, the validators check every id and reason against the candidate list, and code attaches price and availability. One log row per start goes to a BigQuery table in your project so the funnel export can be joined on start id. The trust boundary is the validator: nothing from the model reaches the advertiser unchecked.

---

## Five contracts the proof of concept must keep, each with an enforcement point in code
Covers: contracts
Evidence: docs/architecture/smb-self-serve-ads.md §3 contracts table C1 to C5

- C1 every recommended id is in the code-built candidate list for the region; validator after the model
- C2 price and availability come from your services; the schema has no price field
- C3 each reason names a catalogue attribute on that product; schema plus validator
- C4 at most two model calls per start, model pinned, project quota caps the month
- C5 every request logs start id, arm, candidates, output, build tag; no account identifiers beyond the opaque id

Notes: Five contracts, stated once in the design's table and cited by the goals. C1 and C3 are enforced by a validator that runs after the model and before the response. C2 is structural: the output schema has no price field, so the model cannot state one. C4 is the spend stop, a RunConfig limit of two calls and a quota on the project. C5 is the measurement contract; if its log write fails the response is still served and the failure is counted. The invariants are in the table; I will not restate them.

---

## Data and access: three read-only APIs through your service identity, a BigQuery table, a Gemini quota; access requested on 2 November
Covers: dependencies
Evidence: docs/architecture/smb-self-serve-ads.md §1 data register (brief §4), D2, D5; docs/plans/smb-self-serve-ads.md W2, W3

- Catalogue via the platform API (read-only, confirmed), pricing and inventory APIs (existing), owner: platform team
- Project access and read-only credentials in Secret Manager: wait W2, three working days from 2 Nov
- Integration slot for the 50% arm in week two: wait W3, by 9 Nov

Notes: The data path is yours end to end. The catalogue is read through the platform API, which you confirmed this week; pricing and inventory are the existing services. We need two things on a calendar: project access and read-only credentials in Secret Manager within three working days of the second of November, and a slot in week two to switch half of the starts to the service. Both are waits in the plan, requested on day one, so the build is not idle while they clear.

---

## Evaluation plan: 30 labelled cases offline before go-live, then the live arm measure; thresholds proposed, not agreed
Covers: evidence-plan
Evidence: docs/plans/smb-self-serve-ads.md G04, G06; docs/tickets/smb-self-serve-ads/G04.md; docs/architecture/smb-self-serve-ads.md D6

- G04: 30 cases from the 1,327 completed-step records, labelled with the product owner; zero out-of-region (C1); actual product among the recommendations in at least 70% (proposed)
- G02 and G03: offline tests with a stubbed model and stubbed services for C1 to C4, including an injected instruction in the sentence
- G06: live completion per arm from the funnel export joined on start id, fewer than 2% unmatched

Notes: Evidence comes in three layers. Offline deterministic tests in G02 and G03 cover the validators, the repair path, the fallbacks and an injected instruction in the sentence. G04 runs the service on 30 labelled cases before anything goes live; the two thresholds there are proposed and the product owner agrees or revises them in that goal. G06 is the live measure, completion per arm from your funnel export. No case has run yet; every number in the December review will name its goal.

---

## The baseline is 62% from the Q3 funnel export; the pilot reads the same export per arm on about 250 treated starts
Covers: success-criteria, problem
Evidence: docs/discovery/smb-self-serve-ads.md §4 (measured baseline); docs/architecture/smb-self-serve-ads.md D4 (sample estimated)

- Method: share of starts that reach creative upload, per arm, joined on start id; owner: platform product owner
- We estimate about 500 starts in three live weeks, half treated, margin about six points
- Counter-metric: refund rate, 3% of orders today; switch-off above 4%

Notes: The baseline is already measured, 62 percent of 2,140 starts in Q3, by the product owner from the funnel export. The pilot reads the same export per arm, which is why the log row carries the start id. We estimate about 250 treated starts in three live weeks, a margin of about six points; a smaller lift is reported as within the margin. The refund rate is the guardrail, three percent today, switch-off above four.

---

## Security and data boundaries: no writes, no tools, no end-user identity; the free-text sentence is the only personal data and its retention is open
Covers: risks
Evidence: docs/architecture/smb-self-serve-ads.md §4 depth table, §5 failure rows, §6 open decisions

- Injected text in the sentence cannot act: the agent has no tools and the service no write credentials (G02/A2)
- The logged sentence may hold personal data: retention to be set by the platform team before G05; SDP screening deferred with that trigger
- Deferred, each with a trigger: per-advertiser scope, traces, release gate, rotation

Notes: The security story is structural. The model has no tools and the service holds no write credentials, so an instruction hidden in the sentence has nothing to act on; a test asserts the absence of any call. The one piece of personal data is the sentence itself, which we log for the review loop; its retention is an open decision for your team before the deployment goal, and screening is deferred with that trigger. Everything else deferred is in the depth table with the trigger that brings it forward.

---

## Cost model: about 700 starts a month, at most two model calls each, under a 500 EUR quota; per-start cost measured in G04, not yet estimated
Covers: cost
Evidence: docs/architecture/smb-self-serve-ads.md §1 (allowance, user said), C4; docs/discovery/smb-self-serve-ads.md §4 unit economics (volume); G04 measures

- We estimate volume: 2,140 starts a quarter, about 700 a month, half treated in the pilot
- Bound: `max_llm_calls=2` per start and a project quota; Cloud Run scales to zero between requests
- Not yet estimated: tokens per start and price; G04 records the cost of 30 cases × at most 2 calls

Notes: The cost model is a bound and a measurement, not a forecast. Volume is about 700 starts a month from the quarterly figure, half of them treated during the pilot. Each start makes at most two model calls and the project quota caps the month under the 500 euro allowance. Tokens per start and the resulting price are not yet estimated; the evaluation goal records what 30 cases cost, and that figure goes into the December review.

---

## What we ask of your team: project access in three days, one integration slot, about four review hours over four weeks
Covers: dependencies
Evidence: docs/plans/smb-self-serve-ads.md W2, W3, G05, G06 (hours estimated); assumption: review hours

- W2: project, Cloud Run, Secret Manager, BigQuery dataset, read-only API credentials, by 5 Nov
- W3: the 50% routing change in the platform, week of 9 Nov
- We estimate about four hours of your review across G05 and G06 (assumption, not in the plan's hours); retention decision for the logged sentence

Notes: Concretely, we ask for three things. Project access with Cloud Run, Secret Manager, a BigQuery dataset and read-only credentials by the fifth of November. The routing change that sends half of the starts to the service, in the week of the ninth. And roughly four hours of your review across the deployment and integration goals, which is my assumption and not yet in the plan, plus a decision on how long we keep the logged sentence.

---

## If it stops in December you keep the service code, the 30-case evaluation set, the log table and the findings
Covers: hypothesis
Evidence: docs/plans/smb-self-serve-ads.md G02 to G06 deliverables, G07, G08

- Kept: the service with its tests, the evaluation set and runner, the log table and weekly query, the design and contracts
- Deleted at cleanup: the Cloud Run service, the secrets, the quota; the dataset after retention
- The December review names every deviation from the design and every case not run

Notes: If the production decision is no, nothing is wasted on your side: the code and its tests, the evaluation set, the log table and the design stay, and the service, secrets and quota are removed at cleanup. The December review lists every deviation from the design and every acceptance case that did not run, so what you inherit is written down.

---

## Decision: we need project access by 5 November and the integration slot in the week of 9 November; owner: platform team lead
Covers: ask
Evidence: docs/plans/smb-self-serve-ads.md W2, W3, W4

- A. Grant access and the slot as planned (recommended): live from 9 Nov, production decision review 11 Dec
- B. Grant access, integration slot in week three: one live week less, margin widens past six points
- C. Decline hosting the pilot: the proof of concept cannot run on live traffic; back to the design
- Decider on hosting: platform team lead, by 29 Oct, alongside leadership's decision

Notes: Three options for you. Grant the access and the week-two slot as planned, and the service is live on the ninth with the review on the eleventh of December; that is our recommendation. Grant access but give us the slot a week later, which costs a live week and widens the margin. Or decline to host the pilot, in which case it cannot run on live traffic and we go back to the design. We need your answer by the twenty-ninth, alongside leadership's.

---

## Questions we expect, with the record's answer
Covers: questions
Evidence: docs/architecture/smb-self-serve-ads.md §3, §4, §5, §6; docs/plans/smb-self-serve-ads.md; "not measured" where silent

- Worst failure modes and runs: out-of-region id, invalid output, injected sentence; G02/A2, A3; not yet run
- Demo versus numbers: no demo today; the December demo will be a recording of the build the numbers cover
- Tool contracts: none; the model has no tools; the API contract is `POST /recommend` (design §2)
- Identity and writes: platform service account as invoker; no writes (D2)
- p95 latency and tokens per turn: not measured; G04 records both on 30 cases
- Runaway loop or injection: `max_llm_calls=2`; no tools, no write credentials (C4, G02/A2)
- Rollback: pinned model and image tag; the arm switch-off needs no deploy (G06/A3)
- On-call: none in the pilot; Cloud Run logs only; alerts deferred to G09
- Model version and retirement: `gemini-3.8-flash`, stable, no shutdown announced, lifecycle table checked 2026-10-08 (D3)
- Sensitive-data tests: the sentence is the only personal data; retention open; screening deferred

Notes: Appendix; not spoken unless asked.
