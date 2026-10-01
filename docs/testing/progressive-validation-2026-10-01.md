# Progressive validation feedback — 1 October 2026

Updated three skills from the supplied field feedback about redundant inference
and repeated full-suite validation in staged paid ADK applications.

| Feedback | Instruction location |
| --- | --- |
| Focused repair, qualified continuation, fresh API cases, then frozen release checks | Evaluation's [progressive validation](../../skills/adk-agent-evaluation/references/progressive-validation.md), reached from its entrypoint, live mode and experiment re-entry record |
| Complete checkpoint identity, dependency invalidation, immutable failures and duplicate guards | Workflow's [checkpoint qualification](../../skills/adk-workflow-design/references/checkpoint-reuse.md), reached from its entrypoint, runtime, validation and model-call controls |
| Realistic persistence and lossless storage fit before spending | Checkpoint qualification and progressive validation |
| Preserve decision/evidence/warnings and allow another rejection | Workflow's [review contracts](../../skills/adk-workflow-design/references/review-contracts.md#preserve-the-scope-of-a-narrow-correction) and progressive validation |
| Separate pass meanings, acceptance criteria and outcome agreement | Progressive validation's evidence gates |
| Coverage versus unresolved uncertainty; relevance beyond keyword matching | Progressive validation and review contracts |
| Continuation allocations, settled charges, reservations, unknown holds, balance and remaining allowance | Guardrails' [live campaigns](../../skills/adk-operational-guardrails/references/live-campaigns.md#admit-continuations-within-explicit-quotas), with token-budget and validation pointers |
| Confounded latency, reconnect, isolated verification ownership and exact tested snapshots | Progressive validation, with live-campaign timing guidance |

Seven new [evaluation scenarios](../../evals/scenarios.json) specify observable
assertions for downstream repair, checkpoint invalidation, duplicate/accounting
recovery, realistic storage, narrow correction, evidence interpretation and
reviewer mistakes. Guardrails' forward cases and workflow/guardrail validation
references also carry the relevant acceptance cases. These are **authored cases,
not executed fresh-agent trials or proven behavioral improvements**.

## Executed checks

Used CPython 3.12.9 on macOS with the repository's pinned maintainer requirements:
PyYAML 6.0.3, markdown-it-py 4.0.0 and pytest 9.1.1. Installed those requirements
from existing local wheel-cache contents into an isolated temporary environment;
no repository dependency pins or application environments changed.

- `python -B scripts/check_repo.py`: exit 0; **433 passed, 59 optional SDK tests
  skipped** across the repository and existing offline helper suites.
- All **13 skill packages** validated with zero errors or warnings; the evaluation
  corpus passed structural validation.
- Official skill-creator `quick_validate.py`: exit 0 for each modified skill.
- After the final documentation/link edits, repeated package and case-structure
  checks passed. `git diff --check` passed.

The [retained suite output](artifacts/progressive-validation/repo-checks.txt) and
[source manifest](artifacts/progressive-validation/source-manifest.json) identify
the checks and modified instruction/case snapshot. JSON indentation was normalized
after the full run with parsed content verified unchanged; the final link edit
received the repeated package check, not another helper-suite run.

No runtime helper or SDK recipe was added or changed. No new real-ADK contract
execution, fresh-agent trial, provider call, pricing verification, deployment or
cloud operation was performed. Existing helper-suite passes do not demonstrate
the new continuation contracts in a target application. Historical compatibility
records and `last-tested` metadata remain unchanged.
