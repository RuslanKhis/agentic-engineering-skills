# REPORT: T-103 (gemini-2.5-pro is retiring)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-engineer` (via `/adk-engineer`): `.claude/skills/adk-engineer/SKILL.md`
2. `.claude/skills/adk-release-engineering/SKILL.md` (primary specialist)
3. `.claude/skills/adk-release-engineering/references/model-migration.md`
4. `.claude/skills/adk-release-engineering/assets/model-upgrade-checklist.md`
5. `.claude/skills/adk-release-engineering/assets/PROMPT_CHANGELOG.md`
6. `.claude/skills/adk-release-engineering/scripts/inventory_release_refs.py`. I ran it, I didn't read it: first with Python 3.9, which exited 2, then with 3.12, plus `--help`
7. `.claude/skills/adk-model-and-output-contracts/references/model-selection.md` (supporting)
8. `.claude/skills/adk-model-and-output-contracts/references/reasoning-and-sampling.md`, first 59 lines (supporting)
9. `.claude/skills/adk-release-engineering/references/ci-eval-gates.md`
10. `.claude/skills/adk-release-engineering/assets/eval-gate.github-actions.yml`
11. `.claude/skills/adk-agent-evaluation/SKILL.md` (supporting)
12. `.claude/skills/adk-agent-evaluation/assets/evaluation-expectations.json`, `scripts/check_eval_results.py --help`, and a grep of `references/live-evaluations.md` for the eval-set field table

## 2. Specialist chosen and why

**Specialist: `adk-release-engineering`.** The ticket is a model deprecation notice. The adk-engineer routing table (`.claude/skills/adk-engineer/SKILL.md`, the "Model deprecation notices…" row) and the specialist's own description both send that case here. Its mode guidance says "A deprecation notice is (c) then (d) then a changelog row in (a)". "Our CI only runs unit tests" pointed at mode (b), an eval gate in CI.

Supporting skills:
- `adk-model-and-output-contracts`: choosing the replacement model and the thinking and temperature settings for Gemini 3.
- `adk-agent-evaluation`: eval-set format and the strict CSV checker.

The ticket names no `Primary skill`, so I picked from the table.

## 3. Files changed, and what is not finished

| File | Change |
| --- | --- |
| `support_agent/models.py` (new) | Single pin `AGENT_MODEL = "gemini-3.8-flash"` and `TRIAGE_THINKING_LEVEL = "medium"`. No google.adk import, so tests can load it |
| `support_agent/agent.py` | Four `gemini-2.5-pro` literals → `AGENT_MODEL`. Triage `thinking_budget=2048` → `thinking_level`. `temperature=0.2` removed from triage and root (Gemini 3 default is 1.0). Prompts are unchanged |
| `tests/test_model_pins.py` (new) | Offline tests: pinned, no alias, not retiring, every LlmAgent uses `AGENT_MODEL`, no `thinking_budget` |
| `tests/eval/test_ci_gate.py` (new) | Tier-2 live gate: `AgentEvaluator.evaluate(num_runs, output_file=CSV)` with a cost ceiling. Skips (NOT RUN) unless `EVAL_LIVE=1` |
| `evals/ci.evalset.json`, `evals/test_config.json`, `evals/ci-expectations.json` (new) | Draft 2-case read-only set: order lookup, and invoice routed to billing. Criterion `tool_trajectory_avg_score` 1.0, 3 runs |
| `.github_workflows_ci.yml` | Unit-test job kept. Added an opt-in `live-eval` job (label `run-live-eval` or manual dispatch) that runs pytest+AgentEvaluator, then the strict checker. A missing CSV fails the job |
| `docs/releases/T-103-model-upgrade.md` (new) | Filled go/no-go checklist. Decision: **pending** |
| `PROMPT_CHANGELOG.md` (new) | rc-T103 row |
| `tickets/T-103.md` | Evidence section appended |

**Not finished:**
- **The side-by-side quality comparison (2.5-pro vs 3.8-flash) has not run**, so the ticket's "without silently dropping quality" is unproven. The code is a candidate, not a go.
- The eval set has 2 draft cases. They're not validated with `EvalSet.model_validate` under ADK 2.8.0 and not reviewed against real traffic.
- No refund case and no triage-accuracy set.
- No `response_match_score` threshold: the baseline needs measuring first.
- Tool schema hash unknown.
- No conformance recordings.
- No canary or deploy.
- `tests/test_tools.py` still imports through `support_agent/__init__.py` → google.adk. I left `__init__.py` alone because ADK's agent loader may rely on it.

