# Discovery brief: regional logistics firm, order intake

Status: draft / reviewed with the operations director on 15 October 2026
Entry: no use case yet ("I keep hearing about AI agents but do not know how the technology works or which of our processes it could help")
Next step: `adk-system-designer` with the first use case below

Everything below is either what the user said, what a cited source says, or a
labelled assumption. Numbers carry their source and date. Facts the simulated
user made up beyond the trial's given facts are marked (invented).

## 1. Business and the outcome that matters

- **The problem in the sponsor's words:** "I keep hearing about AI agents but do not know how the technology works or which of our processes it could help." Later: "she says the re-keying is the real pain."
- **The problem in the builder's words:** Four dispatchers spend an estimated 60 hours a week re-typing free-text email orders into the TMS, and nobody measures it or the errors it causes; difference noted: the sponsor asked about AI in general, the builder found one clerical step. Frontline user who agrees: the dispatcher who already drafts replies in a consumer chatbot (operations director, 15 Oct 2026).
- **What the business sells and to whom:** pallet and parcel transport for about 300 business customers in one region (invented); 120 trucks, 40 office staff (invented).
- **KPIs leadership watches:** on-time delivery 91% (TMS report, Q3 2026, reported by the operations director); cost per delivery (value not given); customer complaints about 60 a week (reported, not logged by cause).
- **Processes that move those KPIs:** order intake (four dispatchers, about 900 orders a week by email and phone); weekly driver scheduling (one planner, spreadsheet); proof-of-delivery disputes (about 25 a week); invoice queries (volume unknown).
- **Who decides what, and when:** the owner-CEO decides on a proposal in about three weeks, so a proof-of-concept go-ahead on about 5 November 2026; he would fund one team for a year if the first thing works (operations director, 15 Oct 2026).

## 2. The journey and where it breaks

One journey, the Smithfield-to-Albury order from last Tuesday (invented), told from the dispatcher's side:

| Step | Who does it today | Volume | Where it fails or stalls | Evidence (source, date) |
| --- | --- | --- | --- | --- |
| Customer emails or phones the order | Customer, shared orders mailbox | ~900/week | Free text in ~300 customers' formats; fields missing | Reported, ops director, 15 Oct 2026 |
| Dispatcher reads, phones for gaps, re-keys into TMS | Four dispatchers | ~900/week, ~4 min each (estimate from watching, never timed) | ~60 hours/week of re-typing; wrong entries | Reported estimate, 15 Oct 2026 |
| Dispatch review before planning | Planner | Weekly | Catches most wrong entries; misses not counted | Reported, 15 Oct 2026 |
| Planner builds driver schedules | One planner, spreadsheet | Weekly | Rules live in the planner's head | Reported, 15 Oct 2026 |
| Driver delivers, photo and signed PDF to shared drive | Drivers | ~900/week | Folders by month, no index | Reported, 15 Oct 2026 |
| Customer disputes a delivery | Office staff | ~25/week, ~40 min each (estimate) | ~17 hours/week hunting through PDFs | Reported estimate, 15 Oct 2026 |
| Invoice queries | Unknown | Unknown | Not counted | Reported, 15 Oct 2026 |

Signals used: time per step (reported estimates), rework (wrong entries, reported, not counted), hand-offs (mailbox to TMS to spreadsheet to drive), complaints (about 60 a week, reported). Nothing in this journey is measured: no correction counts, no dispute time, no intake time (ops director, 15 Oct 2026).

## 3. Opportunity portfolio

Scores 1 to 5 are the agent's judgements from the conversation, with the operations director's agreement on 15 October 2026. `Fit` is one of `agent`, `llm`, `ml`, `rules`, `process`, `unclear`. `Risk` 5 means money, messages to real people, regulated decisions or irreversible effects without a review path.

| ID | Opportunity | Value (1-5) | Feasibility (1-5) | Data readiness (1-5) | Risk (1-5) | Fit | Measure | Baseline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | Order intake: read each order email, propose the TMS order fields, dispatcher confirms with one click; ~900/week at ~4 min each to perhaps 1 min | 5 | 4 | 3 | 2 | llm | Dispatcher minutes per emailed order | ~4 min (reported estimate, unmeasured) |
| O2 | Proof-of-delivery disputes: find the photo and signed PDF for an order and draft the reply; ~25/week at ~40 min | 3 | 3 | 1 | 1 | process | Minutes per dispute | ~40 min (reported estimate) |
| O3 | Driver scheduling: build the weekly schedule from orders and driver availability | 4 | 2 | 2 | 3 | rules | Planner hours per week; on-time delivery | unknown |
| O4 | Invoice queries: answer customer questions about invoices | 2 | 2 | 1 | 2 | unclear | Queries per week | unknown |
| O5 | Complaint causes: categorise the ~60 weekly complaints by cause | 2 | 4 | 3 | 1 | llm | Share of complaints with a cause code | 0% (nothing logged) |

