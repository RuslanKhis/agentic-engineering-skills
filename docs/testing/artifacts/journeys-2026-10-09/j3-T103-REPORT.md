# T-103 report: gemini-2.5-pro is retiring (reconstructed)

> Reconstructed from the working tree after the trial was interrupted by a usage limit before it wrote its own report. The live friction log and command transcript were lost. `support_agent/models.py` and `tests/test_release_contract.py` reference a `PROMPT_CHANGELOG.md` that was never written, so the trial stopped mid-release-record.

Skill root for pointers: `/Users/ruslankhissamiyev/Documents/Coding Projects/skills/agentic-engineering-skills/skills/<name>/`.

## 1. Specialist selection (inferred)

**Primary:** `adk-release-engineering`, modes (c) model migration, then (b) eval gate in CI, with (a) versioning started (`SKILL.md:36-38`, composed as `:43`: "A deprecation notice is (c) then (d) then a changelog row in (a)"). **Secondary:** `adk-model-and-output-contracts` for the Gemini 3 settings (`SKILL.md:51`: `thinking_level`, temperature left at 1.0) and its lifecycle table (`assets/model-lifecycle-*.json`, which names `gemini-3.8-flash` as the 2.5-pro replacement).

Evidence: the CI header says "Adapted from adk-release-engineering/assets/eval-gate.github-actions.yml". There are three tiers (deterministic, live on label/merge, judge nightly), `check_eval_results.py` as the strict gate, "NOT RUN blocks", the judge pinned with `num_samples=5`, `release/inventory-rc-0001.json` from `inventory_release_refs.py`, and per-case freshness and drift metadata (`SKILL.md:55`).

**Routing row:** `adk-engineer/SKILL.md:66`: "Model deprecation notices ... eval gates in CI ... | `adk-release-engineering`". It matches both halves of the ticket (retirement, and "CI only runs unit tests"). Row `:63` (model selection, thinking or temperature settings) is the secondary.

## 2. Changes

```
 .github_workflows_ci.yml | 181 +++++++++++++++++-  (8-line workflow became a 3-tier gate)
 pyproject.toml           |  17 +++              (test extra, pytest markers, default deselects paid tiers)
 support_agent/agent.py   |  17 +++--
 3 files changed, 206 insertions(+), 9 deletions(-)
```
Untracked (wc -l):
```
 support_agent/models.py              32   AGENT_MODEL=gemini-3.8-flash, PREVIOUS_AGENT_MODEL, JUDGE_MODEL, JUDGE_NUM_SAMPLES
 evals/ci/support_dev.evalset.json   131   6 single-turn cases (routing, T-101/T-105 regressions, no fabricated IDs)
 evals/ci/cases.meta.json             14   ownership, freshness, drift mode; reviewer/reviewed all null
 evals/ci/test_config.json             6   tool_trajectory_avg_score + response_match_score only
 evals/ci/ci-expectations.json        16   strict-checker expectations, 3 runs per case
 evals/judge/test_config.json         16   final_response_match_v2, hallucinations_v1, safety_v1; judge pinned
 release/inventory-rc-0001.json      369   inventory helper output (partial: true, see F2)
 tests/test_release_contract.py      141   stdlib/ast release-contract checks (9 tests)
 tests/test_request_contract.py       93   ADK-dependent request/pin checks (importorskip)
 tests/eval/test_ci_gate.py           50   live tier 2 (RUN_LIVE_EVAL=1, cost ceiling)
 tests/eval/test_nightly_judge.py     49   judge tier 3 (RUN_JUDGE_EVAL=1)
```
`agent.py`: every `LlmAgent` uses `AGENT_MODEL`. In `triage_agent`, `thinking_budget=2048` became `thinking_level="low"` and `temperature=0.2` was removed. The root's `temperature=0.2` config was dropped.

## 3. Completeness against the ticket

| Requirement | State |
| --- | --- |
| Move off gemini-2.5-pro before 2026-10-20 | **Done in code**: a single pin `gemini-3.8-flash`, which is stable with no retirement in the bundled lifecycle table. |
| "Without silently dropping quality" | **Infrastructure only, no evidence.** No side-by-side run, no baseline (2.5-pro) numbers, the `response_match_score` threshold of 0.3 is labelled "a starting value, not a measurement", all cases are `reviewed: null`, the holdout is "not yet created", and no go/no-go record from `assets/model-upgrade-checklist.md` exists. |
| CI only runs unit tests | **Done in YAML, untested.** The three tiers are defined, but `SKILLS_REF` is a `<PIN: ...>` placeholder, the `eval` environment and `EVAL_GOOGLE_API_KEY` secret do not exist, and the deterministic job would fail as written (F2). |
| Release record (`PROMPT_CHANGELOG.md`, `release/manifest.json`) | **Missing.** Both are referenced by tests but were not written. |
| Rollout / rollback plan (mode d) | **Missing.** |