**Questions I would have asked (my assumption in brackets):**
- Q1: Who owns and approves this release and paid eval runs? [unassigned; recorded as pending]
- Q2: The README says the API-key (Gemini API) backend, but the email is about Vertex. Which backend does production actually use? [Migrate anyway: 2.5 is "limited to prior users" on the Gemini API, and the CI live job uses the API key as in the README]
- Q3: Is a Flash-tier model acceptable in place of Pro, or would you take the Pro preview? [Stable `gemini-3.8-flash`; no stable 3.x Pro exists]
- Q4: Are there real (de-identified) emails and labelled outcomes for a development set? [None found; draft synthetic cases]
- Q5: Is there a latency or throughput requirement that needs a load test? [Unknown; marked not run]
- Q6: Can the CI runner reach `*.internal.example` tool backends, and is there a sandbox for `issue_refund`/`send_email`? [Assumed no; the live job is opt-in and contains no mutating cases]
- Q7: Should the adk-agent-evaluation skill (currently untracked under `.claude/`) be committed so CI can run its checker? [The CI job points at `.claude/skills/adk-agent-evaluation`; it must be committed or vendored]
- Q8: Thinking level for triage: `low` (vendor advice for classification) or `medium` (closest to the old 2048 budget)? [medium]
- Q9: Is dropping `temperature=0.2` acceptable? [Yes, per vendor guidance for Gemini 3; the side-by-side will measure it]

## 4. Checks run, and checks not run

**Run (local):**
- `python3 -m pytest tests/test_model_pins.py tests/eval -q` → **3 passed, 1 skipped** (live gate skipped by design). Python 3.9.13, the only interpreter with pytest; the project targets ≥3.11.
- `check_eval_results.py --dry-run` against `evals/ci-expectations.json` → exit 0, "6 metric rows expected".
- `check_eval_results.py` on a header-only CSV → **exit 1**, "0 metric rows … 2 case/metric count mismatches". This confirms NOT RUN fails the gate.
- `json.load` on the three eval JSON files → ok. `py_compile` on `agent.py`, `models.py` → ok.
- `inventory_release_refs.py --project . --dry-run` with Python 3.12 → exit 0. The project's only model pins were the four `gemini-2.5-pro` in `support_agent/agent.py` (lines 18, 26, 37, 48 before the edit).

**Not run:**
- `tests/test_tools.py`: ImportError, google.adk not installed.
- The full `pytest` CI command.
- AgentEvaluator live gate (needs SDK, API key and backends).
- `EvalSet`/`EvalConfig` validation under ADK 2.8.0.
- Scripted-model / Runner tests (none exist).
- `adk conformance test`.
- Side-by-side quality, latency and cost comparison.
- Re-reading the live Google deprecation pages (no network).
- Canary deploy.

## 5. Friction log

