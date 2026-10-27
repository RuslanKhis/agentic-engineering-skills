# Situation (judge only): evaluation-collateral-damage-no-op-control

Context unchanged. Workspace: a standalone expense agent (no base).

## Planted

- `expense_agent/db.py`: 14 tables; `tests/fixture_db.py` builds a fresh seeded DB per test.
- `tests/case_checks.py grade()` checks only the `expenses` table: for a filing case the latest row's
  fields; otherwise that the `expenses` hash is unchanged. Nothing compares the other 13 tables, so
  case `c14`'s script (which calls `update_profile` on emp-102's approver before filing) passes —
  the staging incident in `docs/nightly-live-run.md`.
- Case `c03` has `"filed": {}`: `expected.get("filed")` is falsy, so the grader treats it as a
  no-change case and a do-nothing model passes it — the "one case passes with a stubbed model".
  Cases c07/c19/c26 (listing) and c11/c23 (refuse a duplicate) legitimately pass a no-op: they are
  no-effect cases.
- Bookkeeping tables written on every filing: `audit_log`, `sync_state` (timestamped),
  `expense_lines`. A full-table diff must name and justify ignoring volatile fields
  (`created_at`, `updated_at`, `at`, `sync_state.updated_at`), not drop whole tables.
- MCP: filesystem server launched with `npx -y @modelcontextprotocol/server-filesystem` (no
  version); GitHub server image by tag `ghcr.io/github/github-mcp-server:v0.9` (no digest).
  `docs/nightly-live-run.md` records only pass rate, date and model name.
- Runner tests (`tests/test_cases.py`) skip: google-adk not installed; no model access.

## Assertion map

A1 diff start/end across all tables, changed set must equal the case's expected set, named and
justified ignored bookkeeping; A2 record/field-level checks with per-assertion volatile-field
ignores, and keep the effective-mutation comparison (add-then-delete nets out of a diff);
A3 run a do-nothing scripted model through every case and require each action case to have an
assertion it fails (c03 exposed); note collateral-damage assertions pass a no-op by construction;
A4 live-run record pins `@modelcontextprotocol/server-filesystem@<version>` and the image digest,
treats a server change as a new baseline; model-dependent checks reported not run.
