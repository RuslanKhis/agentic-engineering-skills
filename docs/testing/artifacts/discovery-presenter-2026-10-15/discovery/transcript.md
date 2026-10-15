# Trial transcript: /adk-discovery, SMB advertising

Both roles are simulated. AGENT follows `skills/adk-discovery/SKILL.md`. USER is a product owner of the self-serve ad platform; facts marked **(invented)** were not in the trial brief and were made up to keep the conversation plausible.

---

**USER (turn 0):**
/adk-discovery Leadership at our media company wants to use AI so that small businesses can buy advertising from us more easily, but nobody has said where. Help me work out where it would pay off, which workflow to improve first, what we would measure, and whether an agent is even the right tool. Save the brief.

---

**AGENT (turn 1):**

What I have so far, separated:

- You said: leadership wants AI so small businesses buy advertising more easily; the location is not chosen; you want the first workflow, the measure, and whether an agent is the right tool.
- Sources supplied: none yet.
- I assume: there is a self-serve buying journey already (product choice, creative, pricing, booking) and the small businesses in question are its users.

Mode: **rough area** (the domain is SMB advertising sales; the journey is "buying advertising from us"). Correct me if you meant to start from the whole business instead. I would first understand where advertisers abandon the current buying journey: choosing the right product, creating an ad, understanding pricing, or completing booking, and use that to choose the first workflow and the outcome to measure. The answer may turn out not to be an agent, or not AI at all.

Three questions:

1. Where do advertisers abandon the journey today, and is that logged? (Decides which workflow goes first. Default if you cannot say: assume product choice, the usual largest drop in self-serve ad funnels, and make measuring the funnel the first step.)
2. Who is the sponsor and which KPI are they judged on this year? (Fixes the metric every candidate is scored against. Default: self-serve advertising revenue.)
3. Walk me through one real advertiser, from landing on the platform to money received: where did it wait, bounce back, or need a person? (Locates friction in observed work; it becomes the running example. Default: I will construct a typical case and mark it assumed.)

---

**USER (turn 1):**

1. Yes, it is logged. Last quarter 2,140 eligible advertisers started a purchase on the self-serve platform. 38% left at product choice, 12% at creative upload, 9% at pricing, 6% at booking; the rest completed. That is from the platform analytics quarterly export **(invented: dated 3 October 2026, Q3 2026 window)**.
2. The sponsor is the Director of SMB Sales. She is judged on self-serve revenue.
3. **(invented)** A two-location bakery wanted to promote a weekend opening. They landed on the product list, saw eleven products (radio spots, display packages, a local newsletter slot and so on), could not tell which fitted a weekend event in one suburb, and called our sales line. A salesperson picked a geo-targeted display package for them, they uploaded a photo of the shop, the pricing page quoted a weekly rate, they booked, and the invoice was paid on net-30. Without the call they would have been one of the 38%.

---

**AGENT (turn 2):**

Recorded as measured (platform analytics, Q3 2026, exported 3 Oct 2026): of 2,140 starters, 813 left at product choice (38%), 257 at creative upload (12%), 193 at pricing (9%), 128 at booking (6%), 749 completed (35%). I assume the steps are sequential in that order, so the step-level rates are: product choice 62% proceed (1,327 of 2,140), creative 81% (1,070 of 1,327), pricing 82% (877 of 1,070), booking 85% (749 of 877). Tell me if the funnel is not sequential.

Running example: the bakery. It would have abandoned at product choice without the sales call.

Three questions:

1. Who handles the product-choice step today when a person is involved, and how often? Is "which product should I buy" counted anywhere? (Decides frequency and the role whose metric moves. Default: sales handles it, volume uncounted.)
2. Which systems own the facts a recommendation would need (product catalogue, pricing, inventory/availability, creative assets) and can we reach them this month? (Data readiness is a gate; no owner, no use case. Default: catalogue and pricing reachable, creative not.)
3. Where do advertisers contact support or retry, and is that logged by reason? (Failure signals; a signal nobody logs needs measuring first. Default: not logged by reason.)

---

**USER (turn 2):**

1. The sales team of six handles escalations from the self-serve platform. **(invented)** Roughly 35 a week reach them; the CRM has a free-text note, not a category, but the team says most are "which product should I buy" and "what will this cost me".
2. Pricing and inventory live in existing services with APIs. **(invented)** The product catalogue is in the same product service as pricing. Creative assets live in a library with rights metadata, but the quality of that metadata is uncertain; nobody has audited whether the "licensed for resale" flag is reliable.
3. **(invented)** The platform logs step exits but not the reason; the "contact sales" button click is logged per step. We do not survey abandoners.

---

**AGENT (turn 3):**

Candidates, each as an activity plus an expected result with units and a frequency, in your job language:

