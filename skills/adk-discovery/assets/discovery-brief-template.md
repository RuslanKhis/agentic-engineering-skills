# Discovery brief: <company or area>

Status: draft / reviewed with <who> on <date>
Entry: rough area ("<the sentence the user started with>") / no use case yet
Next step: `adk-system-designer` with the first use case below / a process
change owned by <role> / more discovery (<what is missing>)

Everything below is either what the user said, what a cited source says, or a
labelled assumption. Numbers carry their source and date.

## 1. Business and the outcome that matters

- **The problem in the sponsor's words:** <quote>
- **The problem in the builder's words:** <one sentence>; difference noted:
  <none / what>; frontline user who agrees: <role>
- **What the business sells and to whom:** <one or two sentences>
- **KPIs leadership watches:** <the two or three, with current values and
  sources where known>
- **Processes that move those KPIs:** <process, owner, volume per period>
- **Who decides what, and when:** <decision-maker; the next decision and its
  date, for example a proof-of-concept go-ahead on <date>>

## 2. The journey and where it breaks

One journey, told from the user's side, with the friction in it:

| Step | Who does it today | Volume | Where it fails or stalls | Evidence (source, date) |
| --- | --- | --- | --- | --- |

Signals used: <funnel counts, abandonment by step, time per step, rework,
hand-offs, tickets, call drivers, "ask a colleague" moments>. Say which are
measured and which are reported anecdotally.

## 3. Opportunity portfolio

Scores 1 to 5 are judgements made in the conversation and say whose. `Fit` is
one of `agent`, `llm`, `ml`, `rules`, `process`, `unclear` (the skill's
technology-fit reference). `Risk` 5 means money, messages to real people,
regulated decisions or irreversible effects without a review path. From the
project root, `python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief
docs/discovery/<topic>.md` adds up the scores; paste its ranking and findings
below the table.

| ID | Opportunity | Value (1-5) | Feasibility (1-5) | Data readiness (1-5) | Risk (1-5) | Fit | Measure | Baseline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | | | | | | | | |

Helper output (ranking and findings, pasted):

```text
```

Why the ranking came out this way, in three or four lines, and any
opportunity moved up or down for a reason the scores do not show (rerun
with `--pick <ID>` when the chosen one is not rank 1).

## 4. First use case

- **Chosen:** <O-ID and one sentence>; why it is first (narrow, measurable,
  low risk, data at hand) and what it deliberately leaves out.
- **Users:** <who uses it, how many, how often>
- **Technology fit:** <fit>, in the stakeholder sentence pattern from the
  technology-fit reference; the nearest alternative and why not.
- **Outcome measure:** <metric>, measured how, over what window, by whom.
- **Baseline:** <value and source and date>, or "unknown; the first goal is
  to measure the current journey for <period>"; measured on the scope the
  production rollout will reach (every queue, region or user group), or the
  brief says which part of that scope has no baseline yet.
- **Counter-metric:** <what must not get worse: refunds, support load,
  complaints, cycle time, cost per unit>.
- **Target and why it is plausible:** <target with units>; typical measured
  gains are under 10 percent of cost and under 5 percent of revenue, so a
  larger target names its mechanism (a step removed, not assisted) here.
- **How the measure reaches a KPI line:** <hours reassigned to what, cost per
  unit, revenue; who decided that conversion>.
- **Hypothesis chain:**

  ```text
  less effort to <step>
    → more <intermediate outcome>
    → <business outcome>, with <counter-metric> flat
  ```

  Every arrow is a hypothesis until measured.
- **Data register:**

  | Source | Owner | Access path | Freshness | Friction logged today? |
  | --- | --- | --- | --- | --- |

- **Workflow before and after:** the steps today, the steps after, and the
  steps removed (not only assisted); where a person validates each action
  and what share of outputs.
- **Permission scope and harms:** what the agent may read and change; the
  top three harms, each with a guardrail threshold; statements about
  policy, price or eligibility grounded in <source> or routed to a person.
