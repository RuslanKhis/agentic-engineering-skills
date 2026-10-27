# Evaluation set

40 cases written in August from real (redacted) conversations (10 scenarios, 4 copies each; reference
replies are placeholders, so only tool trajectory is graded).

- `test_config.json`: criteria (tool trajectory 1.0). Provisional until a baseline is recorded.
- `ci-expectations.json`: the exact gate contract (case IDs, 3 runs per case) read by
  `.claude/skills/adk-agent-evaluation/scripts/check_eval_results.py`. Change it together with the eval set;
  `tests/test_release_gate.py` fails when they drift.
- Live run: see `evals_live/test_ci_gate.py` and `.github/workflows/ci.yml`. Plan: `docs/release/model-upgrade-2026-11.md`.
- `adk eval` exits 0 on failures in 2.8.0; do not use its exit code as a gate.
