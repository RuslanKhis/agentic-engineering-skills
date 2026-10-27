# Triage: scenarios run for the first time (b1, b2, b3, b4, b6, b7)

Every assertion that failed by majority or passed on split votes, 95 rows over
33 scenarios, classified as in Phase 9: (a) skill defect, (b) fixture or
assertion defect, (c) run variance. Rows sharing a scenario and cause are
grouped; votes are in A# order; paths are under `skills/`. Classified by a
read-only subagent and spot-checked; two of its claims were corrected (marked
"corrected").

| Scenario | A# | Votes | Class | Evidence (file:line) | Proposed action |
| --- | --- | --- | --- | --- | --- |
| interoperability-expose-and-register-a2a | 1-4 | FFF ×4 | c (A1's checker half b) | a2a-contracts.md:161, :108, :123; platform-registration.md:8, :73-76 | none |
| interoperability-expose-mcp-server-with-conformance-baseline | 1 | FFF | b | The manifest comes only from running mcp_tool_inventory.py (mcp-exposure.md:149); no shell | accept "manifest step reported not run" |
| same | 2-4 | FFF ×3 | c | validation.md:87-98, :116-121; mcp-exposure.md:91-95 | none |
| interoperability-exposed-agent-forgets-on-modern-clients | 4 | FFF | c | validation.md:150, :177; mcp-exposure.md:172 | none |
| interoperability-mcp-app-widget-to-custom-frontend | 2; 3; 4 | FFF; FPP; PFF | c | mcp-consumption.md:414-446, :424 | none |
| interoperability-verify-signed-agent-card | 1, 4 | FFP, FFF | c | a2a-contracts.md:348, :384-385, :424 | none |
| same | 3 | FFF | b | agent_card_check.py needs a shell | accept "not run" |
| observability-handover-and-postmortem | 1; 3, 4 | FPF; FFF | c | operations-handover.md:64, :9, :32-33 | none |
| release-bigquery-analytics-score-gate-and-drift | 2-4 | FFF ×3 | c | ci-eval-gates.md:11; adk-agent-observability bigquery-analytics.md:81; production-feedback.md:18 | none |
| release-post-launch-quality-loop-aqua | 1-3; 4 | FFF ×3; FPP | c | production-feedback.md:37, :41, :42 (read) | none |
| engineer-resumes-from-progress-block | 2; 3 | FFF; PFP | b; c | git status and the re-verify command need a shell | accept "reported not run" |
| engineer-ticket-with-missing-companion | 1 | FFF | c | adk-engineer/SKILL.md:70, :167 route to composition.md, not opened | none |
| same | 3, 4 | FFF ×2 | b | lint and theme checks need npm (as in Phase 9) | accept "not run" |
| engineer-agents-cli-deploy-ticket | 1, 2, 4 | PFP, FFF, FFF | c | deploy agent-runtime.md:93 | none |
| same | 3 | FFF | a | agent-runtime.md:37-44 has no hand-off to adk-tool-auth-and-secrets for the Agent Identity decision | one-line hand-off |
| same | 5 | FFF | b | "no revision rollback" contradicts adk-release-engineering staged-rollout.md:44-55; the cost-ledger rule is adk-engineer's (ticket-lifecycle.md:56) | reword the assertion |
| engineer-google-skills-supporting-missing | 1, 2 | PFF, FFF | a (minor) | The full rule and the `npx skills@latest add google/skills` command are in adk-engineer/SKILL.md:158-166; deploy SKILL.md:48 only says "adk-engineer explains how to get them" (corrected: a pointer exists) | state the command in deploy, or have ticket runs load adk-engineer |
| same | 3; 5 | PFF; FPP | b; c | local tests and docker build need a shell | none |
| frontend-a2ui-route-and-validation-declared | 1-4 | FFF, FFF, PFF, FFF | c | production.md:110-116; compatibility.md:31 | none |
| frontend-assistant-ui-adk-python-gateway | 2; 4 | PFP; FFF | c | production.md:66; frontend-quality.md:72 | none |
| frontend-tool-widgets-staged-emission | 2-4 | FFF ×3 | c | production.md:106, :116 | none |
| model-output-schema-with-tools-hardening | 2-4 | FFF ×3 | c (A2's checker half b) | SKILL.md:51, :63, :66; validation-and-repair.md:33, :80-82 | none |
| sensitive-data-model-armor-file-attachments-and-template-update | 4, 5 | FFF ×2 | c | model-armor.md:127-135, :75, :83 | none |
| sensitive-data-offline-pii-oracle-in-ci | 1-4 | FFF, FFF, PFF, PFF | c | validation.md:24-56; SKILL.md routes there, no reference read | optional: name "offline leak oracle" in the validation row |
| sql-acceptance-metric-names-and-spider2-bigquery-probe | 2; 4 | FFF; PFP | c | acceptance-and-extensions.md:39-53 | none |
| sql-managed-bigquery-mcp-read-only-by-platform | 3, 4 | FFF ×2 | c | acceptance-and-extensions.md:304-316 | none |
| sql-semantic-map-reviewed-files | 1-3 | FFP, FFF, FFP | c | implementation.md:25; execution-safety.md:11 | none |
| out-of-scope-marketing-edit | 3 | FFF | c | no skill involved | none |
| plain-adk-no-scaffold | 4, 5 | FFF ×2 | c (corrected) | The agent's Reads of `.../plain-adk-no-scaffold/app/tools/*.py` were denied because it left out the `workspace/` segment; the denial is correct confinement, not a harness fault | none |
| workflow-checkpoint-dependency-invalidation | 1, 2, 3 | FFF, FFF, FFP | c (root cause a) | checkpoint-reuse.md:20-29, :54, :106-107 (found by Glob) | see defect 1 |
| same | 5 | FFF | b | tests written, cannot run without a shell | none |
| workflow-content-safeguards-in-code | 3, 4 | FFF ×2 | c (root cause a) | content-safeguards.md:21-23, :57, :98 (read) | see defect 1 |
| workflow-durable-refund-resume-or-engine | 1-4 | FFF, PFF, FFF, FFF | a | no workflow file read; runtime.md:62-75, :98-107, :175-185 cover all four; SKILL.md:68 routes, the description has no trigger | see defect 1 |
| workflow-engine-restate-or-dapr-keeps-adk-contract | 1-5 | FFF ×5 | c | runtime.md:113-150, :151-170; guardrails human-review.md:161 | assertions could add "or rejects Dapr on its licence" |
| workflow-realistic-checkpoint-storage-preflight | 1-5 | FFF, FFF, FFP, FFF, FFF | a | no skill file read; checkpoint-reuse.md:85-96 covers them (A1's Runner run also needs a shell) | see defect 1 |
| workflow-warning-only-correction-preservation | 2-4 | FFF, FFP, FFF | a | no skill file read; review-contracts.md:109-114 covers them | see defect 1 |
| portability-ticket-carried-out | 2; 7 | FFF; FPF | b | design hash needs `git hash-object` (SKILL.md:62, :201); the checker needs a shell | accept "reported not run" |
| same | 8 | PFP | c | split | none |
| presenter-monthly-value-report | 2; 3 | FFF; PFF | c; b | value-report.md:79-80; check_value_report.py needs a shell | accept "not run" |

Counts after the corrections: (a) 15, (b) 11, (c) 69.

## Suspected skill defects (not fixed in this phase)

1. **adk-workflow-design, SKILL.md:3-13 (description).** It names control
   flow, event consumption, `output_key` handoffs and parallel, loop or graph
   orchestration, but not checkpoint or saved-stage reuse, resuming after a
   restart versus a durable engine (Temporal, DBOS, Restate, Dapr), multi-day
   approval waits, checkpoint storage limits, draft consistency checks or
   warning-only correction and review repair, which the body routes
   (SKILL.md:68-69, :132-143). The primary loaded in 2 of 7 workflow runs; 15
   (a) rows in three runs, and 7 (c) rows found only by Glob.
2. **deploy-adk-on-google-cloud, references/agent-runtime.md:37-44.** No
   hand-off saying the Agent Identity decision belongs to
   adk-tool-auth-and-secrets.
3. **deploy-adk-on-google-cloud, SKILL.md:48 (minor).** A ticket loaded
   straight into deploy sees only "adk-engineer explains how to get them" for
   a missing google/skills product skill; the install command and the
   "product skill operates, specialist decides" rule are only in
   adk-engineer/SKILL.md:158-166.

## Fixture or assertion defects

- Need a shell, with no "reported not run" escape: conformance A1, signed
  card A3, resumes A2, missing-companion A3-A4, google-skills A3,
  checkpoint-dependency A5, portability A2 and A7, presenter value report A3.
- engineer-agents-cli-deploy-ticket A5 contradicts the release skill on
  Agent Runtime rollback.
- From the (a) re-runs: guardrails-unanswered-approval-and-screening-placement
  does not install protect-adk-sensitive-data, which now owns screen
  placement; sensitive-data-local-tool-result-screen-llamafirewall's
  `expected_primary` is adk-agent-security, which the ownership decision now
  makes protect-adk-sensitive-data.
