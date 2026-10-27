# tau2-bench alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/tau2-bench-comparison-2026-10-22.md).
In the repository: the unbiased pass^k helper rules in the evaluation
skill's result-auditing reference; a new section "Grade the end state, not
the path" in its evaluation-design reference with the multiplicative,
premature-stop and missing-criterion rules; the pointer from its
compatibility table; the comparability precedent in the release skill's
versioning reference; provenance in the evaluation skill. After the trial
(23 October): a mode-table row for the end-state method, the
effective-mutation comparison beside the state hash (a reversible detour
nets to the same state), the release skill's flakiness controls and gate
policy pointing at the end-state grader, the provisional gate's third exit
outcome, the trial-record shape, the verified google-genai selector
precedence, and the tools-as-a-seam rule. No benchmark data; no helper
changed. **One scenario case**
(`evaluation-repeated-trials-pass-hat-k-and-end-state`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the [testing log](index.md) entry for this date.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK installed, on a synthetic project, without the expected answers;
interrupted once by a usage limit and resumed.

### Evaluation and release: a reliability gate for flaky booking evals

The project: an ADK 2.12 booking agent whose nightly `adk eval` passed some
nights and failed others because the model chose a different but correct
order of calls; an in-memory backend fixture; two cases.

What the agent did: an end-state grader that replays the case's reference
trajectory on a fresh backend and compares the canonical state and the
multiset of effective mutations, with order graded only when a case lists
it; a reliability module computing the unbiased pass^k per case with
infrastructure errors kept in the report and out of the denominator, a gate
with distinct exit codes for pass, fail, not run and provisional; a trial
runner written to the 2.12.0 signatures and reported as not run; a corrected
fixture (the reference cancel had nothing to cancel); 24 offline tests run
and one Runner test skipped; a two-tier workflow; the retired model id
flagged and left for a release decision.

Ease rating: **3 of 5**. The decisive guidance existed and was precise, but
sat across six references in two skills with the end-state section
reachable only through a cross-link.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The mode table never named the end-state method | A mode-table row routes the flaky-order problem to it |
| The release skill's flakiness controls and gate policy stopped at `match_type` | Both now point at the end-state grader when the requirement is an outcome |
| "Any extra mutation fails" was false for a reversible detour | The section now compares effective mutations beside the state hash |
| Report-only versus blocking left the provisional exit code to invention | The gate policy names a third outcome mapped to a warning, never promote |
| No shape for the trial record | A minimum row shape in result auditing |
| `GOOGLE_GENAI_USE_ENTERPRISE` versus `GOOGLE_GENAI_USE_VERTEXAI` unverified | Both honoured on google-genai 2.32.0, enterprise wins on conflict, from the installed client |
| Tools and agent in one module blocked replay | Tools as a seam, in deterministic tests |
| A pass^k helper script; the workflow asset's 2.8.0 baseline; the engineer's ticket protocol length | Left: the helper is owed with tests, the asset's baseline is the toolkit's, the protocol's placement is a Phase D question |

## What this does not establish

The Runner tests and the trial runner did not run; the pinned interpreter
and test-runner combination was not exercised.