Fit notes, one line each: O1 llm, rejected agent (the step list never varies) and rules (free text in 300 formats). O2 process first (name and index files by order number with a script; no index means no retrieval), then llm for drafting. O3 rules in the sense of a deterministic optimisation solver (routing and rostering), not a language model; the planner's rules are not written down yet. O4 unclear until counted. O5 llm classification, reviewed weekly; measurement, not automation.

Helper output (ranking and findings, pasted):

```text
$ python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief docs/discovery/order-intake.md   (exit 0, 16 Oct 2026)
Rank | ID | Score | Value | Feas. | Data | Risk | Fit | Measure | Opportunity
1 | O1 | 10 | 5 | 4 | 3 | 2 | llm | Dispatcher minutes per emailed order | Order intake: read each order email, propose the TMS order fields, dispatcher confirms with one click; ~900/week at ~4 min each to perhaps 1 min
2 | O5 | 8 | 2 | 4 | 3 | 1 | llm | Share of complaints with a cause code | Complaint causes: categorise the ~60 weekly complaints by cause
3 | O2 | 6 | 3 | 3 | 1 | 1 | process | Minutes per dispute | Proof-of-delivery disputes: find the photo and signed PDF for an order and draft the reply; ~25/week at ~40 min
4 | O3 | 5 | 4 | 2 | 2 | 3 | rules | Planner hours per week; on-time delivery | Driver scheduling: build the weekly schedule from orders and driver availability
5 | O4 | 3 | 2 | 2 | 1 | 2 | unclear | Queries per week | Invoice queries: answer customer questions about invoices

First use case: O1 (Order intake: read each order email, propose the TMS order fields, dispatcher confirms with one click; ~900/week at ~4 min each to perhaps 1 min)
Ready for adk-system-designer: the first use case has a measure and a technology fit.
```

Why the ranking came out this way: O1 is the largest hour count, the input exists today (emails and their matching TMS orders), and a dispatcher can approve every order before it is created, so risk stays low. O5 ranks second on feasibility but moves nothing by itself. O2 scores on value but its data readiness is 1: the drive has no index, so its first step is a filing script the IT firm can run, not AI. O3 is the biggest prize for on-time delivery but the rules are undocumented and the planner is one person; it waits as O-next with the trigger "the planner writes down the scheduling rules". No `--pick` override: the chosen candidate is rank 1.

## 4. First use case

