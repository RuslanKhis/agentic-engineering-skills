# Prompt and release changelog

One row per release. Rows are immutable; append a correction row instead of editing history. Record hashes and version numbers, never prompt text or secret values. The newest row is the current release; the row it names as rollback target is the previous release unit.

Columns:

- **Date**: release date (ISO).
- **Release**: tag or candidate ID.
- **ADK**: `google-adk` version.
- **Prompt**: label and `sha256` of the literal text that reaches `instruction` (first 12 hex characters are enough when the full hash is in the manifest).
- **Agent model**: pinned ID; one cell per agent when several differ.
- **Judge**: `judge_model` and `num_samples`; "unchanged" is a valid value.
- **Eval set**: `eval_set_id` and commit or `sha256`.
- **Tool schema**: hash from the scripted-model capture.
- **Dev delta by category**: `category: before -> after` for each category that moved; "no change" when none.
- **Holdout**: score and date, or "not run".
- **Deploy ref**: image digest, Cloud Run revision or Agent Runtime revision ID.
- **Secrets**: Secret Manager version numbers that changed, or "unchanged".
- **Rollback target**: the Release value of the row to restore.
- **Tier**: local / mocked / live / not run for the evidence behind the row.
- **Approver**: who approved traffic and paid runs.

| Date | Release | ADK | Prompt | Agent model | Judge | Eval set | Tool schema | Dev delta by category | Holdout | Deploy ref | Secrets | Rollback target | Tier | Approver |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-07 | rc-0001 (example) | 2.8.0 | billing-v12 `3f9a1c…` | gemini-3.8-flash | gemini-3.8-flash x5 | ci `a81e…` | `c07d…` | missed_policy: 4 -> 1; weak_condition: 2 -> 2 | 0.91 (2026-10-06) | sha256:… / rev billing-00042 | unchanged | rc-0000 | live | (name) |
