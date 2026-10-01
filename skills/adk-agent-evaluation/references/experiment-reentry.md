# Re-enter an experiment after structural failures

Read when recurring failures from the same family make another broad paid run
unlikely to distinguish hypotheses. Prepare this short record during offline
diagnosis; it is not a new approval step for local fixes or work already covered
by valid authorization. There is no universal repeat threshold or extra allowance.

Use [progressive validation](progressive-validation.md) for scheduling the repair
and targeted continuation; this record governs re-entry to a broader experiment.

## Diagnose before another cohort

Retain the first reached failure and all later known blockers. A checker that
stops at missing coverage may conceal unsupported evidence or an impossible
outcome representation. Repairing that first predicate is not evidence that the
remaining task is achievable.

| Failure family | Discriminating offline check |
| --- | --- |
| Transport/schema incompatibility | Send the actual serialized request to a controlled rejecting transport; keep route and schema identity with the result. |
| Unrepresentable outcome | Pass a truthful reference with nondecisive issues through the real schema/checker; reject invented claim associations. |
| Copying/coverage failure | Test server-owned identities/slots, duplicate/missing slots and replay after a draft revision. |
| Retrieval miss | Inspect document and operative-section coverage, extraction state, query misses and unviewed visuals separately. |
| Semantic error | Judge fixed complete evidence against reviewed positive, negative and borderline expectations. |

Choose the smallest check that separates the proposed explanation from plausible
alternatives. A model's support label is a judgment to evaluate, not an independent
oracle. An accepted reference must preserve necessary controls, contradictions and
unsupported material issues; reducing rejection alone is not a repair.

## Re-entry record

Copy this into the project's existing experiment record and fill only the fields
relevant to the proposed work. Keep historical attempts immutable.

```text
Experiment/revision and source/config/dataset hashes:
Prior attempt IDs; first reached failure; later known blockers:
Failure classification and supporting evidence:
Retained minimal reproducer:
Honest passing reference through actual schema/checker/runtime:
Negative controls (false association, missing safeguard, unsupported evidence):
Changed boundary; offline regression commands/results; remaining unknowns:
New hypothesis; observation that would distinguish it from alternatives:
Purpose of each phase (diagnostic or release evidence):
Exact route/identity/models, inputs and fixed case/trial IDs:
Phase admission and stop/continue rules declared before execution:
Submissions, actual-send attempts (including retries), output/time limits:
Cost estimate, allowance and existing authorization scope/reference:
Shared durable ledger, reservation/settlement and evidence destination:
```

A staged plan may reserve one diagnostic canary, followed by a fixed cohort only
if its declared gate passes. Its cases, allocation and transition rule belong in
the plan before approval. Reuse existing approval when that plan is already within
scope. Keep the original rules for an approved fixed cohort: do not add early stops,
replace failed cases or introduce retries after seeing its outcomes. A required
safety/budget stop still applies; retain unrun cases as missing evidence.

## Accounting and interpretation

Use an append-only attempt record or the existing durable ledger:

```text
campaign / phase / case / trial / logical-call / actual-send IDs
route + source/config/schema hashes; reserved allowance; dispatch timestamp
terminal state: completed | failed | uncertain | not dispatched
authoritative usage/receipt ID; settled cost; unresolved reservation/estimate
first failure; retained artifact; diagnostic/release/replay classification
```

Reserve before dispatch across workers/restarts; count retries as actual sends.
Deduplicate authoritative usage receipts. A local deadline without a receipt leaves
usage/cost uncertain, not zero; a conservative reservation is not settled billing.
Record later reconciliation as a linked event without rewriting the original run.

Report attempted, completed, published, substantively scored and missing cases
separately, keeping the fixed denominator. Zero publications does not mean every
unscored draft was a wrong decision. Replaying a retained failure after repair tests
the changed application boundary; the original failed trial remains failed. A
passing canary establishes its observed contract, not cohort quality.
