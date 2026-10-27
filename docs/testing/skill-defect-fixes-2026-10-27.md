# Skill defects from the scenario triage, fixed and re-run · 27-28 October 2026

The [scenario fixtures record](scenario-fixtures-2026-10-27.md) listed thirteen
suspected skill defects from the triage of its 77-scenario run. Each was
checked against the skill text on `main` at `b928f09` (the routing-gap
description edits had landed after the run), fixed in the skill that owns the
topic in [ownership.md](../../skills/adk-engineer/references/ownership.md),
and measured: activation on the dev and held-out splits, a re-run of every
scenario with an assertion triaged (a), and a first run of the scenarios
Phase 9 did not reach.

## Defects and fixes

Line numbers are on branch `phase-10-skill-defects`.

| # | Defect | Verdict | Fix | Where |
| --- | --- | --- | --- | --- |
| 1 | Guardrails description misses escalation rate, review queue, paid continuation and attempt ledger | Confirmed | Description names "escalation rates and review-queue load, paid continuations after a lost response (attempt ledgers)" | `skills/adk-operational-guardrails/SKILL.md:7-10` |
| 2 | Guardrails `human-review.md` has nothing on the escalation-rate dashboard | Confirmed | Missed escalations gate, over-escalation is the usefulness target, the dashboard rate is a drift signal only | `skills/adk-operational-guardrails/references/human-review.md:145` |
| 3 | Screen placement has no owner that states it | Confirmed | Rule copied with its citation to protect-adk-sensitive-data ("Where a screen runs") and routed from its mode table; security keeps the threat-model view with a pointer; guardrails gets a pointer row; ownership.md gains a row | `skills/protect-adk-sensitive-data/references/boundaries.md:182-210`, `SKILL.md:64`; `skills/adk-agent-security/references/agency-and-output.md:280-282`; `skills/adk-operational-guardrails/SKILL.md:56`; `skills/adk-engineer/references/ownership.md:32` |
| 4 | Security mode (d) does not route to "Screening is a layer" | Confirmed | Mode (d) names the section and what it holds (Preview and accuracy caveat, placement, aggregate bound, signed writes, simulated demo controls); the implement bullet links it | `skills/adk-agent-security/SKILL.md:96`, `:130-133` |
| 5 | Protect has nothing on Prompt Guard 2; its description never names prompt content leaking through exporters | Confirmed | "A local screen for tool results" (512-token window and chunking, `scan_async` ALLOW on error, unconfigured role ALLOW, load once from pre-provisioned weights, Llama 4 licence as an owner decision, test fake) moved from security with its citation; security keeps two threat-model facts and a pointer. Description adds "prompt content leaking through trace, completion-upload or analytics exporters" and screen placement; the reciprocal pair with observability ("telemetry pipelines and alerts" / "content-redaction policy") is unchanged, and ownership.md's redaction row says which side owns what may leave | `skills/protect-adk-sensitive-data/references/boundaries.md:140-180`, `SKILL.md:3-15`, `:65`; `skills/adk-agent-security/references/agency-and-output.md:284-291`, `SKILL.md:134-136` |
| 6 | Memory has no rule for the SDK-absent case | Confirmed in SKILL.md (the shared evidence-labels block in `operating-rules.md` already says a hand-built Runner is never a pass) | Write the scripted-model Runner tests of stored effects and report them `not run`; no `SimpleNamespace` Runner; these are application checks, not behavioural unit tests | `skills/adk-memory-architecture/SKILL.md:152-157` |
| 7 | Engineer ticket lifecycle silent on backups and PITR outliving the instance | Confirmed | Retention line copied from the designer's resource cost ledger with its pages and date; the teardown ticket checks `gcloud sql backups list --instance=-` | `skills/adk-engineer/references/ticket-lifecycle.md:47-56` |
| 8 | Evaluation description misses quote or citation support, saved paid-stage recovery, holdout budget | Confirmed | Description adds "quote or citation support", "fixing a failed stage without re-running paid earlier ones", "holdout budgets", trimmed elsewhere to stay under 950 characters | `skills/adk-agent-evaluation/SKILL.md:3-17` |
| 9 | Evaluation has no do-nothing control | Not confirmed | The rule is at `references/evaluation-design.md:9` (curate cases, step 1: run a do-nothing scripted model through every case's graders, give each action case an assertion it fails, nothing-else-changed assertions pass a no-op) and `SKILL.md:49` links it; the run's agent read that file. No change | - |
| 10 | Release capability gate drops the MCP definition pin | Confirmed | The capability diff sees a widened `tool_filter` but not a server's changed definition; keep `mcp_tool_inventory.py --diff ... --fail-on-diff` as a separate check | `skills/adk-release-engineering/references/ci-eval-gates.md:29` |
| 11 | Interoperability silent on schema keywords ADK's conversion drops | Confirmed | Section "Schema keywords the conversion drops" with the SEP citations, a recorded-definition comparison, and a checklist line; tool-interface named as owner of the subset | `skills/adk-agent-interoperability/references/mcp-consumption.md:151-167`, `:466` |
| 12 | Deploy topology A gives no IAP audience form | Confirmed | Topology A: Cloud Run audience form, confirmed against a captured token on the first live run; topology E gets the backend-service form | `skills/deploy-adk-on-google-cloud/references/frontend-hosting.md:12`, `:16` |
| 13a | Security supply-chain pin silent on `list_changed` and TTL | Confirmed | ADK never subscribes to `list_changed`; `None` re-lists every request, a positive TTL hides a change until expiry | `skills/adk-agent-security/references/tool-supply-chain.md:41-45` |
| 13b | Evaluation does not say a judge change is a new baseline | Confirmed | Judge change (model, settings, rubric) starts a new baseline; pointer to release's versioning reference | `skills/adk-agent-evaluation/references/evaluation-design.md:51` |
| 13c | Observability states the Agent Runtime tail loss only in a table | Partly (also in `export-paths.md:30`) | SKILL.md's provider-ownership bullet states the tail loss and the second-request check | `skills/adk-agent-observability/SKILL.md:68` |

No rule was needed verbatim in three or more skills, so no shared snippet was
added. `docs/skills.md` entries for the three changed descriptions were kept
consistent; README.md and CHANGELOG.md were not edited.

### Description lengths

| Skill | Before | After |
| --- | --- | --- |
| adk-operational-guardrails | 849 | 949 |
| adk-agent-evaluation | 932 | 947 |
| protect-adk-sensitive-data | 736 | 885 |

`scripts/check_boundaries.py` passes.

## Activation

`scripts/run_activation.py --backend claude-cli --model claude-sonnet-5-5
--repeat 2`, compared with the routing-gap run
(`artifacts/routing-gaps-2026-10-27/dev-sonnet-5-5.json`). Nine dev cases
were added to `evals/activation.json`: positives for escalation queues, paid
continuations, quote support, saved-stage recovery, exporter leaks and screen
placement; near-misses for an escalation dashboard (observability), workflow
resume (workflow-design) and a trace pipeline (observability).

| Split | Cases × repeats | PASS | PARTIAL | FAIL | Baseline |
| --- | --- | --- | --- | --- | --- |
| dev | 172 × 2 | 331 | 12 | 1 | 163 × 2: 315 / 11 / 0 |
| held-out (run once, after the edits) | 78 × 2 | 156 | 0 | 0 | 156 / 0 / 0; no case changed grade |

All nine new dev cases passed in both repeats except
`guardrails-review-dashboard-near-miss` (PASS, PARTIAL: guardrails named as
supporting behind observability). The one new FAIL is
`designer-checkpoint-positive` (PARTIAL, FAIL: adk-engineer chosen over
adk-system-designer), and neither description changed. Three repeats of the
designer cases alone gave PARTIAL, PASS, PARTIAL on this branch and FAIL,
FAIL, PASS on an export of `main`, so it is existing instability between the
designer and the engineer, not a regression from these edits; it is left for
the designer's owner. Artifacts:
[activation/](artifacts/scenarios-2026-10-27-defect-fixes/activation/).

## Scenario runs

Settings as Phase 9: `run_scenarios.py run`, agent and judge
`claude-sonnet-5-5` through `claude-cli` (Claude Code 2.1.306), three judge
repeats with majority verdicts, `--max-turns 30`, 900 s, `--max-budget-usd 3`,
default confinement (no shell), project skill install, skills at `c297ef1`.
Evidence per scenario and each batch's manifest and results are under
[scenarios-2026-10-27-defect-fixes/](artifacts/scenarios-2026-10-27-defect-fixes/);
[summary.md](artifacts/scenarios-2026-10-27-defect-fixes/summary.md) has every
vote. A pause stopped four batches part-way: finished agents were judged on
their unchanged evidence (`judge --run-dir`; the b4 manifest was cut to its
two finished scenarios), and the five workflow and three portability or
presenter scenarios whose agents were cut were re-run from fresh workspaces
(batches b6, b7).

### (a) assertions before and after

All 16 scenarios with an (a) row were re-run. The triage tables hold 27 (a)
rows (26 marked "a" and `privacy-with-observability` A1 marked "a+c"; the
fixtures record's count of 29 could not be reproduced). Per row:
[a-assertions-before-after.md](artifacts/scenarios-2026-10-27-defect-fixes/a-assertions-before-after.md)
(its "primary loaded" column uses each scenario's `expected_primary`).

| Defect | Scenario | (a) rows | Before | After | Reading |
| --- | --- | --- | --- | --- | --- |
| 1, 2 | guardrails-continuation-accounting-and-duplicates | A2, A4 | FFF, FFF | FFF, FFF | Skill now loaded (was not); the answer still lacks stage allocations and separate ledger fields: variance |
| 1, 2 | guardrails-escalation-two-sided-calibration | A1-A3 | FFF ×3 | FFF ×3 | Skill loaded and `human-review.md` read (neither before); no scripted Runner test or labelled set, and the drift rule was paraphrased, not adopted: variance |
| 3 | guardrails-unanswered-approval-and-screening-placement | A3 | FFF | FFF | protect-adk-sensitive-data, which now owns placement, is not installed for this scenario, and the pointer row alone did not move the screen: fixture defect, install the owner |
| 4 | security-refund-agent-build-time-controls-vs-screening | A1, A3, A4 | FFF ×3 | PPP, FFF, FFF | Agent read agency-and-output.md (no reference before); the Preview caveat now passes; signed writes and the A2A policy service still not built or named: variance |
| 5 | sensitive-data-local-tool-result-screen-llamafirewall | A1, A2, A5 | FFF ×3 | PPP ×3 | protect-adk-sensitive-data loaded and its new section read. The scenario's `expected_primary` is still adk-agent-security, which the ownership decision now contradicts: assertion metadata to update |
| 5 | privacy-with-observability | A1 | FFF | PPP | Data-boundary skill loaded (no skill before); scenario 2/6 to 4/6 |
| 6 | engineer-agents-cli-focused-memory-1-11 | A3 | FFF | FFF | Runner tests written, but no forgetting case and no "application checks" sentence: variance |
| 6 | memory-write-back-loop-from-horizon | A4 | FFF | PPP | Pass |
| 7 | engineer-ticket-creates-cloud-sql | A3 | FFF | PPF | Pass |
| 8 | evaluation-bound-spans-versus-model-paraphrase | A1-A5 | FFF ×5 | FFF ×5 | Still no skill loaded: the agent went straight to the code. The dev activation case for the same kind of request passes, so selection from the description works; the agent did not consult any skill |
| 8 | evaluation-progressive-downstream-repair | A4 | FFF | FPF | Skill loaded (was not); split vote |
| 9 | evaluation-collateral-damage-no-op-control | A3 | PFF | FFF | Not a defect (rule already present); the agent added a do-nothing control but not the by-construction note: variance |
| 10 | release-coding-agent-capability-diff-gate | A5 | FFF | FFF | The answer now names the pin as a separate `--fail-on-diff` check, read from ci-eval-gates.md, but deferred it because the agent found the fixture's manifest unusable; judged not implemented |
| 11 | interoperability-consume-enterprise-mcp-server-registration-and-sso | A4 | FFF | FFF | The judges credit the schema-drop check now; the assertion still fails on recording the mcp major version |
| 12 | web-backend-deploy-routes-to-deploy | A3 | FFF | PPP | Pass; scenario 4/4 |
| 13a | mcp-rug-pull-runtime-pin-and-mcp-ids | A1 | FFF | FFF | The answer cites list_changed but frames it as unneeded, and its test uses fake tools rather than a Runner with a changing server double: variance |

(a) rows passing: 0 of 27 before, 8 of 27 after. Whole scenarios: 22 of 71
assertions before, 33 of 71 after; the expected primary's SKILL.md loaded in
14 of 16 runs (9 of 16 in Phase 9, judged then before slash commands
counted). Of the 19 rows still failing, the defect's own point now appears in
the answer in three (release A5, interop A4, rug-pull A1), one needs a
fixture change (guardrails A3), five belong to the one run that loaded no
skill (bound-spans), and the rest are answers that left out what the loaded
skill says.

### Scenarios Phase 9 did not reach

The set was computed from the runner's list: scenarios runnable now that were
not runnable before Phase 9 (113), less the ones Phase 9 graded. That gives
40, not the 41 the fixtures record states, plus the two whose fixtures changed
after their run (`engineer-resumes-from-progress-block`,
`engineer-ticket-with-missing-companion`). 33 of these 42 ran; the eight
governance packs and `presenter-rollout-pack-go-live` were left for the cost
cap.

| Primary skill | Run | Assertions passed (majority) | Split votes | Primary SKILL.md loaded |
| --- | --- | --- | --- | --- |
| (no primary: out-of-scope edit) | 1 | 2/3 | 0 | - |
| adk-agent-interoperability | 5 | 6/20 | 3 | 5/5 |
| adk-agent-observability | 1 | 1/4 | 1 | 1/1 |
| adk-engineer (the two changed fixtures) | 2 | 3/7 | 1 | 2/2 |
| adk-frontend-integration | 4 | 7/15 | 2 | 4/4 |
| adk-model-and-output-contracts | 1 | 1/4 | 0 | 1/1 |
| adk-portability-planning | 1 | 6/8 | 2 | 1/1 |
| adk-presenter | 2 | 7/9 | 1 | 2/2 |
| adk-release-engineering | 2 | 2/8 | 1 | 1/2 |
| adk-sql-agent-engineering | 3 | 6/12 | 3 | 3/3 |
| adk-workflow-design | 7 | 8/33 | 4 | 2/7 |
| deploy-adk-on-google-cloud | 2 | 3/10 | 4 | 2/2 |
| protect-adk-sensitive-data | 2 | 4/10 | 2 | 2/2 |
| **All** | 33 | 56/143 (39 %) | 24 | 26/32 |

The two changed fixtures: `engineer-resumes-from-progress-block` 1/3 to 2/3
(A3 now passes on a split vote; A2 needs a shell),
`engineer-ticket-with-missing-companion` 2/4 to 1/4 (A1 fell: the agent did
not open the composition reference).

**Triage** of the 95 failed or split rows
([triage.md](artifacts/scenarios-2026-10-27-defect-fixes/triage.md)):
15 (a), 11 (b), 69 (c). New suspected skill defects, not fixed here:

1. **adk-workflow-design description** (SKILL.md:3-13) names none of
   checkpoint or saved-stage reuse, resume versus a durable engine, multi-day
   approval waits, checkpoint storage limits, draft consistency checks or
   warning-only correction, though the body routes them; the skill loaded in
   2 of 7 workflow runs, and all 15 (a) rows are this gap.
2. **deploy-adk-on-google-cloud `references/agent-runtime.md:37-44`**: no
   hand-off giving the Agent Identity decision to adk-tool-auth-and-secrets.
3. **deploy-adk-on-google-cloud SKILL.md:48** (minor): a ticket loaded
   straight into deploy sees only "adk-engineer explains how to get them"
   for a missing google/skills product skill.

Fixture and assertion defects found: ten more shell-dependent assertions
without a "reported not run" escape; `engineer-agents-cli-deploy-ticket` A5
contradicts the release skill on Agent Runtime rollback;
`guardrails-unanswered-approval-and-screening-placement` should install
protect-adk-sensitive-data now that it owns placement; and
`sensitive-data-local-tool-result-screen-llamafirewall` should name
protect-adk-sensitive-data as `expected_primary`. In two workflow runs the
agent built absolute paths without the `workspace/` segment and was refused;
the confinement worked as intended.

## Cost

Recorded: agent $16.51, judge $6.42, **$22.93** for the 49 graded scenarios
(16 re-runs, 33 first runs). Not recorded: the judge calls superseded when
batches b1 and b3 were re-judged after the pause (five scenarios, about $0.60
at this run's judge average) and the two agents cut by the pause before they
wrote a result, whose cost was not reported. Activation runs go through the
same CLI and are not part of the scenario cap. The total stays under $25, so
nine scenarios were not started.

## Left

- The eight governance packs and `presenter-rollout-pack-go-live` (about $5
  at this run's $0.47 per scenario).
- The three new suspected defects above, and the designer-versus-engineer
  activation instability, for their owners.
- The fixture and assertion changes listed above, and a re-run of the
  guardrails placement scenario with protect-adk-sensitive-data installed.
- `evaluation-bound-spans-versus-model-paraphrase` still loads no skill: the
  description now selects the evaluation skill in activation, but the agent
  went straight to the code; a contextual case cannot fix that.

## Limits

One run per scenario, as in Phase 9, so a changed verdict on one assertion
says what happened in this run, not how often; 6 of 71 re-run assertions and
24 of 143 new ones had split judge votes. The agent had no shell. The new
triage was done by a subagent of the same model family and spot-checked
(two of its claims corrected); its (a) rows were checked against skill text,
its (c) rows mostly against the judges' reasons.

## Checks

`.venv/bin/python scripts/check_repo.py` passed on Python 3.12.9, including
`check_boundaries.py` and `sync_shared.py --check`.
