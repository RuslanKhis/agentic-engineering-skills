# Discovery brief: SMB self-serve advertising

Status: draft, reviewed with the self-serve platform product owner on 15 October 2026
Entry: rough area ("Leadership wants to use AI so that small businesses can buy advertising from us more easily, but nobody has said where")
Next step: `adk-system-designer` with the first use case below (O1)

Everything below is either what the user said, what a cited source says, or a labelled assumption. Numbers carry their source and date. The only source supplied is the platform analytics quarterly export (Q3 2026, exported 3 October 2026), quoted by the product owner; the sales escalation volume is reported by the sales team, not counted.

## 1. Business and the outcome that matters

- **What the business sells and to whom:** A media company sells advertising (radio spots, display packages, a local newsletter slot and similar products) to small businesses through a self-serve platform, with a sales team of six handling escalations.
- **KPIs leadership watches:** Self-serve advertising revenue (the sponsor's KPI; current value not supplied). Self-serve purchase completion: 749 of 2,140 eligible starters (35%) completed last quarter (platform analytics, Q3 2026, exported 3 Oct 2026). Refunds: 3% of orders (same source).
- **Processes that move those KPIs:** The self-serve buying journey (product choice, creative upload, pricing, booking), owned by the platform product owner, 2,140 starts per quarter. Sales escalations from that journey, owned by the Director of SMB Sales, about 35 a week (reported by the sales team; not counted by reason).
- **Who decides what, and when:** The Director of SMB Sales decides what to propose and takes it to the leadership meeting on 29 October 2026; leadership decides whether to fund a proof of concept (one developer, four weeks). A production decision follows the build and a measurement window.

## 2. The journey and where it breaks

One journey, told from the advertiser's side. Running example: a two-location bakery promoting a weekend opening in one suburb; it would have abandoned at product choice without a sales call, in which a salesperson picked a geo-targeted display package for it.

| Step | Who does it today | Volume (Q3 2026) | Where it fails or stalls | Evidence (source, date) |
| --- | --- | --- | --- | --- |
| Start a purchase | Advertiser alone on the platform | 2,140 eligible starters | n/a | Platform analytics, Q3 2026, exported 3 Oct 2026 |
| Choose a product | Advertiser alone; sales by phone when they escalate | 2,140 enter, 813 leave (38% of starters), 1,327 proceed (62%) | Eleven products; the advertiser cannot tell which fits their goal and either leaves or calls sales | Measured: same export. Reported: sales says most escalations are "which product should I buy" |
| Upload a creative | Advertiser alone | 1,327 enter, 257 leave (12% of starters), 1,070 proceed (81%) | No creative to hand, or wrong format; time to a first usable creative has never been measured | Measured exits: same export. Reported: product owner |
| See pricing | Advertiser alone | 1,070 enter, 193 leave (9% of starters), 877 proceed (82%) | Price not known until this step; sales reports "what will this cost me" escalations | Measured exits: same export. Reported: sales team |
| Book and confirm | Advertiser; a person must confirm any purchase | 877 enter, 128 leave (6% of starters), 749 complete (85%) | Reasons not logged | Measured exits: same export |
| Changes after booking | Sales team of six | not counted | Changes go through sales; some are refunded; refunds 3% of orders | Measured refunds: same export. Reported: product owner |

Signals used: funnel counts by step (measured), refund rate (measured), "contact sales" clicks per step (logged, not supplied), sales escalation volume and reasons (reported anecdotally), the bakery case (reported). Not available: exit reasons, abandoner surveys, time per step. Assumption A1: the steps are sequential in the order above, so the per-step proceed rates are derived from the share-of-starters figures.

## 3. Opportunity portfolio

Scores 1 to 5 are the product owner's judgements, proposed by the agent and confirmed or adjusted in the conversation on 15 October 2026 (O2 risk raised from 3 to 4 by the product owner). `Fit` is one of `agent`, `llm`, `ml`, `rules`, `process`, `unclear` (the skill's technology-fit reference). `Risk` 5 means money, messages to real people, regulated decisions or irreversible effects without a review path. Ranking computed with `rank_opportunities.py` (output quoted below the table).