1. **Helpful:** the routing table made the specialist choice immediate (`.claude/skills/adk-engineer/SKILL.md:70`). So did the composition hint "A deprecation notice is (c) then (d) then a changelog row in (a)" (`.claude/skills/adk-release-engineering/SKILL.md:43`).
2. **Unsure what to type:** the inventory helper failed on the default `python3` (3.9). The fallback rule is at `.claude/skills/adk-engineer/SKILL.md:101-103` and `.claude/skills/adk-release-engineering/SKILL.md:22`, but neither gives a command for finding a 3.11+ interpreter. I had to search `/opt/homebrew/bin`.
3. **Heavier than needed / noisy:** `inventory_release_refs.py --project .` scanned the installed `.claude/skills/` tree (149 files). It reported 13 model IDs (`gemini-9.9-future`, `gemini-offline-fixture`, judge `gemini-2.5-flash` "retiring_default" and more), and 31.6 KB of output overflowed the tool. The project contributed only 4 IDs. There is no `--exclude` flag (`--help`), and `.claude` is not in the default exclusion list. I had to post-filter the JSON by `path`. Also, the output is JSON followed by trailing text, so `json.load` failed ("Extra data"). See `.claude/skills/adk-release-engineering/SKILL.md:25-28`.
4. **Assumed something I couldn't provide:** "Dates below are a snapshot; verify them on the cited pages at use time" (`.claude/skills/adk-release-engineering/references/model-migration.md:7`, also `.claude/skills/adk-model-and-output-contracts/references/model-selection.md:3`). No network, so I relied on the snapshot and recorded that.
5. **Assumed something I couldn't provide:** the migration procedure asks for a frozen development set, judge, holdout and a two-stage side-by-side (`.claude/skills/adk-release-engineering/references/model-migration.md:35-41`). The project has none of these, and the skill gives no "minimum viable path when no eval set exists". I had to improvise a 2-case draft set.
6. **Assumed something I couldn't provide:** the workflow asset assumes the Vertex backend (`GOOGLE_GENAI_USE_ENTERPRISE`, WIF; `.claude/skills/adk-release-engineering/assets/eval-gate.github-actions.yml:108-123`), plus `requirements.txt`, `tests/unit`, conformance recordings and a judge config (lines 61, 84, 86, 172). This project uses an API key and `pyproject.toml`, so I adapted roughly 60% of it by hand.
7. **Assumed something I couldn't provide:** the checker is "reused, not copied", from an installed skill path (`.claude/skills/adk-release-engineering/references/ci-eval-gates.md:25-30`; asset line 41-43). In this repo `.claude/` is untracked, so CI cannot see it without a decision from the user.
8. **Unsure what to do (safety):** none of the references warn that a live eval of an agent with mutating tools (`issue_refund`, `send_email`) will perform real writes unless the tools are mocked. I worked this out from `tools.py` and excluded refund cases. `ci-eval-gates.md:39` mentions environment simulation only as a flake control.
9. **Unsure:** the instruction to keep temperature at 1.0 (`.claude/skills/adk-model-and-output-contracts/references/reasoning-and-sampling.md:25`) conflicts with "same settings except the ones the new generation requires" (`.claude/skills/adk-release-engineering/references/model-migration.md:38`). The parenthetical there resolves it, but only on careful reading.
10. **Helpful:** the thinking_budget → thinking_level warning with its Vertex 400 risk (`reasoning-and-sampling.md:19`). Without it, the triage agent would likely have broken on the new model.
11. **Helpful:** the "`adk eval` exits 0" warning and the strict checker with exact-count NOT RUN semantics (`.claude/skills/adk-release-engineering/references/ci-eval-gates.md:17-23,50-52`). It was verifiable locally in seconds.
12. **Unsure what to type next:** adk-engineer says "end with the run prompt for the next ready goal or ticket" (`.claude/skills/adk-engineer/SKILL.md:39-40`) but gives no template or wording. No specialist I read supplied a next prompt either.
13. **Reading before useful work:** 8 references and assets (~700 lines) before the first edit. The checklist asset is 81 lines, and most rows ended up "not run".

## 6. Rating

**3 / 5.** Routing was frictionless and the technical guidance was accurate and decisive: model choice, thinking_level, gates that fail by exit code. Most friction came from tooling noise and templates that assume a richer project than this one.

Three changes that would most help:
1. Make `inventory_release_refs.py` exclude `.claude/`, `.agents/` and skill install directories by default, or add `--exclude`. Emit pure JSON. Have adk-engineer give a one-line command for finding a 3.11+ interpreter.
2. Add a "minimum viable migration" path to `model-migration.md` for projects with no eval set, judge or holdout: pin, offline pin test, 3–5 read-only seed cases, baseline-on-main versus candidate-on-branch. Include an explicit warning to mock or exclude mutating tools before any live eval.
3. Make the workflow asset backend-neutral (API-key and Vertex variants) and `pyproject`-friendly. Give a concrete recommendation for how CI should get the checker when skills are installed locally and untracked.

## 7. Next prompt the skills told the user to type

None given. adk-engineer asks for "the run prompt for the next ready goal or ticket" (`.claude/skills/adk-engineer/SKILL.md:40`) but supplies no wording. My suggestion, not quoted from the skills: "Please take ticket tickets/T-104.md and carry it out."
