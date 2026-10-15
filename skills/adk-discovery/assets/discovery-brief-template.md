# Discovery brief: <company or area>

Status: draft / reviewed with <who> on <date>
Entry: rough area ("<the sentence the user started with>") / no use case yet
Next step: `adk-system-designer` with the first use case below / a process
change owned by <role> / more discovery (<what is missing>)

Everything below is either what the user said, what a cited source says, or a
labelled assumption. Numbers carry their source and date.

## 1. Business and the outcome that matters

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
  to measure the current journey for <period>".
- **Counter-metric:** <what must not get worse: refunds, support load,
  complaints, cycle time, cost per unit>.
- **Hypothesis chain:**

  ```text
  less effort to <step>
    → more <intermediate outcome>
    → <business outcome>, with <counter-metric> flat
  ```

  Every arrow is a hypothesis until measured.
- **Systems that own the facts:** <catalogue, pricing, orders, CRM, rights>,
  and who can grant access.
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

Presentation milestones the plan should carry (each becomes an
`adk-presenter` goal): <proof-of-concept approval on <date>; production
decision after <event>; results review>.

## 7. Assumptions, open questions and what would change the choice

| Assumption or question | Why it changes the choice | How to settle it | Owner |
| --- | --- | --- | --- |

## 8. Next prompt

The filled prompt from the skill's handoff reference:

```text
/adk-system-designer Read docs/discovery/<topic>.md and design the first use
case it selects (<O-ID>: <one sentence>). Treat its confirmed answers as
settled; ask only what it leaves open. The outcome measure is <metric>
against <baseline>, with <counter-metric> as the guardrail. The sponsor is
<role>; <decider> decides on <decision> on <date>, so plan a presentation
goal for it. Design only.
```