Validation run during reconstruction (system Python 3.9.13, no ADK):

```
python3 -m pytest -q -p no:cacheprovider tests/test_release_contract.py
7 passed, 2 failed
  FAILED test_no_model_literal_or_thinking_budget_in_agent_module   (the trial's own comment in agent.py contains "thinking_budget")
  FAILED test_changelog_newest_row_is_complete                       (PROMPT_CHANGELOG.md does not exist)
python3 -m pytest -q tests  ->  collection error: tests/test_tools.py imports support_agent -> google.adk (baseline problem)
tests/test_request_contract.py: skipped (importorskip google.adk); tests/eval/*: deselected by addopts
```

## 4. Quality notes against `adk-release-engineering/SKILL.md`

1. **Pins over aliases; the judge is a pinned dependency (`SKILL.md:48-49`): followed.** Stable IDs live in one module and the judge is pinned with `num_samples`. A test asserts no alias suffixes and no retiring IDs.
2. **Migrate the judge separately (`references/model-migration.md:45-50`): not followed.** The agent model and the judge (from the 2.8.0 default `gemini-2.5-flash` to `gemini-3.8-flash`) change in the same release, and the judge is the same model as the agent. There was no prior judge baseline, which softens the problem but is not stated.
3. **Gate must fail by exit code; NOT RUN counts as failure (`SKILL.md:50`, `:37`): followed** carefully. The workflow avoids `adk eval`, uses pytest + `AgentEvaluator` + the strict CSV checker, and fails on a missing or empty CSV.
4. **On Gemini 3 use `thinking_level`, leave temperature at 1.0 (`adk-model-and-output-contracts/SKILL.md:51`; `adk-release-engineering/SKILL.md:52`): followed.**
5. **Validation (`SKILL.md:63`): manifest round trip, changelog row, rollback rehearsal: not reached.**

## 5. Friction the artefacts reveal

- **F1. The release unit's change record was never reached.** The trial spent its budget on a 181-line CI workflow, 6 eval cases with metadata, and two test tiers before writing `PROMPT_CHANGELOG.md` (`SKILL.md:36`) or a manifest. Modes (c)+(b)+(a) composed per `SKILL.md:43` are a lot of artefacts for one ticket, and the skill gives no "minimum viable migration" ordering, for example pin, changelog row, then gate.
- **F2. The shipped CI asset breaks itself.** `assets/eval-gate.github-actions.yml:65` runs `inventory_release_refs.py --project . --dry-run > inventory.json` inside the scanned project. The shell creates the empty file first, the scanner reads it, records `malformed_file` (`scripts/inventory_release_refs.py:444-445`), sets `partial: true`, and exits 1. Reproduced during reconstruction on a scratch copy: `exit 1`, `issues: [{'path': 'inventory.json', 'reason': 'malformed_file'}]`. The trial copied the pattern into its workflow (whose step also fails on `partial`). Its own committed `release/inventory-rc-0001.json` shows the same `malformed_file` self-scan.
- **F3. The inventory helper penalises the pattern the skill recommends.** Moving pins to one constants module (`SKILL.md:47`, "one release unit") makes every `model=AGENT_MODEL` a `model_dynamic` signal, because `inventory_release_refs.py:234-237` resolves only same-module literals. It also reports the test file's retiring-ID list as `model_pinned` for `gemini-2.5-flash` and `gemini-2.5-flash-lite`.
- **F4. External repo checkout in CI.** The asset expects the skills repo vendored or checked out (`assets/eval-gate.github-actions.yml:43`, `<PATH: ...>`), and the trial left `SKILLS_REF: "<PIN: commit SHA ...>"`. A maintainer must choose between vendoring two helper scripts and pinning a third-party repo. The skill does not recommend either.
- **F5. Quality claims need paid runs that are approval-gated (`SKILL.md:59`).** The ticket's core requirement ("without silently dropping quality") cannot be met offline. The skill says so, but it gives no offline proxy (for example, request-capture diffs of tool declarations under the new model config) to show progress.
- **F6. SDK-free testing again.** `tests/test_release_contract.py` re-implements AST parsing of `agent.py` because `support_agent/__init__.py` imports ADK. The baseline `tests/test_tools.py` still cannot be collected.
- **F7. A self-inflicted test failure from an explanatory comment.** The agent's comment "Gemini 3: thinking_level replaces thinking_budget" trips its own substring test. This is minor, but it shows the absence of any run of the new test file before the interruption.

## 6. Note on lost evidence

The original agent's friction log, the order in which it read references (`model-migration.md`, `ci-eval-gates.md`, `versioning.md`), and the helper exit codes were lost with the interruption. The `release/inventory-rc-0001.json` artefact is the only command output that survives.
