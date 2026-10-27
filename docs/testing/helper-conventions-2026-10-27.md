# Helper conventions — 27 October 2026

Convention: [helper conventions](../helper-conventions.md). Check:
`tests/test_helper_conventions.py` with its exceptions in
`tests/helper_conventions_allowlist.json`.

## What the review found, checked against the code

Every `argparse` definition and exit path of the 48 command-line helpers was
read (`plan_files.py` and `review_contract.py` are importable modules with no
command line). The review was right on each point, and reading found more:

- The target directory came four ways: `--project` (most), `--root`
  (deploy and optimise inspectors, `check_tickets.py`), `--project-root`
  (`field_notes.py`), `--repo` (`profile.py`), and positionals in the
  protect and tool-auth inspectors. Deploy's `--project` took the GCP project
  ID.
- "Incomplete" was exit 1 in eight scanners, 2 in the workflow, tool-auth and
  protect inspectors, 4 in the FastAPI and frontend inspectors, 2 for a
  manifest problem in the deploy and optimise inspectors, and 0 in the SQL
  inspector. Opt-in gates (`--fail-on`, `--fail-on-diff`, `--compare`,
  `--require-baseline`, `--expect-adk`, `--require-tested-stack`,
  `--require-adk-version`) and the AG-UI outcome check used 3, while document
  checkers used 1 for the same idea. Malformed input was 1 in the session
  helpers, `local_retrieval.py` and `qualify_ingestion.py`, and a traceback in
  `score_document_coverage.py`.
