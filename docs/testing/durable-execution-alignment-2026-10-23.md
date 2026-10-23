# Temporal and DBOS ADK integrations alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/durable-execution-comparison-2026-10-23.md).
In the repository: the resume-versus-durable-execution section in the
workflow skill's runtime reference with both engines' facts and the choice
order (plus LangGraph's four rules for code around a pause); the three-way
decision in the designer's design-decisions reference; why the key survives
an engine in the safe-API skill. After the trial: routing rows in the
engineer's table and the workflow skill's mode table that name durable
execution, worker restarts and pauses of days; the compatibility gate for an
engine whose declared ADK floor predates the project's pin; cross-references
between the three references that each hold a third of the decision; a
verdict for the persistent-store-plus-days case in the guardrails skill with
the public tool-context accessors. **One scenario case**
(`workflow-durable-refund-resume-or-engine`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK, Temporal or DBOS installed, on a synthetic project, without the
expected answers; interrupted once by a usage limit and resumed.

### Workflow: a refund workflow that waits days and re-issued a refund after a restart

The project: an ADK 2.12 refund tool against a payments API with
idempotency keys, Postgres available, no Temporal cluster, a manager
approval that can take days, and a worker restart that duplicated a refund.

What the agent did: decided that resume is not enough and wrote the design
note; built a Postgres-shaped durable operation ledger (SQLite offline over
the same schema) with one idempotency key per operation, explicit states,
approval as a ledger transition and reconciliation by key before any
re-send; renamed the model-facing tool so its name no longer claims an
effect; planned DBOS behind a compatibility gate because its declared ADK
floor predates 2.x; wrote the requested kill-after-the-write tests in both
positions plus the negative control on keyless at-least-once resume (two
effects), 18 offline tests run on the pin-meeting interpreter, 3 SDK and
DBOS tests reported as not run.

Ease rating: **3 of 5**. Once found, the runtime section answered the
request almost verbatim; finding it needed a search because no routing row
named the decision.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| No routing row named durable execution, worker restarts or pauses of days | Both tables now do |
| Three skills each held a third of the decision without naming the others | Each now names its neighbours |
| DBOS recommended for Postgres with its ADK floor unverified on 2.x and "keep the pins" | The compatibility-gate rule |
| The persistent-store-plus-days verdict was left to the reader; tool-context accessors unknown | The verdict and `tool_context.user_id` / `function_call_id` stated |
| The interpreter rule sits in a long paragraph; the workflow skill does not restate the helper fallback | Left: the rule is now also cross-referenced from two specialists; the paragraph's placement is a Phase D question |

## What this does not establish

No engine ran; the ledger was exercised on SQLite, not Postgres; the SDK
confirmation boundary test did not run.