- **O1 Product choice.** Help an advertiser who describes their business and goal in their own words pick one product from the catalogue, with availability and price checked in the product service, so that more of the ~813 advertisers a quarter who leave at product choice proceed to creative. Result: product-choice step completion rises from 62%.
- **O2 Creative upload.** Turn an advertiser's photo or short text into a first usable creative in the right format for the chosen product, so fewer of the ~257 a quarter who leave at creative upload stall. Result: time to first usable creative falls (currently unmeasured) and creative-step completion rises from 81%.
- **O3 Pricing clarity.** Show an advertiser what their chosen product will cost for their dates and locations before the pricing step, so fewer of the ~193 a quarter who leave at pricing do so. Result: pricing-step completion rises from 82%.
- **O4 Booking and escalation handling.** Reduce the ~128 a quarter lost at booking and the ~35 weekly sales escalations by routing or pre-answering them. Result: booking completion rises from 85%; escalations per week fall.

Three questions, mostly about error cost, which decides automate versus augment and whether AI fits at all:

1. What happens when a product recommendation is wrong: who notices, and can it be undone? Does a person confirm any purchase before money moves? (Default: assume a person confirms.)
2. Does the price shown have to be exactly the price invoiced, every time, for the same input? (Decides deterministic code versus a model for anything touching price. Default: yes.)
3. For creative: has anyone measured time to first usable creative, and what is the refund rate on orders today? (Baseline and the counter-metric. Default: unmeasured; refunds unknown.)

---

**USER (turn 3):**

1. A wrong product recommendation is reversible before booking; the advertiser can change the product, and a person must confirm any purchase. Nothing is charged until that confirmation. **(invented)** After booking, changes go through sales and are sometimes refunded.
2. Yes. **(invented)** The price on screen must equal the invoice; finance has rejected anything that estimates.
3. Nobody has measured time to first usable creative. Refunds were 3% of orders last quarter (same analytics export, Q3 2026).

---

**AGENT (turn 4):**

Technology fit, asking the reference's questions in order for each candidate:

- **O1 Product choice: `llm`.** Input is free text (the advertiser's description of their business and goal); the rules for mapping a goal to a product are known in prose but context-dependent; the output is a bounded judgment (one or two products from the catalogue, with a reason) under a schema; availability and price are lookups the code makes against the product service, never the model. The step list can be written down (collect goal, budget, area, dates → pick candidates → look up price and availability → present), so an agent that chooses its own path is not needed; nearest alternative rejected: `agent`. Error cost is low: reversible before booking, and a person confirms every purchase.
- **O2 Creative: `llm` (image or text generation), provisional.** Unstructured input; the rights metadata on the asset library is of uncertain quality, which is a data-readiness and legal risk; nothing is measured yet. Nearest alternative rejected: `process` (a template gallery). Provisional until the rights flag is audited.
- **O3 Pricing: `rules`.** Price must be exact and deterministic and the pricing service already computes it; the mistake to avoid is an LLM doing arithmetic. The fit is a price preview built on the pricing API, shown at product choice. Nearest alternative rejected: `llm`.
- **O4 Booking and escalations: `process`.** The booking drop is the smallest and a person confirms purchase anyway; escalation reasons are not categorised, so measurement (a reason code in the CRM) comes before any software. Nearest alternative rejected: `llm` classifier of CRM notes (no labelled outcomes).

Proposed scores (1 to 5; value, feasibility, data readiness, risk); I will record them as yours once you confirm or adjust:

| ID | Value | Feasibility | Data | Risk |
| --- | --- | --- | --- | --- |
| O1 | 5 | 4 | 4 | 2 |
| O2 | 3 | 3 | 2 | 3 |
| O3 | 2 | 5 | 4 | 1 |
| O4 | 1 | 4 | 4 | 3 |

Three questions:

1. Deadline, people and money: when must the first version exist, who builds it, and is there a budget for model and cloud usage? Who approves the next step and when? (Fills the scope gate the designer would otherwise ask. Default: unknown, marked "ask".)
2. What would make you cancel this in six months? (Cost ceiling, risk controls and the real value question.)
3. Who else has to change how they work for this to count? (Most of the effort is people and process.)

---

**USER (turn 4):**

Scores: fine, except raise O2 risk to 4; publishing a creative built on an asset we do not have resale rights for is a legal problem, not just a bad ad.

1. Leadership wants a proof-of-concept decision in two weeks, so 29 October 2026. If approved they would give one developer four weeks. **(invented)** I do not know the developer's familiarity with ADK or GCP; I would have to ask engineering. There is no budget line for model usage yet. The Director of SMB Sales takes it to the leadership meeting on 29 October; she decides what to propose, leadership decides whether to fund the four weeks.
2. **(invented)** If the product-choice completion number does not move in the four weeks after launch, or if refunds or sales escalations go up because advertisers were steered to the wrong product.
3. **(invented)** The sales team: for the first weeks they would review a sample of recommendations and take any "the assistant told me X" calls. The product service team would have to expose the catalogue and availability endpoints to the new component.

---

**AGENT (turn 5):**

Scores recorded as yours, with O2 risk at 4. Choice: **O1 product choice** first. It is the largest drop with the most advertisers behind it, the facts live in services with APIs, a wrong answer is reversible and a person confirms every purchase, and one developer could show it in four weeks. O3 (pricing preview) is close behind and is a `rules` change; it is a natural second piece because O1 will call the same pricing API. O2 waits for the rights audit and a baseline. O4 is a process change (reason codes in the CRM) owned by sales.

For O1, the measure, which I want you to confirm:

- **Outcome measure:** product-choice step completion rate: advertisers who select a product and reach creative upload, divided by eligible advertisers who started a purchase, per week, read from the platform analytics by you. **Baseline:** 62% (1,327 of 2,140), Q3 2026, export of 3 Oct 2026.
- **Lagging outcome:** self-serve revenue (the sponsor's KPI). Usage of the assistant is not an outcome.
- **Counter-metric:** refund rate on self-serve orders, 3% of orders (Q3 2026), and sales escalations per week, about 35 (reported by the sales team, not counted). Neither may get worse.
- **Leading indicator:** weekly exits at product choice, and "contact sales" clicks at that step.
- **Threshold sentences:** "If product-choice completion for the self-serve buying journey rises above 70% over four consecutive weeks with refunds at or below 3%, we will propose a production decision." "If refund rate for self-serve orders rises above 4% in any two consecutive weeks, or weekly sales escalations rise above 45, we will pause the recommendation and have sales review every recommended product before it is shown."
- **Automate or augment:** augment. The assistant proposes; the advertiser chooses; a person confirms the purchase. Sales keeps escalations and reviews a sample for the first weeks.
- **Success in 90 days:** "Self-serve advertisers who describe their business and goal are shown a product that fits, and product-choice completion has moved from 62% towards 70% with refunds flat at 3%."

Two questions:

1. Is that the number you would sign, and is refunds plus escalations the right pair that must not get worse? (Default: yes.)
2. In a customer's words, what does the better journey sound like? (Becomes the future press release paragraph. Default: I draft it from the bakery case.)

---

**USER (turn 5):**

1. Yes. That is the pair. Add that the sales team must agree the escalation count before we use it, since nobody has counted it properly.
2. Draft it from the bakery; **(invented)** the owner's words on the call were "I just want someone to tell me what works for a Saturday opening in Northcote and what it costs".

---

**AGENT (turn 6):**

Brief written to `docs/discovery/smb-advertising.md`. Helper run from the project root:

```text
$ python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief docs/discovery/smb-advertising.md
Rank | ID | Score | Value | Feas. | Data | Risk | Fit | Measure | Opportunity
1 | O1 | 11 | 5 | 4 | 4 | 2 | llm | Product-choice step completion rate (advertisers who select a product and reach creative upload / eligible starters), weekly | Product choice: recommend one catalogue product from the advertiser's own description of business and goal, with price and availability looked up by code
2 | O3 | 10 | 2 | 5 | 4 | 1 | rules | Pricing-step completion rate, weekly | Pricing clarity: show the exact price for the chosen product, dates and locations at product choice, computed by the pricing service
3 | O4 | 6 | 1 | 4 | 4 | 3 | process | Booking-step completion rate and sales escalations per week | Booking and escalations: add reason codes to sales escalations and fix the booking form
4 | O2 | 4 | 3 | 3 | 2 | 4 | llm | Time to first usable creative (minutes from entering the creative step to a creative accepted by the platform), weekly median | Creative upload: produce a first usable creative in the right format from the advertiser's photo or text

First use case: O1 (Product choice: recommend one catalogue product from the advertiser's own description of business and goal, with price and availability looked up by code)
Ready for adk-system-designer: the first use case has a measure and a technology fit.
```

Ranking is computed, not recalled: O1 at 11, O3 at 10, O4 at 6, O2 at 4. No blocking findings, no warnings. O1 is rank 1, so no override to record.

**Where the brief is:** `docs/discovery/smb-advertising.md`.

**First use case:** O1, help a self-serve advertiser who describes their business and goal in their own words pick one product from the catalogue, with price and availability looked up by code; measured by product-choice step completion rate against a baseline of 62% (1,327 of 2,140, Q3 2026, platform analytics export of 3 Oct 2026), with refund rate (3% of orders) and sales escalations (~35 a week, reported) as the numbers that must not get worse.

**Technology fit, for the stakeholder:** You asked whether AI can handle product choice for self-serve advertisers. The input is free text (the advertiser's description of their business and goal), the rules for matching a goal to a product are known but dependent on context, and we have no recorded past outcomes of "the right product" to learn from, only 813 abandonments a quarter. That points to a language model with a fixed output: one or two catalogue products with a reason, while price and availability are looked up by code in the existing services. We chose it over an agent that works through the steps itself because the step list can be written down and does not change. The error cost is low, so the advertiser chooses and a person confirms every purchase before money moves. Running cost per recommendation and who keeps the prompt current are for the designer to state; the product owner and sales keep the catalogue mapping reviewed. It is not an agent, and it should not be a chatbot in front of the product list: the model sits behind a short form.

**Next decision:** proof-of-concept go-ahead at the leadership meeting on 29 October 2026, proposed by the Director of SMB Sales; a production decision follows the four-week build and a four-week measurement window.

**Next prompt:**

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

Open items the designer should expect: the developer's ADK and GCP familiarity, the model and cloud budget, and whether the product service team can expose catalogue and availability endpoints in the first week; all marked "unknown: ask" in the brief.
