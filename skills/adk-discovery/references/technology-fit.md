# Technology fit: agent, LLM call, classical ML, rules, or a process change

Read when an opportunity is about to get its `Fit` value in the portfolio, and
again before the handoff, because the designer inherits the choice. The vendor
guides and benchmarks behind this reference (sources and dates in the
repository's research note `docs/research/technology-fit-triage.md`) agree on
one order: the simplest mechanism that meets the need, with probabilistic
parts only where deterministic ones cannot do the job. Treat the table as a
checklist that makes the choice defensible, not as a predictor of success.
A hybrid takes the fit of its model-driven step: `llm` when the model makes
one bounded judgement and code does the rest, `agent` when the model chooses
the steps or the tools.

## Ask in order

Record each answer per candidate; the answers are the evidence for the `Fit`
column and the one-paragraph explanation to the stakeholder.

1. **What does the current process achieve, and is it optimised?** If a
   clearer rule, a form or a staffing change meets the goal, the fit is
   `process` and no software is proposed. Google's first rule of ML is to
   launch without ML and put metrics in place first.
2. **Structured records or unstructured language?** Structured with known
   rules: `rules`. Structured with unknown rules and labelled outcomes in
   volume (thousands of rows): `ml`. Free text, documents, conversation: an
   LLM candidate.
3. **Is the rule set known and stable?** Known and stable: `rules`, or a
   workflow with a fixed step order. Known but unwieldy to maintain
   (OpenAI's second criterion): `ml` or `llm`.
4. **What is the output?** A number, class, probability or ranking: `ml`. A
   fixed transformation: `rules`. A bounded judgment over text with a schema
   and a small action set: `llm` (one call, no tool loop). A sequence of
   actions across systems whose length and order depend on what each step
   finds: `agent`. Anthropic's test is exact: an agent is for the case where
   you cannot hardcode the path.
5. **What does an error cost, and can someone review it?** High cost and no
   review path: do not automate; PAIR lists "cost of errors outweighs the
   benefits", "predictability matters" and "people told you they do not
   want it automated" as stop conditions. High cost with review: the model
   interprets and a person or code decides.
6. **Volume and latency?** High volume and delay-tolerant: batch pricing or a
   trained model. Interactive and high volume: the per-call cost and latency
   are measured before the choice is final; none of the sources quantify
   them for you.
7. **Determinism and audit?** Regulated or contestable decisions are made by
   code or a reviewable model; the LLM may prepare inputs and drafts only.

## Triage table

| Criterion | `rules` (script, workflow) | `ml` (classical) | `llm` (single call) | `agent` | `process` (no software) |
| --- | --- | --- | --- | --- | --- |
| Input | Structured, known fields | Structured, many examples | Unstructured language | Unstructured plus external systems | Any |
| Rules | Known and stable | Unknown but learnable | Known in prose, hard to encode | Unwieldy, context-dependent | Unclear or disputed |
| Labelled history | Not needed | Thousands of rows | Dozens, for evaluation | Dozens of end-to-end cases | Not needed |
| Output | Fixed transformation | Number, class, probability, rank | Bounded judgment with a schema | Actions and a result | A decision a person owns |
| Path | Fixed | Fixed | One step | Unknowable in advance | Variable |
| Error cost | Any, if tested | Must be measurable | Needs review or low cost | Needs guardrails and review | Required when errors are intolerable |
| Determinism and audit | Full | Reproducible per model version | Partial; log prompt and output | Lowest; log every tool call | Full |
| Recurring cost | Compute only | Inference plus retraining | Per token per call | Per token per step, many steps | Staff time |
| Who maintains | Developers | ML engineers, data owners | Prompt and eval owners; vendor model migration | Same plus tool and guardrail owners | Process owner |
| Example | Tax calculation, format conversion | Churn score, demand forecast | Route an email to one of eight queues | Investigate a claim across three systems and draft a decision | Approve refunds above a threshold |

The benchmarks matter for the `ml` column: tree ensembles remain
state-of-the-art on medium tabular data, removing the LLM from an LLM
time-series forecaster does not hurt it, and fine-tuned small encoders beat
LLMs on pattern-driven text classification with a full labelled set. With
labelled outcomes in volume over tables, series or pattern-driven text,
default to `ml` and leave the LLM for the residue that needs reading or world
knowledge.

## Mistakes to name when you see them

| Mistake | Tell | Better choice |
| --- | --- | --- |
| LLM doing arithmetic, lookups or exact matching | "Calculate", "look up the ID", "compare codes" in the intended prompt | A function tool or plain code; the model only decides when to call it |
| Agent where a workflow suffices | The step list can be written down and does not change | A sequential or parallel workflow, or ordinary code |
| Classical ML on forty labelled rows | Tiny training set, or no outcome column at all | A heuristic, or an LLM with in-context examples, plus a labelling plan |
| LLM forecasting or scoring tabular data | The input is a table or a series with history | Gradient-boosted trees or a conventional forecaster |
| Chatbot as the default interface | A form, a button or a batch job already does the job | Keep the interface; put the model behind it, or leave it out |

## Hybrid shapes worth proposing

- **LLM interprets, code decides.** The model extracts fields into a schema;
  deterministic code applies the policy and produces the effect.
- **ML model as a tool.** A trained classifier or forecaster behind an ADK
  function tool; the agent chooses when to call it and explains the result.
- **Rules first, LLM for the residue.** Settle what a rule settles; send
  only the ambiguous cases to the model.
- **Workflow outside, agent inside.** Fixed orchestration with one
  model-driven step where judgment is needed; ADK's workflow agents run
  without consulting a model for the orchestration.

Microsoft's per-step question is the cleanest way to draw a hybrid: for each
step, who decides what happens next, the model, the code or a person?

## Ownership, stated with the choice

An LLM component carries a per-call cost and a vendor-set model migration
cadence; a trained model carries a retraining cadence the team sets from its
own drift measurements; a script carries only rule changes. The brief names
the call volume, whether the work is interactive or batch, and the role that
owns migration, retraining or rule changes; the designer estimates the cost.
Evaluation needs a labelled set in every column.

## Explaining the choice to a business stakeholder

One sentence per slot, each mapping to a row of the table, so the explanation
and the triage are the same artefact:

> You asked whether AI can handle [process]. The input is [structured records
> / free-text documents], the rules are [stable / known but hard to keep
> current / dependent on context], and we [do / do not] have [N] past
> outcomes to learn from. That points to [a script / a predictive model / a
> language model with a fixed output / an agent that works through the steps
> itself]. We chose it over [nearest alternative] because [one observable
> reason]. The error cost is [low / high], so [a person reviews every output /
> the system decides only within these limits]. [Role] keeps it current,
> including [rule changes / retraining / model upgrades the vendor requires];
> the design will state what it costs to run.

Sources were read on 15 October 2026 and are listed with URLs in the
repository's research note; re-read a vendor page before quoting a price,
a lifecycle promise or a product capability in a brief.
