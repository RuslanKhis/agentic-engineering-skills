# Provenance and evidence limits

This skill translates Chapter 7, *Testing Your Agent — Evaluating a Probabilistic System*, from *Agentic Engineering* into an independent evaluation workflow.

The installed skill does not require the manuscript or companion repository. Origin file names below identify the evidence behind a rule; they are not paths that must exist in a user's project. Apply the rule to the target's own architecture and validate the change there.

## Source identity

The source was reopened at revision `c909d7e5d285ae582abb3899bbe162fa55f075dd`. All 38 files listed in the retained final application/test manifest matched their recorded SHA-256 values when preparing this skill. Manifest digest: `e53f9692b04e78c33a0a2a1ae12c0a9fb7bdcbcfedd1ae61344c3b6d49bc6d02`. The final receipt renderer digest is `95036f2c370ddbc4c8addcc73d2f50afb158082a4c79fe63b63187e5fcda418c`.

The relevant origin materials are the updated chapter dated 15 September 2026, `INDEPENDENT_AUDIT_2026-09-13.md`, `REMEDIATION_2026-09-13.md`, and their retained synthetic evidence. Hash agreement connects current source to the recorded files; it is not a new execution of those files. Exact historical runtime versions are in [compatibility.md](compatibility.md). Validation of this newly packaged skill is separate and recorded in [validation.md](validation.md).

## What was actually exercised

| Evidence class | Observed scope | What it does not prove |
| --- | --- | --- |
| Historical live calls | CLI and local ADK Web with real Vertex inference; fixed evaluations; a managed simulated conversation; conformance recording. Business tools used an in-memory synthetic backend. | Deployed hosting, real customer authentication, real refunds or all future model behaviour. |
| Final offline suite | 64 tests passed with two live tests deselected. Tests covered business rules, actual Runner and HTTP routes, callback state, schemas, setup branches and process deadlines. | That scripted model choices predict live model decisions. |
| Environment Simulation | A fixed injected 503 bypassed the actual lookup tool; a scripted model supplied the following answer through the real Runner. | A real HTTP outage or a live model's response to it. Real backend-error handling was tested separately. |
| Source-change equivalence | After the final batch-receipt correction, 22 captured agent turns and 28 recorded model responses were replayed through real Runner/tools with networking denied. | Fresh inference on the final source or exhaustive equivalence for unseen decisions. |
| Final browser/conformance | Browser and conformance runs used final source. Guarded offline conformance replay executed one case successfully. | Token-streaming latency, a general SLA, or automatic network isolation in ordinary replay. |
| Not exercised live | Fresh API activation, IAM changes, deployment, durable remote mutations and unknown-write recovery. Missing/enable/repeat/partial-error setup branches had offline subprocess tests. | Permission to perform those operations in another project. |

Fixed CSV and managed evaluation completed before the last batch-receipt correction. They were not repeated to obtain another live pass; captured-decision equivalence supplied the later offline evidence. Keep this distinction whenever using the historical results.

## Rule-to-evidence map

All source names in this table are within the origin's Chapter 7 directory.

| Reusable rule | Origin implementation/test or production principle |
| --- | --- |
| Use the real orchestration with only external boundaries substituted | `tests/fakes/scripted_llm.py`; `tests/integration/test_scripted_agent.py`; `test_web_app.py`. The scripted model records requests and fails if an unexpected extra generation occurs. |
| Enforce trusted identity and current-turn prerequisites below the model | `support_agent/tools.py`; `tests/unit/test_tools.py`; `test_prior_turn_lookup_cannot_authorise_a_later_refund`. Backend ownership checks remain independent. The example's demo identity fallback must not be copied into production. |
| Consider application-rendered transactional confirmations when appropriate | `support_agent/responses.py`; `tests/integration/test_terminal_responses.py`; `tests/unit/test_terminal_callback.py`. Real tool results supply dynamic fields; stale or forged conversation content supplies no receipt. This is an optional design for factual outcomes, not a universal ban on model-written answers. |
| Preserve committed effects when a later action fails | `test_completed_refund_survives_later_tool_results_in_same_batch` and `test_completed_refund_survives_lookup_and_creation_for_another_order`. A rejected duplicate cannot turn an existing request into a false no-write claim. |
| Check individual rows and business outcomes, not exit code alone | Baseline CSV: 20/20 trajectories passed but two response rows scored 0.28 and 0.2127659574 against threshold 0.3; the case average 0.3235531915 passed. The answers still refused safely. Later receipt rendering passed all 40 rows without changing criteria; that is application-output consistency, not better model paraphrasing. |
| Make result coverage and thresholds an explicit, repeatable contract | The skill's new `scripts/check_eval_results.py` implements this lesson; it was not an existing companion helper. Its 15 CLI tests cover incomplete/extra rows, invalid data, inconsistent status/score, secrecy and repeatability. Re-reading the retained CSVs rejected the baseline's two failed rows and accepted all 40 remediation rows. This checks metric rows, not independent trial identities. |
| Separate observed any/all success from reliability guarantees | `support_agent/reliability.py` and `tests/unit/test_reliability.py`. The functions consume per-case booleans; they do not identify trials in arbitrary CSVs or establish independent future probabilities. |
| Identify business-data lifetime explicitly | `tests/conftest.py` resets per pytest test; `support_agent/eval_runner.py` resets once before repeated evaluator cases. Separate sessions can share the same idempotent store. |
| Bound blocking work outside the blocked event loop | `support_agent/eval_runner.py`; `tests/integration/test_eval_deadline.py`. The regression reached synchronous grading before the parent terminated and reaped the worker. Adapt process-group handling to the target platform. |
| Resolve ADC/key conflicts without overwriting secrets | `scripts/setup_vertex.py`; `tests/unit/test_setup_vertex.py`; historical ADC preflight/live commands. Existing keys were preserved while command-scoped overrides selected ADC. Unknown activation completion was an offline reconciliation case, not a successful live activation claim. |
| Review replay baselines and verify an executed case | Conformance specification and retained recording/replay validation. The final eligible recording had two model and two tool entries; the callback supplied final prose. Recorded outputs do not establish the truth of current tool results. |
| Calibrate judges, retain holdouts, compare slices, minimise production evidence and reconcile unknown remote mutations | Clearly stated production principles in the chapter. The companion does not implement a complete rubric-calibration service, holdout programme, production monitoring system or remote-write reconciliation protocol. Validate these adaptations separately. |

Do not import the example's fixture IDs, model/region choices, call counts, lexical thresholds or local storage lifetime as universal requirements. The durable lesson is to choose a meaningful boundary, preserve failed and incomplete evidence, and state whether validation used real services, substituted boundaries or inspection alone.