- **Unit economics known so far:** expected volume per period, the cost
  ceiling the sponsor accepts, who pays the model bill after the pilot (the
  design estimates the cost itself).
- **Correction loop:** where a correction is captured, who reviews it, which
  artefact changes (prompt, rule, evaluation case, retrieval source); how
  people learn from the system and the system from people.
- **Embedding:** the pilot runs on live volume in <system of record> from
  week one for <queue or region>; "scaled" means <definition> and needs
  <governance sign-off>.
- **Build or buy:** <a partner already runs this process / build>, and why.
- **Cost of a wrong answer:** <what happens, who notices, how it is undone>;
  whether a person reviews before any effect.
- **Threshold sentences:** "If <metric> for <workflow> <drops below / rises
  above> <threshold>, we will <action>", for the outcome and the
  counter-metric.
- **Automate or augment:** <which, and why; what the people in the step keep>
- **What changes for the people in it:** <roles, training, the redesigned
  workflow, not an overlay on the old one>
- **Success in 90 days looks like:** <one sentence a stakeholder would sign>,
  followed by one paragraph describing the improved journey in the
  customer's words, as a future press release.

## 5. Constraints and facts for the designer

| Scope-gate question | Answer (confirmed / assumed) |
| --- | --- |
| Deadline for the first useful version, and what follows | |
| People, hours, familiarity with ADK and GCP (often "unknown: ask") | |
| Money for models and cloud | |
| Who uses or judges it, and what they read | |
| Data touched and effects allowed | |
| Who must approve the next step, and when | |

Known systems, platforms, identity, data residency, regulation, brand or
legal constraints: <one line each>.

## 6. Stakeholders and the decision calendar

| Stakeholder | Cares about | Decides | When |
| --- | --- | --- | --- |

- **Decider:** <the one person who decides the next step>; sponsor if
  different: <role>.
- **Senior owner:** <name, role, budget line>; will fund one team on this
  problem for a year: <yes / no / unknown>.
- **People plan:** who changes what they do, what training, when; the
  champion among the staff already using AI unofficially: <role>.
- **Publicity:** who approves what may be said outside the company, and the
  Google Cloud relationship (direct customer, through a partner or IT firm,
  startup program), for a later case study.

Presentation milestones the plan should carry (each becomes an
`adk-presenter` goal): <proof-of-concept approval on <date>; production
decision after <event>; results review>.

## 7. Stall checks

One row per known reason AI projects stall (the skill's reference lists the
evidence); each cites the section that answers it or says `gap: <what is
missing and who settles it>`.

| Cause | Answered where |
| --- | --- |
| Problem misframed | §1 two-voice statement |
| No baseline or measure | §4 measure and baseline |
| Workflow not redesigned | §4 workflow before and after |
| No senior owner | §6 senior owner |
| No human-validation point | §4 workflow validation points |
| Data poor or inaccessible | §4 data register |
| Cost not modelled per unit | §4 unit economics |
| Risk controls absent | §4 permission scope and harms |
| Change and training ignored | §6 people plan |
| No feedback loop | §4 correction loop |
| Pilot not embedded | §4 embedding |
| Build or buy on pride | §4 build or buy |
| Model churn breaks the target | §4 technology fit (rules for deterministic steps); outcome-defined measure |

## 8. Assumptions, open questions and what would change the choice

| Assumption or question | Why it changes the choice | How to settle it | Owner |
| --- | --- | --- | --- |

## 9. Next prompt

The filled prompt from the skill's handoff reference:

```text
/adk-system-designer Read docs/discovery/<topic>.md and design the first use
case it selects (<O-ID>: <one sentence>). Treat its confirmed answers as
settled; ask only what it leaves open. The outcome measure is <metric>
against <baseline>, with <counter-metric> as the guardrail. The sponsor is
<role>; <decider> decides on <decision> on <date>, so plan a presentation
goal for it. Design only.
```
