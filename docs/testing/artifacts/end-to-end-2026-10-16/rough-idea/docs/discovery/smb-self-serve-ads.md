# Discovery brief: SMB self-serve advertising

Status: draft / reviewed with the AI engineer on 15 October 2026
Entry: rough area ("Leadership wants AI so small businesses can buy advertising from us more easily, but nobody has said where")
Next step: `adk-system-designer` with the first use case below

Everything below is either what the user said, what a cited source says, or a labelled assumption. Numbers carry their source and date.

## 1. Business and the outcome that matters

- **The problem in the sponsor's words:** "AI so that small businesses can buy advertising from us more easily" (leadership, relayed by the AI engineer, 15 Oct 2026).
- **The problem in the builder's words:** advertisers who start a self-serve purchase leave before booking, most of them at product choice; difference noted: leadership says "easier", the funnel says "where". Frontline user who agrees: the product owner of the self-serve platform (user said).
- **What the business sells and to whom:** advertising inventory (display, audio, local video slots; user said) sold direct to small businesses through a self-serve platform.
- **KPIs leadership watches:** self-serve ad revenue (the sponsor's KPI; current value not given: unknown); refunds at 3% of orders (user said, Q3 2026).
- **Processes that move those KPIs:** the self-serve purchase funnel (platform product owner; 2,140 starts in Q3 2026, funnel export); sales escalations (six sales staff; about 35 a week, user said).
- **Who decides what, and when:** leadership decides on a four-week, one-developer proof of concept on 29 Oct 2026; production decision review two weeks after the proof of concept ends.

## 2. The journey and where it breaks

| Step | Who does it today | Volume (Q3 2026) | Where it fails or stalls | Evidence (source, date) |
| --- | --- | --- | --- | --- |
| Sign up and start a purchase | Advertiser | 2,140 starts | n/a | Funnel export, Q3 2026 (measured) |
| Choose a product | Advertiser, sometimes a sales chat | 2,140 enter; 38% leave (about 813) | About 40 products across formats and regions; advertiser cannot tell which fits (assumed typical case) | Funnel export (measured); product owner agrees (reported) |
| Upload creative, rights check | Advertiser; rights metadata in the creative library | About 1,327 enter; 12% leave (about 257) | Waiting on rights check; time-to-first-usable-creative never measured | Funnel export (measured); rights data quality uncertain (reported) |
| Understand pricing | Advertiser; pricing service | About 1,070 enter; 9% leave (about 193) | Price shown without explanation (assumed) | Funnel export (measured) |
| Book and confirm | Advertiser; a person confirms every purchase | About 877 enter; 6% leave (about 53) | n/a | Funnel export (measured) |
| After the run | Sales staff | Refunds 3% of orders; about 35 escalations a week | Ad did not run where expected (assumed typical case) | User said, Q3 2026 (reported) |

Signals used: funnel counts by step (measured, funnel export Q3 2026), refund rate (reported by the user), escalation volume (reported by the user). Derived counts in brackets are my arithmetic from the percentages, not from the export. Time per step and ticket drivers are not logged.

## 3. Opportunity portfolio

Scores are the AI engineer's judgements from the conversation of 15 October 2026, with the product owner's agreement on O1 only. Risk 5 means money, messages to real people, regulated decisions or irreversible effects without a review path.

| ID | Opportunity | Value (1-5) | Feasibility (1-5) | Data readiness (1-5) | Risk (1-5) | Fit | Measure | Baseline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | Help an advertiser choose the right product in one sitting, so more of the 38% who leave at product choice reach creative upload | 5 | 4 | 4 | 2 | llm | Completion of the product-choice step (share of starts that reach creative upload) | 62% (100 - 38), funnel export Q3 2026 |
| O2 | Cut the wait for a usable creative, so fewer of the 12% leave at upload | 3 | 2 | 2 | 3 | unclear | Time-to-first-usable-creative | unknown |
| O3 | Explain the price shown in plain language, so fewer of the 9% leave at pricing | 2 | 4 | 4 | 2 | rules | Completion of the pricing step | 91%, funnel export Q3 2026 |
| O4 | Draft escalation replies for the six sales staff from the catalogue and the order | 2 | 3 | 3 | 3 | llm | Escalations per week | 35 a week, reported |

Helper output (ranking and findings, pasted):

```text
Rank | ID | Score | Value | Feas. | Data | Risk | Fit | Measure | Opportunity
1 | O1 | 11 | 5 | 4 | 4 | 2 | llm | Completion of the product-choice step (share of starts that reach creative upload) | Help an advertiser choose the right product in one sitting, so more of the 38% who leave at product choice reach creative upload
2 | O3 | 8 | 2 | 4 | 4 | 2 | rules | Completion of the pricing step | Explain the price shown in plain language, so fewer of the 9% leave at pricing
3 | O4 | 5 | 2 | 3 | 3 | 3 | llm | Escalations per week | Draft escalation replies for the six sales staff from the catalogue and the order
4 | O2 | 4 | 3 | 2 | 2 | 3 | unclear | Time-to-first-usable-creative | Cut the wait for a usable creative, so fewer of the 12% leave at upload

First use case: O1 (Help an advertiser choose the right product in one sitting, so more of the 38% who leave at product choice reach creative upload)
Ready for adk-system-designer: the first use case has a measure and a technology fit.
```

Why the ranking came out this way: O1 has the most people behind it and the facts live in a database the team can reach; O3 is cheap but small; O2 has a data gate (rights metadata of uncertain quality) and no baseline, so it waits for measurement; O4 helps staff, not the KPI. O2 stays in the portfolio with the trigger "time-to-first-usable-creative measured for one quarter".

## 4. First use case

- **Chosen:** O1: a guided product recommendation in the self-serve flow, where the advertiser describes the promotion in their own words and gets one to three fitting products with the reason, each confirmable by a person before booking. Why first: largest drop, data at hand, reversible, a person already confirms every purchase. Leaves out: creative generation, pricing changes, and any automatic booking.
- **Users:** small-business advertisers in the self-serve flow (about 2,140 starts a quarter); the six sales staff receive the corrections.
- **Technology fit:** `llm` (one bounded judgement with a schema; code filters the catalogue and a person confirms). Stakeholder sentence: You asked whether AI can handle product choice. The input is free-text about the promotion plus structured catalogue records, the rules are known but dependent on context, and we have about 813 abandoned and 1,327 completed step records from one quarter to evaluate against (not to learn from; no labelled "right product" column). That points to a language model with a fixed output over a catalogue the code has already filtered. We chose it over an agent because the step list (filter catalogue by region and format, rank, explain) can be written down and does not change. The error cost is low, so the advertiser and then a person review every output before money moves. The platform team keeps it current, including the model upgrades the vendor requires; the design will state what it costs to run. Nearest alternative rejected: `agent` (no step the model needs to choose); `rules` would need a goal-to-product mapping nobody has written.
- **Outcome measure:** product-choice completion: share of purchase starts that reach creative upload, from the funnel export, per quarter and for the proof-of-concept window, read by the product owner.
- **Baseline:** 62% of 2,140 starts (38% left), funnel export, Q3 2026.
- **Counter-metric:** refund rate, 3% of orders (user said, Q3 2026); secondary: escalations per week (35).
- **Hypothesis chain:**

  ```text
  less effort to choose a product
    → more starts reach creative upload (62% → higher)
    → more bookings and self-serve revenue, with refunds flat at 3%
  ```

  Every arrow is a hypothesis until measured.
- **Data register:**

  | Source | Owner | Access path | Freshness | Friction logged today? |
  | --- | --- | --- | --- | --- |
  | Product catalogue | Platform team | Platform database (invented: read access via the platform API) | Live | Yes (funnel step) |
  | Pricing service | Platform team | Existing API | Live | Yes |
  | Inventory service | Platform team | Existing API | Live | No |
  | Funnel export | Product owner | Analytics export, quarterly | Quarterly | Yes |
  | Creative rights metadata | Creative library owner (unknown: ask) | Unknown | Unknown | No (out of scope for O1) |

- **Workflow before and after:** Before: advertiser browses about 40 products, opens a sales chat or leaves. After: advertiser types the promotion in one sentence; code filters the catalogue by region and format; the model ranks one to three and explains; advertiser picks; a person confirms at booking as today. Steps removed: unaided browsing and the product-choice escalation to sales; the person's confirmation is kept at 100% of purchases.
- **Permission scope and harms:** reads the catalogue, pricing and inventory APIs; changes nothing. Harms: (1) a product that cannot run in the advertiser's region (guardrail: code filters by region before the model sees the list; threshold zero out-of-region recommendations in the acceptance set); (2) a stated price or availability that is wrong (guardrail: price and availability come from the APIs, never from the model); (3) a recommendation with no reason (guardrail: the schema requires a reason tied to a catalogue field). Price and eligibility statements are grounded in the pricing and inventory services or routed to sales.
- **Unit economics known so far:** about 2,140 starts a quarter, so about 700 model calls a month at one call per start; cost ceiling: "less than one sales hire" (user said); after the pilot, the platform team's budget hosts it (user said the platform team hosts; who pays the model bill: unknown: ask).
- **Correction loop:** the advertiser's choice versus the recommendation is logged; sales staff flag wrong recommendations from escalations; the product owner reviews weekly; the artefact that changes is the catalogue filter rule or the evaluation case set, not the prompt alone.
- **Embedding:** the proof of concept runs on live traffic in the self-serve platform from week two for one region or a share of starts (designer to choose); "scaled" means all starts, and needs the platform team's hosting sign-off.
- **Build or buy:** build; the catalogue and the rules are ours, and no partner runs this process (user said; assumed no vendor evaluation done).
- **Cost of a wrong answer:** the advertiser picks an unsuitable product; the advertiser or the confirming person notices before booking; undone by choosing again; a person reviews before any effect.
- **Threshold sentences:** "If product-choice completion for the self-serve purchase flow does not rise above 62% in the proof-of-concept window, we will not propose production." "If the refund rate for self-serve orders rises above 4%, we will switch the recommendation off and review the cases."
- **Automate or augment:** augment; the advertiser keeps the choice and the person keeps the confirmation.
- **What changes for the people in it:** sales staff handle fewer product-choice escalations and take on reviewing flagged recommendations (about an hour a week, assumed); the product owner reads the weekly measure.
- **Success in 90 days looks like:** advertisers on the self-serve platform reach creative upload more often than the 62% baseline, with refunds still at 3%. Press release (future): "A bakery owner types 'weekend promotion for my shop in the east of town', sees two local products with a reason for each, picks one and books in one sitting, without calling anyone."

## 5. Constraints and facts for the designer

| Scope-gate question | Answer (confirmed / assumed) |
| --- | --- |
| Deadline for the first useful version, and what follows | Four-week proof of concept, one developer, decided 29 Oct 2026; production decision review two weeks after it ends (confirmed) |
| People, hours, familiarity with ADK and GCP | One developer for four weeks (confirmed); ADK and GCP familiarity: unknown: ask |
| Money for models and cloud | Ceiling "less than one sales hire" (confirmed, vague); proof-of-concept budget: unknown: ask |
| Who uses or judges it, and what they read | Advertisers use it; the product owner and the Director of SMB Sales judge it on product-choice completion from the funnel export (confirmed) |
| Data touched and effects allowed | Reads catalogue, pricing, inventory; no writes; a person confirms every purchase (confirmed) |
| Who must approve the next step, and when | Leadership, 29 Oct 2026 (proof of concept); production decision review two weeks after the proof of concept ends (confirmed) |

Known constraints: the platform team hosts whatever is built (confirmed); identity, data residency, regulation, brand: unknown: ask.

## 6. Stakeholders and the decision calendar

| Stakeholder | Cares about | Decides | When |
| --- | --- | --- | --- |
| Director of SMB Sales (sponsor) | Self-serve revenue | Funds the work | Ongoing; proof of concept 29 Oct 2026 |
| Leadership | Easier buying, revenue | Proof-of-concept go-ahead | 29 Oct 2026 |
| Platform product owner | Funnel completion | Judges the measure | Weekly during the pilot |
| Platform team | Hosting, operations | Hosting sign-off for production | Production decision review |
| Six sales staff | Fewer escalations | Nothing; report corrections | Weekly |

- **Senior owner:** Director of SMB Sales, self-serve revenue budget line; will fund one team for a year: yes.
- **People plan:** sales staff review flagged recommendations weekly (training: one session, assumed); champion among unofficial AI users: unknown: ask.

Presentation milestones the plan should carry: proof-of-concept approval, leadership, 29 Oct 2026; production decision review, two weeks after the proof of concept ends; results review after one quarter in production.

## 7. Stall checks

| Cause | Answered where |
| --- | --- |
| Problem misframed | §1 two-voice statement; product owner agrees |
| No baseline or measure | §4 measure and baseline (62%, Q3 2026) |
| Workflow not redesigned | §4 workflow before and after (browsing and the escalation removed) |
| No senior owner | §6 senior owner (yes, one team for a year) |
| No human-validation point | §4 workflow (person confirms 100% of purchases) |
| Data poor or inaccessible | §4 data register; gap: creative rights owner (out of scope for O1) |
| Cost not modelled per unit | §4 unit economics; gap: who pays the model bill after the pilot (sponsor settles) |
| Risk controls absent | §4 permission scope and harms |
| Change and training ignored | §6 people plan; gap: champion unknown (product owner settles) |
| No feedback loop | §4 correction loop |
| Pilot not embedded | §4 embedding (live traffic from week two) |
| Build or buy on pride | §4 build or buy; gap: no vendor evaluation done (AI engineer settles) |
| Model churn breaks the target | §4 technology fit (filters are code; acceptance on completion rate) |

## 8. Assumptions, open questions and what would change the choice

| Assumption or question | Why it changes the choice | How to settle it | Owner |
| --- | --- | --- | --- |
| The funnel export's "product choice" step is where the advertiser picks, not a page-load artefact | If the drop is a page problem, the fit is `process` | Product owner checks the step definition | Product owner |
| Catalogue read access via the platform API this month (invented) | No access, no proof of concept | Platform team confirms | Platform team |
| Developer's ADK and GCP familiarity | Sets the depth of the design | Ask | AI engineer |
| Who pays the model bill after the pilot | Cost goal and the cancel condition | Sponsor decides | Director of SMB Sales |
| Proof-of-concept traffic share and region | Sample size for the measure | Designer proposes, product owner approves | Designer |

## 9. Next prompt

```text
/adk-system-designer Read docs/discovery/smb-self-serve-ads.md and design the first use
case it selects (O1: a guided product recommendation in the self-serve flow that turns the
advertiser's description into one to three fitting products with reasons, confirmed by a
person before booking). Treat its confirmed answers as settled; ask only what it leaves
open. The outcome measure is product-choice completion (share of purchase starts that reach
creative upload) against 62% (funnel export, Q3 2026), with the refund rate (3% of orders) as
the guardrail. The sponsor is the Director of SMB Sales; leadership decides on the four-week,
one-developer proof of concept on 29 October 2026, so plan a presentation goal for it. Design only.
```