| ID | Opportunity | Value (1-5) | Feasibility (1-5) | Data readiness (1-5) | Risk (1-5) | Fit | Measure | Baseline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | Product choice: recommend one catalogue product from the advertiser's own description of business and goal, with price and availability looked up by code | 5 | 4 | 4 | 2 | llm | Product-choice step completion rate (advertisers who select a product and reach creative upload / eligible starters), weekly | 62% (1,327 of 2,140), platform analytics Q3 2026, exported 3 Oct 2026 |
| O2 | Creative upload: produce a first usable creative in the right format from the advertiser's photo or text | 3 | 3 | 2 | 4 | llm | Time to first usable creative (minutes from entering the creative step to a creative accepted by the platform), weekly median | unknown |
| O3 | Pricing clarity: show the exact price for the chosen product, dates and locations at product choice, computed by the pricing service | 2 | 5 | 4 | 1 | rules | Pricing-step completion rate, weekly | 82% (877 of 1,070, derived under A1), same export |
| O4 | Booking and escalations: add reason codes to sales escalations and fix the booking form | 1 | 4 | 4 | 3 | process | Booking-step completion rate and sales escalations per week | 85% (749 of 877, derived under A1); escalations ~35 a week (reported, uncounted) |

Helper output (`python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief docs/discovery/smb-advertising.md`, run 15 October 2026): O1 scores 11, O3 10, O4 6, O2 4; first use case O1; no blocking findings and no warnings; "Ready for adk-system-designer: the first use case has a measure and a technology fit."

Why the ranking came out this way: O1 has the largest drop with the most advertisers behind it (813 a quarter), the facts live in services with APIs, and a wrong answer is reversible before booking with a person confirming every purchase. O3 is one point behind because it is cheap and deterministic but touches a smaller drop; it shares the pricing API with O1 and is the natural second piece. O2 has the second-largest drop but its data readiness is 2 (rights metadata of uncertain quality) and its risk is 4 (publishing an asset without resale rights); it waits for a rights audit and a baseline. O4 is a process change. No opportunity was moved from its computed rank.

Technology fit per candidate, with the nearest alternative rejected and the one observable reason:

- O1 `llm`, over `agent`: the step list (collect goal, budget, area and dates; shortlist products; look up price and availability; present) can be written down and does not change; the model makes one bounded judgment under a schema, code makes the lookups.
- O2 `llm`, over `process` (a template gallery): the input is a photo or free text and the output format depends on the product; provisional until the rights flag on the asset library is audited.
- O3 `rules`, over `llm`: the price on screen must equal the invoice every time; the pricing service already computes it; an LLM doing arithmetic is the named mistake.
- O4 `process`, over an `llm` classifier of CRM notes: escalation reasons are not recorded, so the first step is a reason code in the CRM owned by sales, not software.

## 4. First use case