- **Chosen:** O1, order intake: a language model reads each order email in the shared mailbox and proposes the TMS order fields; a dispatcher approves with one click and ordinary code creates the TMS order. First because it is narrow (one step, one mailbox), measurable (TMS timestamps against mailbox timestamps), low risk (a person approves every order) and the data is at hand (past emails and their TMS orders). It deliberately leaves out phone orders, scheduling, disputes and any reply to the customer.
- **Users:** four dispatchers, about 900 orders a week, all day.
- **Technology fit:** llm. "You asked whether AI can handle order intake. The input is free-text emails, the rules for what goes in an order are stable, and we have thousands of past emails and their TMS orders to check against (assumed: the mailbox and the TMS keep history; confirm with the IT firm). That points to a language model with a fixed output, with ordinary code writing to the TMS. We chose it over a script because the emails come in 300 customers' formats, and over an agent because the steps never vary. The error cost is a wrong delivery, so a dispatcher approves every order before it is created. The external IT firm keeps it current, including model upgrades the vendor requires; the design will state what it costs to run."
- **Outcome measure:** dispatcher minutes per emailed order, from mailbox received time to TMS order created time, weekly median over the pilot, read from the TMS and mailbox by the operations director.
- **Baseline:** about 4 minutes (operations director's estimate from watching, 15 Oct 2026, never timed); the first goal is to measure the current journey for two weeks.
- **Counter-metric:** orders corrected at dispatch review and wrong-place deliveries (both uncounted today; counting them is part of the baseline goal), and complaints (about 60 a week, reported).
- **Hypothesis chain:**

  ```text
  less effort to re-key an emailed order
    → fewer dispatcher hours on intake (about 60/week reported to about 15/week)
    → lower cost per delivery or capacity for phone orders and disputes, with corrected orders, wrong deliveries and complaints flat
  ```

  Every arrow is a hypothesis until measured. The last arrow reaches a P&L line only if the operations director reassigns the freed hours; the brief records that as her decision, not the system's effect.
- **Data register:**

  | Source | Owner | Access path | Freshness | Friction logged today? |
  | --- | --- | --- | --- | --- |
  | Shared orders mailbox | Operations (dispatchers) | External IT firm holds admin; path unknown: ask | Live | No |
  | TMS orders | Operations | TMS API, external IT firm holds admin | Live | No (corrections not counted) |
  | Past emails and matching TMS orders (for evaluation) | Operations | Same two systems; retention unknown: ask | Historical | No |

- **Workflow before and after:** Today: read email, phone for gaps, re-key five field groups, send to dispatch review. After: the system drafts the fields from the email and flags gaps; the dispatcher reads the draft against the email, fixes or approves in one click, and still phones for gaps; dispatch review unchanged during the pilot. Step removed: re-keying. Step assisted: gap spotting. Validation: a dispatcher on 100% of orders before creation; the planner's dispatch review stays as the second check.
- **Permission scope and harms:** reads the orders mailbox; writes one order to the TMS only after approval; never emails a customer. Top harms: (1) a wrong address or date approved without reading, guardrail: corrected-at-review rate above the measured baseline stops the pilot; (2) a missed order (email not picked up), guardrail: daily count of emails against drafts must match; (3) customer data leaving the firm through the model vendor, guardrail: the design names where the data goes and the IT firm signs it off. Price or service statements are never generated; the system fills fields only.
- **Unit economics known so far:** about 900 emailed orders a week (the email share of 900 is not known: ask); cost ceiling not stated: ask; after the pilot the external IT firm hosts and the firm pays, per the CEO's one-year funding if the pilot works. The design estimates the cost itself.
- **Correction loop:** every dispatcher edit to a draft is stored with the email; the operations director reviews the edits weekly with the champion dispatcher; a repeated edit changes the prompt or becomes an evaluation case; a new customer format becomes an evaluation case.
- **Embedding:** the pilot runs on live emails in the real mailbox and creates real TMS orders from week one for one dispatcher's queue; "scaled" means all four dispatchers on all emailed orders and needs the operations director's and the IT firm's sign-off.
- **Build or buy:** build, small; no partner was named and the TMS vendor's intake options are unknown: ask the IT firm whether the TMS already offers email intake before building.
- **Cost of a wrong answer:** a wrong field becomes a wrong delivery if it passes both the dispatcher and dispatch review; noticed by the customer; undone by a redelivery at the firm's cost. A person reviews before any effect.
- **Threshold sentences:** "If dispatcher minutes per emailed order for the pilot queue does not fall below 2 minutes by the end of week four, we will stop and report why." "If orders corrected at dispatch review for the pilot queue rise above the measured baseline, we will pause the pilot the same day."
- **Automate or augment:** augment; the dispatcher keeps judgement, the phone call for gaps and the approval; the machine does the typing.
- **What changes for the people in it:** dispatchers move from typing to checking; one hour of training on reading a draft against an email; the champion dispatcher runs the pilot queue in week one; the workflow is the approval screen, not the old TMS form with a helper beside it.
- **Success in 90 days looks like:** emailed orders on the pilot queue take under two minutes of dispatcher time, measured in the TMS, with corrected orders and wrong deliveries no worse than the two-week baseline. "Since spring, when I email an order to the depot it is in their system within minutes and nobody rings me to ask what I already wrote; my deliveries have not been late or wrong any more often than before." (a Smithfield customer, imagined)

## 5. Constraints and facts for the designer

| Scope-gate question | Answer (confirmed / assumed) |
| --- | --- |
| Deadline for the first useful version, and what follows | Confirmed: CEO decision about 5 Nov 2026; a four-week proof of concept with one contractor is plausible; one team for a year if it works |
| People, hours, familiarity with ADK and GCP | Confirmed: one contractor, no platform team, external IT firm hosts everything; ADK and GCP familiarity unknown: ask |
| Money for models and cloud | Unknown: ask (CEO funds the team; a model and cloud ceiling was not discussed) |
| Who uses or judges it, and what they read | Confirmed: four dispatchers use it; the operations director judges on minutes per order; the CEO reads a proposal |
| Data touched and effects allowed | Confirmed: reads the orders mailbox, writes TMS orders after one-click approval, no customer contact |
| Who must approve the next step, and when | Confirmed: owner-CEO, about 5 Nov 2026 |

Known systems and constraints: TMS with an API, admin held by the external IT firm; shared mailbox (platform not named: ask); shared drive, folders by month, no index; hosting by the external IT firm; data residency, regulation and brand constraints not discussed: ask.

## 6. Stakeholders and the decision calendar

| Stakeholder | Cares about | Decides | When |
| --- | --- | --- | --- |
| Owner-CEO | A proposal that works; funds one team for a year if it does | Proof-of-concept go-ahead; production funding | About 5 Nov 2026; after the proof of concept |
| Operations director (sponsor) | On-time 91%, cost per delivery, complaints; dispatchers not working around the tool | Pilot scope, stop or continue | Weekly during the pilot |
| Four dispatchers | Less re-keying, no blame for machine errors | Whether to use it | Daily |
| External IT firm | Hosting, TMS API access, admin | Access and hosting sign-off | Before the pilot |

- **Senior owner:** the owner-CEO (name not given), owner of the budget; will fund one team on this problem for a year: yes, if the first thing works (operations director, 15 Oct 2026).
- **People plan:** dispatchers move from typing to approving, one hour of training in pilot week one, the champion dispatcher (the one already using a consumer chatbot) runs the pilot queue first.

Presentation milestones the plan should carry (each becomes an `adk-presenter` goal): proof-of-concept approval by the CEO on about 5 November 2026; proof-of-concept review with the CEO and the operations director after the four weeks; results review after production, when the 90-day measure is in.

## 7. Stall checks

| Cause | Answered where |
| --- | --- |
| Problem misframed | §1 two-voice statement; champion dispatcher agrees re-keying is the pain |
| No baseline or measure | §4 measure (minutes per emailed order) and baseline (estimate; two-week measurement is goal one) |
| Workflow not redesigned | §4 workflow before and after: re-keying removed, approval screen replaces the TMS form |
| No senior owner | §6 senior owner: owner-CEO, funds one team for a year if it works |
| No human-validation point | §4 workflow validation points: dispatcher on 100% before creation, dispatch review second |
| Data poor or inaccessible | §4 data register; gap: mailbox platform, retention and API access path are held by the external IT firm; the operations director asks them before the design |
| Cost not modelled per unit | §4 unit economics; gap: email share of orders and the cost ceiling; the operations director settles both before the CEO meeting |
| Risk controls absent | §4 permission scope and harms, three guardrails |
| Change and training ignored | §6 people plan, champion named |
| No feedback loop | §4 correction loop: edits stored, weekly review, prompt or evaluation case changes |
| Pilot not embedded | §4 embedding: live mailbox, real TMS orders, one dispatcher's queue from week one |
| Build or buy on pride | §4 build or buy; gap: whether the TMS vendor already sells email intake; the IT firm answers |
| Model churn breaks the target | §4 technology fit: the TMS write is ordinary code; acceptance is minutes per order and the corrected-order rate, re-run on any model swap |

## 8. Assumptions, open questions and what would change the choice

| Assumption or question | Why it changes the choice | How to settle it | Owner |
| --- | --- | --- | --- |
| The 4 minutes per order is an untimed estimate | If real intake is 1.5 minutes, O1's value drops below O3 | Measure for two weeks from TMS and mailbox timestamps | Operations director |
| The email share of 900 orders is unknown | Phone orders are out of scope; a small email share shrinks the prize | Count one week's mailbox | Operations director |
| The TMS API allows order creation, and the IT firm will grant access within the pilot | No API write, no use case; the fallback is a draft the dispatcher pastes | Ask the IT firm this week | Operations director |
| The TMS vendor may already sell email intake | A bought feature beats a four-week build | Ask the vendor through the IT firm | External IT firm |
| Past emails and their TMS orders are retained and can be paired | No pairs, no evaluation set; the pilot would start blind | Ask the IT firm for retention and sample 50 pairs | External IT firm |
| Customer order data may leave the firm through a model vendor | A residency or contract clause could block the cloud model | Check customer contracts and the IT firm's hosting terms | Operations director |
| Top customers would accept a structured order form | A process change removing the step for them is cheaper than any model | Ask the five largest customers | Operations director (parallel, not blocking) |

## 9. Next prompt

The filled prompt from the skill's handoff reference:

```text
/adk-system-designer Read docs/discovery/order-intake.md and design the first use case it selects (O1: extract order fields from emails in the shared mailbox and create the TMS order after one-click dispatcher approval). Treat its confirmed answers as settled; ask only what it leaves open. The outcome measure is dispatcher minutes per emailed order against about 4 minutes (reported estimate, unmeasured), with orders corrected at dispatch review and wrong deliveries as the guardrail. The sponsor is the operations director; the owner-CEO decides on the proof-of-concept go-ahead on 5 November 2026, so plan a presentation goal for it. Design only.
```
