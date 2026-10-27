# Plan: move off gemini-2.5-pro before 2026-11-17

Opened 2026-10-27. Evidence labels: offline / local / live / release; `not run` means not run.
Nothing below was executed against a model, cloud project or network in the session that wrote it.

## Questions nobody could answer, and the assumption used

| Question | Assumption |
| --- | --- |
| The forwarded notice says retirement is 2026-11-17. Google's Vertex page (as captured in the repo's lifecycle snapshot, read 2026-10-08, updated 2026-10-21 per the skill) lists gemini-2.5-pro as retired on Vertex on 2026-10-20. Which is right for this project? | Treat 2026-11-17 as the hard deadline, but **today check that production still answers** (a failing request means the deadline already passed). Re-read the Vertex model-versions page for the real date. |
| Which model replaces it? | Primary candidate `gemini-3.8-flash` (stable, listed replacement, no retirement date announced). Second candidate `gemini-3.5-flash` for the side-by-side. Both are Flash, not Pro; this is a tier change on the refund path. |
| Who approves traffic and pays for eval runs? | Sam (sender of the notice) approves go/no-go; spend is approved per run, see the ceiling below. |
| Is the Gemini API or Vertex used? | Vertex (Cloud Run with a service account, region europe-west1). |
| Who owns the `eval` GitHub environment and WIF? | Not created. Needs an owner before the live job can run. |

## Inventory (offline, read by hand; the inventory script could not run, no shell)

- Model ID `gemini-2.5-pro` in three places: `app/settings.py` default, `deploy/cloudrun.sh` (`MODEL_ID` env, overrides the default), `app/triage.py` (hardcoded). `triage.py` now reads `Settings`, so one value plus the deploy env controls both agents. The deploy script is still a second source and is the one to change last.
- Judge model: unset. The ADK 2.8.0 judge default is `gemini-2.5-flash`, a model on the same retirement path. Plan below uses no judge in the gate, so this does not block, but the nightly tier cannot be added until a judge is pinned.
- No eval config existed. Defaults would have applied: trajectory 1.0 and `response_match_score` 0.8.
- Prompts are constants in `app/prompts.py`; no versioning. Record its sha256 in the changelog row.
- `adk eval` exits 0 on failures in 2.8.0 (per the skill's source reading; not re-verified here). The gate does not use it.

## Findings about the 40-case set that limit what the gate can promise

1. **10 distinct scenarios, 4 copies each.** Cases 11-40 are the first ten with "(variant N)" appended. Three repeats of 40 cases is about 10 independent observations, not 40.
2. **All 40 reference replies are the placeholder "(reference reply omitted)".** `response_match_score` (ROUGE) against it is meaningless, so the config omits it. Nothing grades reply wording.
3. **All expected tool args are `{}`.** Real calls carry arguments (order ID, amount). Whether 2.8.0 trajectory matching treats `{}` as a mismatch was not verified. `ignore_args` arrived in 2.9.0 and the pins must not move in this change. **Expect the first live run to show trajectory failures on every case that expects a call; that is a case-data fix (real args), not a model regression.** Do it in the baseline step.
4. **Only 4 cases expect `issue_refund`**, and none grades the outcome. The risk Sam named (new model quietly breaks refunds) is: refund the wrong amount, refund over the limit (`max_refund_cents` 20,000), refund a gift card, or refund without a lookup. Trajectory cannot see a wrong amount. Add end-state cases before relying on this gate for refunds (step 3).
5. No case covers `fetch_email`, `send_email` or the triage agent.
6. `app_name` in the cases is `support` while the package is `app`; confirm it loads in the first run.

## Plan (21 days; 2026-11-17 is day 21)

| Step | By | Tier / evidence | Notes |
| --- | --- | --- | --- |
| 0 Confirm prod health and the real retirement date | 10-28 | not run | If requests already fail, skip to step 5 with the best available candidate. |
| 1 Merge the gate scaffolding in this change; create the `eval` environment (WIF, project, location) | 10-30 | offline | Owner needed. Live job stays non-required. |
| 2 Fix case data: real tool args, 3-4 distinct scenarios replacing duplicates | 10-30 | local | Do not edit cases after the baseline starts. |
| 3 Add refund end-state cases (amount, over limit, gift card, other customer's order, no lookup) graded on the recorded refund, not the path | 11-02 | local | Needs an end-state grader from adk-agent-evaluation; the tools already have unit tests. |
| 4 Baseline on `gemini-2.5-pro` if still serving: 5 runs, minimum per case | 11-03 | live | Skip if the model already fails; record why. Sets thresholds. |
| 5 Side-by-side `gemini-3.8-flash` vs `gemini-3.5-flash`, frozen set, no prompt edits; record token, latency and cost deltas | 11-06 | live | Cost ceiling below. Approve before running. |
| 6 Holdout, once, with the winner. Needs a holdout set: none exists; write ~15 fresh cases first | 11-09 | live | |
| 7 If the prompt needs changes, a separate changelog row, re-run step 5 | 11-10 | live | Never folded into the model swap. |
| 8 Deploy tagged revision with 0% traffic (`--no-traffic --tag`), set `MODEL_ID`, test the tag URL | 11-11 | release | Approval for the deploy. Previous revision kept. |
| 9 Traffic 10% -> 50% -> 100% with a stop rule (refund error rate, p95 latency, refund count per hour vs 2.5-pro week) | 11-12 to 11-14 | release | Rollback = previous revision (image, prompt hash, model ID together). Note rollback only works until 11-17. |
| 10 Change defaults in `settings.py` and `deploy/cloudrun.sh`, merge | 11-14 | offline | |

Buffer 11-15 to 11-16. Judge migration is a separate later release.

## Gate design

- **Tier 1, every PR, no model calls (blocks):** existing unit tests, `tests/test_release_gate.py` (expectations match eval set; no model ID outside `settings.py`), checker dry run over `eval/ci-expectations.json`.
- **Tier 2, label `run-live-eval`, merge to main, or manual:** `evals_live/test_ci_gate.py` runs 40 cases x 3 runs, tool trajectory only, no judge. Then `check_eval_results.py` requires every run row to pass with exact row counts, so a missing CSV or a dropped case fails. Anti-flakiness: deterministic criterion, repeats, strict per-run rule, no judge, a cost ceiling of 120 case-runs that fails (not skips) when exceeded. A case that passes on the mean but fails strict is the flakiness list; keep it, move it to a rubric or end-state check.
- **Tier 3 judge nightly:** not added. Needs a pinned judge and calibration first.
- **Provisional:** thresholds (1.0 trajectory) are not measured. Until step 4 or 5 records a baseline, the live job is advisory; do not mark it required, and read a green run as "not yet a baseline".
- Cost ceiling for approval request: 120 agent runs per gate run; side-by-side two candidates x 40 x 3 = 240 runs plus baseline 200. Estimate in dollars not made (no pricing read).

## Go/no-go record (fill during steps 4-9)

Use `.claude/skills/adk-release-engineering/assets/model-upgrade-checklist.md`. Frozen hashes to record: `eval/support.evalset.json`, `eval/test_config.json`, sha256 of `ROOT_INSTRUCTION` and `TRIAGE_INSTRUCTION`, tool signature hash, `google-adk==2.8.0`, `google-genai==2.19.0`.

## Not done

Models not changed; no eval run; unit tests not run (no shell); `evals_live/test_ci_gate.py` and the workflow are unverified against ADK 2.8.0 and GitHub; GitHub environment, WIF and variables not created.