- **Chosen:** O1: help a self-serve advertiser who describes their business and goal in their own words pick one catalogue product, with price and availability looked up by code. It is first because it is the largest measured drop, the facts are reachable, the error is reversible with a person before any purchase, and one developer can show it in four weeks. It deliberately leaves out creative generation, any change to pricing logic, booking, and anything that writes to the order system.
- **Users:** Self-serve advertisers at the product-choice step, about 2,140 a quarter (roughly 165 a week), each once per purchase. The sales team of six reviews a sample of recommendations in the first weeks.
- **Technology fit:** `llm`. You asked whether AI can handle product choice for self-serve advertisers. The input is free text (the advertiser's description of their business and goal), the rules for matching a goal to a product are known but dependent on context, and we do not have recorded past outcomes of "the right product" to learn from, only 813 abandonments a quarter. That points to a language model with a fixed output: one or two catalogue products with a reason, while price and availability are looked up by code in the existing product and pricing services. We chose it over an agent that works through the steps itself because the step list can be written down and does not change. The error cost is low, so the advertiser chooses and a person confirms every purchase before money moves. Running cost per recommendation is for the designer to state (assumption A4: interactive, about 165 calls a week); the product owner keeps the catalogue mapping current and the designer names who owns prompt changes and vendor model upgrades. Not an agent; not a chatbot in front of the product list: the model sits behind a short form.
- **Outcome measure:** product-choice step completion rate: advertisers who select a product and reach creative upload, divided by eligible advertisers who started a purchase, per week, from the platform analytics, read by the product owner; over a four-week window after launch, all self-serve starters.
- **Baseline:** 62% (1,327 of 2,140), platform analytics Q3 2026, exported 3 October 2026.
- **Counter-metric:** refund rate on self-serve orders, 3% of orders (Q3 2026, same export), and sales escalations per week, about 35 (reported by the sales team; the team must agree a counted baseline before it is used).
- **Leading indicator:** weekly exits at the product-choice step and "contact sales" clicks at that step (logged in the platform).
- **Hypothesis chain:**

  ```text
  less effort to choose a product (described in the advertiser's words, priced and available)
    → more advertisers reach creative upload (completion from 62% towards 70%)
    → more completed self-serve purchases and self-serve revenue, with refunds flat at 3% and escalations not rising
  ```

  Every arrow is a hypothesis until measured. More use of the assistant establishes none of them.
- **Systems that own the facts:** product catalogue and pricing (product service, API; product service team grants access, assumption A2 on who in that team), inventory and availability (existing service, API; same team assumed), platform analytics (product owner), CRM escalation notes (sales). The creative library is not needed for O1.
- **Cost of a wrong answer:** the advertiser is shown a product that does not fit; they can change it before booking, a person confirms every purchase, and nothing is charged until confirmation. Who notices: the advertiser, the confirming person, or sales on an escalation. Reviewed before any effect: yes, by the confirming person; the assistant has no write effect.
- **Threshold sentences:** "If product-choice step completion for the self-serve buying journey rises above 70% over four consecutive weeks with refunds at or below 3%, we will propose a production decision." "If refund rate for self-serve orders rises above 4% in any two consecutive weeks, or weekly sales escalations rise above 45 against an agreed count, we will pause the recommendation and have sales review every recommended product before it is shown."
- **Automate or augment:** augment. The assistant proposes, the advertiser chooses, a person confirms the purchase. Nobody asked for the choice to be taken away from the advertiser; sales keeps escalations.
- **What changes for the people in it:** advertisers answer a short form (business, goal, area, dates, budget) instead of scanning eleven products. Sales reviews a sample of recommendations weekly for the first weeks and takes "the assistant told me X" calls, and agrees the escalation count. The product service team exposes catalogue and availability endpoints. The product owner reads the weekly number.
- **Success in 90 days looks like:** Self-serve advertisers who describe their business and goal are shown a product that fits, and product-choice completion has moved from 62% towards 70% with refunds flat at 3% and escalations not above the agreed count.

  Future press release, in the customer's words: "I run a bakery with two shops and wanted to tell Northcote about our Saturday opening. I used to open the ad site, see eleven products I did not understand, and phone someone. Now I type 'Saturday opening, Northcote, about $400' and it shows me the one package that reaches that suburb that weekend, what it costs, and that it is available. I picked it, added a photo, and confirmed. Nobody had to call me, and the price was the price on the invoice."

## 5. Constraints and facts for the designer

| Scope-gate question | Answer (confirmed / assumed) |
| --- | --- |
| Deadline for the first useful version, and what follows | Confirmed: proof-of-concept decision at leadership on 29 October 2026; if funded, one developer for four weeks (build ends about 27 November 2026, assumption A3 on start date); then a four-week measurement window and a production decision |
| People, hours, familiarity with ADK and GCP | Confirmed: one developer, full time, four weeks. Familiarity with ADK and GCP: unknown: ask |
| Money for models and cloud | Confirmed: no budget line yet. Amount: unknown: ask |
| Who uses or judges it, and what they read | Confirmed: self-serve advertisers use it; the Director of SMB Sales judges it on self-serve revenue and reads the weekly product-choice completion rate from platform analytics; leadership reads the proof-of-concept proposal |
| Data touched and effects allowed | Confirmed: read-only access to product catalogue, pricing and availability through existing APIs; no write to orders; no purchase without a person confirming; advertiser free text is the only input. Whether that text may contain personal data: unknown: ask |
| Who must approve the next step, and when | Confirmed: leadership, on 29 October 2026, on the Director of SMB Sales's proposal |

Known systems, platforms, identity, data residency, regulation, brand or legal constraints:
- Pricing and inventory: existing services with APIs (confirmed).
- Product catalogue: in the product service with pricing (reported by the product owner).
- Creative library with rights metadata of uncertain quality (confirmed; not in O1's scope).
- Price shown must equal the price invoiced (reported; finance requirement).
- Cloud platform, identity, data residency: unknown: ask.

## 6. Stakeholders and the decision calendar

| Stakeholder | Cares about | Decides | When |
| --- | --- | --- | --- |
| Director of SMB Sales (sponsor) | Self-serve revenue; escalation load on her team | What to propose to leadership; whether to pause on the counter-metric | 29 October 2026 proposal; weekly during measurement |
| Leadership | Whether the proof of concept is worth one developer for four weeks | Funding the proof of concept; later the production decision | 29 October 2026; after the measurement window (about late December 2026, assumption A3) |
| Self-serve platform product owner | Step completion, the journey, the measure | Scope of the product-choice step; reads the weekly number | Throughout |
| Sales team of six | Escalation volume and quality of recommendations | Agrees the escalation count; reviews sampled recommendations; triggers a pause request | Weekly in the first weeks after launch |
| Product service team (engineering) | API exposure, load on catalogue and pricing endpoints | Grants access to catalogue and availability endpoints | First week of the build |
| Finance | Price shown equals price invoiced | Rejects anything that estimates price | At design review |

Presentation milestones the plan should carry (each becomes an `adk-presenter` goal): proof-of-concept approval at leadership on 29 October 2026; production decision after the four-week measurement window (about late December 2026); results review against the 90-day sentence.

## 7. Assumptions, open questions and what would change the choice

| Assumption or question | Why it changes the choice | How to settle it | Owner |
| --- | --- | --- | --- |
| A1: the funnel steps are sequential (product choice, creative, pricing, booking) | The per-step proceed rates and the O3 and O4 baselines are derived from it | Check the step order in the analytics export | Product owner |
| A2: the product service team can expose catalogue and availability endpoints within the first week of the build | O1 feasibility 4 depends on it; without access, a data-access goal comes first | Ask the product service lead before 29 October | Product owner |
| A3: the build starts the week after approval | The measurement window and production-decision date move with it | Confirm with engineering on approval | Director of SMB Sales |
| A4: about 165 recommendations a week, interactive | Per-call cost and latency are stated by the designer from this | Derived from 2,140 starters a quarter; confirm with analytics | Product owner |
| Does the advertiser's free text contain personal data, and where may it be processed? | Sensitive-data handling and residency constraints in the design | Ask legal or privacy before design | Product owner |
| Developer's familiarity with ADK and GCP | Depth the designer can plan in four weeks | Ask engineering | Product owner |
| Model and cloud budget | Whether an interactive model call per advertiser is affordable | Ask finance with the designer's per-call estimate | Director of SMB Sales |
| Sales escalation count and reasons are not recorded | The counter-metric has no counted baseline; O4 depends on reason codes | Sales counts escalations by reason for two weeks before launch | Director of SMB Sales |
| Rights metadata quality on the creative library | O2 stays at data readiness 2 and risk 4 until audited; O2's trigger to move up | Audit the "licensed for resale" flag on a sample | Product owner with legal |
| Time to first usable creative is unmeasured | O2 has no baseline; measurement would be O2's first goal | Add a timestamp on creative accepted | Product owner |
| Would it change the choice? | If the product-choice drop is mostly advertisers who were not eligible after all, or who leave for price reasons before seeing a price, O3 moves first | Sample 50 product-choice exits and their "contact sales" clicks | Product owner |

Triggers that bring the next opportunities forward: O3 (pricing preview) when O1 is live and calls the pricing API; O2 (creative) when the rights audit passes and the creative-step timestamp exists; O4 when sales has two weeks of reason codes.

## 8. Next prompt

```text
/adk-system-designer Read docs/discovery/smb-advertising.md and design the first use
case it selects (O1: help a self-serve advertiser who describes their business and
goal in their own words pick one catalogue product, with price and availability
looked up by code). Treat its confirmed answers as settled; ask only what it leaves
open. The outcome measure is product-choice step completion rate against 62%
(1,327 of 2,140, Q3 2026), with refund rate (3% of orders) and sales escalations
(~35 a week) as the guardrails. Plan a presentation goal for the proof-of-concept
decision on 29 October 2026 and a production decision after the four-week build.
Design only.
```