- `--dry-run` was a documented no-op ("same read-only scan", "explicit
  synonym") in 17 helpers, not only tool-auth's.
- Invocations in SKILL.md used `/path/to/skill`, `/path/to/adk-workflow-design`
  and paths relative to the skill folder as well as `"$SKILL_DIR"`.

Adjustments to the proposed convention, from the code: exit 2 also covers a
named input or project directory that is missing or malformed (the document
checkers already did this); when 1 and 3 both apply, 1 wins when the failure
stands regardless of what was unread (security `--compare`, frontend tested
pins, SQL definite mismatches) and 3 wins when unread files could change the
answer (tool-auth `--expect-adk`); `--dry-run` stays visible only where it
changes behaviour.

## Behaviour changes (one per helper, for the release notes)

| Helper | Change |
|---|---|
| `adk-agent-instructions/scripts/instruction_lint.py` | Partial scan exit 1 → 3. `--dry-run` hidden, deprecated no-op. |
| `adk-agent-interoperability/scripts/agent_card_check.py` | `--fail-on` finding exit 3 → 1; no card fetched from `--url` 1 → 3; unreadable or non-object `--file` 1 → 2. |
| `adk-agent-interoperability/scripts/mcp_tool_inventory.py` | Partial exit 1 → 3; `--fail-on-diff` signal 3 → 1. |
| `adk-agent-observability/scripts/events_to_eval_set.py` | Malformed input, hook failure, existing or unwritable `--out` exit 1 → 2; malformed items skipped (no structural problems) 1 → 3. No case selected and structural problems stay 1. |
| `adk-agent-observability/scripts/invocation_summary.py` | Malformed session or price table exit 1 → 2; partial 1 → 3. `--dry-run` hidden no-op. |
| `adk-agent-security/scripts/inspect_security_surface.py` | Partial exit 1 → 3; `--compare` capability change 3 → 1 (still wins). `--dry-run` hidden no-op. |
| `adk-engineer/scripts/field_notes.py` | `--project-root` → `--project` (alias kept). |
| `adk-fastapi-backend/scripts/inspect_backend.py` | Incomplete exit 4 → 3. `--dry-run` hidden no-op. |
| `adk-frontend-integration/scripts/inspect_project.py` | Incomplete exit 4 → 3; `--require-tested-stack` failure 3 → 1, now reported even when the scan is incomplete. `--dry-run` hidden no-op. |
| `adk-frontend-integration/scripts/check_agui_trace.py` | Valid trace with an unexpected outcome exit 3 → 1. `--dry-run` hidden no-op. |
| `adk-frontend-integration/scripts/check_theme.py` | `--dry-run` hidden no-op. |
| `adk-memory-architecture/scripts/inspect_project.py` | Conflicting, mismatched or non-2.x ADK pins exit 3 → 1. |
| `adk-memory-architecture/scripts/local_retrieval.py` | Invalid input exit 1 → 2. |
| `adk-memory-architecture/scripts/qualify_ingestion.py` | Invalid inventory exit 1 → 2; error text moved from stdout to stderr. |
| `adk-memory-architecture/scripts/score_document_coverage.py` | Unreadable or malformed observation: traceback (exit 1) → message and exit 2. |
| `adk-model-and-output-contracts/scripts/audit_model_config.py` | Partial exit 1 → 3. `--dry-run` hidden no-op. |
| `adk-operational-guardrails/scripts/inspect_project.py` | Incomplete exit 1 → 3; `--require-adk` mismatch stays 1. `--dry-run` hidden no-op. |
| `adk-release-engineering/scripts/inventory_release_refs.py` | Partial exit 1 → 3. `--dry-run` hidden no-op. |
| `adk-sql-agent-engineering/scripts/inspect_project.py` | `--expect-adk` failure exit 3 → 1 (3 when the only reason is an incomplete inventory); a limit or unreadable file now exits 3 (was 0). Scope notes such as unparsed lockfiles stay 0. |
| `adk-system-designer/scripts/check_tickets.py` | `--root` → `--project` (alias kept). |
| `adk-tool-auth-and-secrets/scripts/inspect_project.py` | Positional `project_root` → `--project` (positional kept as a deprecated alias); incomplete exit 2 → 3; `--expect-adk` failure 3 → 1 (3 wins). `--dry-run` hidden, deprecated no-op. |
| `adk-tool-interface-design/scripts/lint_tool_schemas.py` | Partial exit 1 → 3. `--dry-run` hidden no-op. |
| `adk-tool-interface-design/scripts/report_tool_result_sizes.py` | Partial exit 1 → 3. |
| `adk-workflow-design/scripts/inspect_project.py` | Incomplete exit 2 → 3; `--require-adk-version` mismatch 3 → 1. |
| `deploy-adk-on-google-cloud/scripts/inspect_project.py` | `--root` → `--project` (alias kept); the GCP project ID moves from `--project` to `--gcp-project`; a `--project` that is not a directory, or `--root` with `--project`, exits 2 saying to use `--gcp-project`; `--require-baseline` 3 → 1; unreadable or invalid manifest or a hard limit 2 → 3. `--dry-run` hidden no-op. |
| `optimise-adk-on-google-cloud/scripts/inspect_project.py` | `--root` → `--project` (alias kept); `--require-baseline` 3 → 1; unreadable or invalid manifest or a hard limit 2 → 3 (a bad project directory stays 2). `--dry-run` hidden no-op. |
| `optimise-adk-on-google-cloud/scripts/check_run.py` | Acceptance failure exit 3 → 1. `--dry-run` hidden no-op. |
| `optimise-adk-on-google-cloud/scripts/context_budget.py` | Malformed input exit 1 → 2; partial 1 → 3. `--dry-run` hidden no-op. |
| `practice-profile/scripts/profile.py` | `--repo` → `--project` (alias kept); exit codes unchanged. |
| `protect-adk-sensitive-data/scripts/inspect_project.py` | Positional project → `--project` (positional kept as a deprecated alias); unreadable or over-limit metadata exit 2 → 3 (a bad project directory stays 2). |
| `safe-api-tool-calls/scripts/inspect_project.py` | Partial exit 1 → 3. `--dry-run` hidden no-op. |

Unchanged: `check_eval_results.py`, `check_source_support.py`,
`label_agreement.py`, `rank_opportunities.py`, `apply_brand.py`,
`check_governance.py`, `make_ingestion_fixture.py`,
`check_response_schema.py`, `check_portability.py`, the three presenter
checkers, the SQL `check_results.py`, `check_schedule.py`, `check_sow.py`,
`plan_status.py` and `draft_consistency.py`.

## Compatibility kept

Every old spelling still works and prints one stderr line, for example
`inspect_project.py: --root is deprecated; use --project`: `--root` (deploy,
optimise, `check_tickets.py`), `--project-root` (`field_notes.py`), `--repo`
(`profile.py`), the positional directory (protect, tool-auth; giving both a
positional and `--project` exits 2), and `--dry-run` on the 17 read-only
helpers (hidden from `--help`, documented as a deprecated no-op where the
skill mentioned it). The one break is deliberate: deploy's `--project` now
means the directory, so an old `--root DIR --project GCP_ID` command exits 2
and names `--gcp-project` instead of planning against the wrong project.
Scripts that tested for a specific non-zero code need the new numbers; a step
that fails on any non-zero exit behaves as before. One transition to note:
`adk-agent-security`'s pull-request gate runs the base commit's copy of the
inspector, so update the vendored inspector and the gate script (now
`status -eq 1` for a capability change, `-eq 3` for unread paths) in the same
pull request, which will report NOT RUN as the docs already warn.

## Exceptions allowlisted

The documents a checker reads stay positional (`check_governance.py` drafts,
`check_portability.py` assessment, `check_agui_trace.py` trace, `profile.py`
files and candidates). `profile.py --root` is the profile store, not the
project, and its exit codes 3 to 6 are binding states that six identical
`practice-profile.md` copies branch on. `field_notes.py url --repo` is a
GitHub owner/name. The test fails on an entry that no longer excuses anything.

## Documents

Invocation lines updated in 16 SKILL.md files and the references and asset
that instruct a command (flags, exit meanings, `$SKILL_DIR`, dropped no-op
`--dry-run`), plus the six identical `practice-profile.md` copies and the
release CI template. Dated records of past runs were left as written
(`validation-results.md`, `skill-validation.md`, `verification-record.md`,
`docs/testing/artifacts/`, `docs/research/`, the guardrails laptop recheck,
`safe-api-tool-calls/tests/forward-evaluation.md`). README.md and
CHANGELOG.md were not touched.

## Automated checks

Repository convention test: 9 tests (directory flags and positionals, GCP
IDs, visible no-op `--dry-run`, exit codes above 3, `$SKILL_DIR` and current
flags in 120 documented commands across SKILL.md, references and asset
templates, stale allowlist entries, and two parser cases). Helper suites gained
alias tests (deploy, optimise, tool-auth, protect, profile, `check_tickets.py`,
`field_notes.py`), the deploy `--gcp-project` refusal, the guardrails
`--require-adk` gate and the SQL unread-file and lockfile cases, and their exit
assertions moved to the new codes. `scripts/check_repo.py` passes: 26 packages, 1181 tests (60 optional SDK checks skipped), up from 1163 (60 skipped) before this change.
