# Design: guided product recommendation for SMB self-serve advertising

Status: **draft**, compact form (proof of concept meant to be kept). Source of the use case, baseline and stakeholders: `docs/discovery/smb-self-serve-ads.md` (the brief). Plan: `docs/plans/smb-self-serve-ads.md`. Working ADK assumption: `google-adk==2.8.0` (the specialists' compatibility pin); confirming the chosen pin is an acceptance item of G02.

## 1. Constraints and profile

| Scope-gate question | Answer (status) | What depends on it |
| --- | --- | --- |
| First useful version and what follows | Four-week proof of concept after the 29 Oct 2026 decision, live on 50% of starts from week two; production review two weeks after it ends (confirmed) | Phase 1 code is kept; phase 2 graduates it |
| Builder | One developer, new to ADK, has deployed to Cloud Run; about 30 focused hours a week (user said) | Multiplier 1.5 on every goal; capacity in the plan |
| Money | Under 500 EUR for models and cloud, capped by a project quota (user said); after the pilot, the sponsor's budget line (user said) | Flash-tier model, offline evaluation repeats limited |
| Users and judges | Advertisers in the self-serve flow; the product owner and the Director of SMB Sales judge completion from the funnel export (confirmed) | Measurement contract C5; arm logging |
| Data and effects | Reads catalogue, pricing and inventory; writes nothing; a person confirms every purchase (confirmed) | No effect contracts; floor only |
| Reviews needing a presentation | Approval 29 Oct 2026 (business); production decision review two weeks after the pilot (business and technical, the platform team hosts); results review after one quarter in production (business) (brief §6) | Presentation goals G01, G07, G08, G10 |
| Traffic slice | 50% of all starts, assigned by the platform (product owner agreed) | D4; the margin on the measure |

Profile: **proof of concept, kept**. Depth per concern and deferred controls are in §4.

## 2. Journey and shape

The advertiser, already signed in to the self-serve platform, reaches product choice and types one sentence ("weekend promotion for my bakery in the east of town"). The platform calls the recommendation service with the account id, the region and the sentence; code filters the catalogue to products that can run in that region and format, the model ranks one to three of them with a reason each, code attaches the price and availability from the existing services, and the advertiser picks one and continues to creative upload. Booking is unchanged: a person confirms every purchase.

The model decides only the ranking and the wording of the reason over a candidate list it did not build. Code controls the candidate list, the schema, the price and availability, the number of model calls and what is logged. Half of the starts get the recommendation (treatment arm); the other half see today's catalogue page; both are logged with the start id so the funnel export can be read per arm.

```text
platform (signed-in advertiser) --POST /recommend {account, region, sentence, start_id, arm}-->
  service (Cloud Run, platform project)
    code: catalogue read (platform API) -> filter(region, format) -> candidates (<= 40)
    LlmAgent(gemini-3.8-flash, output_schema Recommendation[1..3]) over candidates
    code: validate ids and reasons against candidates (C1, C3)
    code: pricing API + inventory API -> price, availability (C2)
    code: log request, candidates, output, build tag -> BigQuery (C5)
  <-- {recommendations[1..3] | fallback: "browse the catalogue" + sales link}
```

## 3. Contracts and decisions

Requirements: R1 fitting products only (brief §4 harm 1); R2 true price and availability (harm 2); R3 a reason per product (harm 3); R4 spend stays inside the allowance (floor); R5 the measure can be read per arm (brief §4 outcome measure).

| ID | Invariant and scope | Authority | Enforced where | Failure outcome | Check |
| --- | --- | --- | --- | --- | --- |
| C1 (R1) | Every recommended product id is in the code-built candidate list for the advertiser's region and format, for every request | Catalogue via platform API; account region from the platform | Code validator after the model, before the response | Offending id dropped; zero left: fallback to today's page plus a sales link | Planned, offline: G02/A2, G02/A3; live: zero out-of-region in G04 |
| C2 (R2) | Price and availability shown come from the pricing and inventory services; the output schema has no price field | Pricing and inventory APIs | Code enrichment step; the model never sees prices | Service down: product shown with "price on the next page", logged | Planned, offline: G03/A1, G03/A2 |
| C3 (R3) | Each recommendation carries a reason naming a catalogue attribute present on that product | Catalogue record | Schema plus code validator | Recommendation without a valid reason dropped | Planned, offline: G02/A4 |
| C4 (R4) | At most two model calls per start (one plus one repair), model id pinned, project quota caps monthly calls | RunConfig and the Gemini quota | `RunConfig.max_llm_calls=2` in the service; quota on the project | Cap hit: fallback to today's page; nothing retried | Planned: G02/A5 (config test), G05/A3 (quota set, live) |
| C5 (R5) | Every request logs start id, arm, candidates, output, chosen product and build tag; no account identifiers beyond the opaque account id | Platform start id | Code logging step; the funnel export joins on start id | Log write fails: response still served, failure counted and alerted weekly | Planned: G05/A2 (local), G06/A2 (live join) |

Floor kept: no writes to any platform system (the service holds read-only credentials); no secrets in source; model id pinned; spend stop (C4); a person confirms every purchase (unchanged platform step).

Decisions, in requirement, contract, choice, tradeoff, check order:

- **D1** (R1, R3; C1, C3): ordinary code plus one `LlmAgent` with `output_schema` and no tools; the candidate list is passed in the prompt. Tradeoff against an agent with a catalogue search tool: fewer failure modes and one call, at the cost of a prompt that grows with the catalogue (about 40 products, so fine). Check: G02.
- **D2** (hosting, identity): a stateless HTTP service on Cloud Run in the platform team's project, invoked only by the platform's service account (IAM invoker); account id and region arrive as trusted context, no end-user identity in the service. Tradeoff against Agent Runtime: the platform team already runs Cloud Run (user said), no session store is needed; against `adk web`: it cannot sit in the live flow. Check: G05/A1.
- **D3** (C4): `gemini-3.8-flash`, stable, no shutdown announced (lifecycle table checked 2026-10-08); low temperature; one repair attempt on invalid output. Tradeoff: a pro model might rank better; not measurable before G04, and the allowance is small. Check: G04.
- **D4** (R5; C5): 50% of all starts in the treatment arm, assigned by the platform from a stable hash of the start id. We estimate about 500 starts in three live weeks (2,140 a quarter, brief §2), so about 250 treated and a margin of about six points on the completion rate; one region would be unreadable. Check: G06/A2.
- **D5** (C5): logs go to a BigQuery table in the platform project, written by the service, read by a weekly review query; the platform database is never written. Tradeoff: one more component to delete at cleanup. Check: G05/A2.
- **D6** (acceptance): an offline set of 30 cases labelled with the product owner from the 1,327 completed-step records (brief §2); thresholds proposed, not agreed: zero out-of-region, the advertiser's actual product among the recommendations in at least 70% of cases. Check: G04.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise it |
| --- | --- | --- |
| Core judgment, measured | Build: 30 offline cases (G04), live arm measure (G06) | Production: evaluation set from the pilot's logs |
| Identity and data scope | Minimal: platform service identity only; opaque account id | Production: per-advertiser scope if the service ever reads account data |
| Secrets | Minimal: Secret Manager, read-only API credentials | Production: rotation |
| External writes | None (read only) | Any write proposal reopens the design |
| Sensitive data | Minimal: the free-text sentence is logged; no names or emails | Production: retention and SDP screening of the sentence |
| Budgets and loops | Minimal: C4 and the project quota | Production: per-month shared budget |
| Observability | Defer: Cloud Run logs and the C5 table | Production: traces, cost per start, alerts |
| Release | Minimal: pinned model and image tag; offline tests | Production: evaluation gate in CI, joint rollback |

Graduation conditions (phase 2): completion above 62% with refunds at or under 4% in the live window; evaluation set from live logs; observability; a release gate; the platform team's hosting sign-off.

## 5. Failure rows (read-only journey; no action rows)

| Integration | Unavailable or slow | Rejects or malformed | Rate limited | Untrusted content |
| --- | --- | --- | --- | --- |
| Catalogue (platform API) | Fallback page: G03/A2 | Same: G03/A2 | n/a: one read per start | n/a: platform-owned records |
| Pricing and inventory APIs | "Price on the next page": G03/A1, G03/A2 | Same: G03/A2 | n/a: two reads per start | n/a: platform-owned |
| Gemini | Fallback page after deadline: G02/A5 | Invalid output: one repair, then fallback: G02/A3 | Quota hit: fallback: G05/A3 | Injected text in the sentence cannot act: no tools, no writes: G02/A2 |
| BigQuery log | Served, counted: G05/A2 | Same: G05/A2 | n/a: one row per start | n/a: service-written |

Write outcome unknown, partial change, duplicates: n/a: the service writes only its own log row.

## 6. Plan, open decisions and next prompt

Goals, estimates, capacity and the cut line are in `docs/plans/smb-self-serve-ads.md`. Open decisions: D6 thresholds (product owner agrees at G04); retention of the logged sentence (platform team, before G05); the exact ADK pin (G02). Next prompt:

```text
/adk-presenter Carry out G01 from docs/plans/smb-self-serve-ads.md: the proof-of-concept approval presentation for a business audience from the brief, this design and the plan, for the Director of SMB Sales on 29 October 2026.
```
