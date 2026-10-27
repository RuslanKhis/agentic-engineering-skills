# Situation: release-model-retirement-and-ci-gate

Overlay on support-assistant:
- pyproject pins google-adk 2.8.0.
- `gemini-2.5-pro` in three places: `app/settings.py` default, `app/triage.py`, `deploy/cloudrun.sh`
  env (A1: release inventory, pin judge explicitly, release manifest with models, prompt hashes,
  eval set).
- `eval/support.evalset.json`: 40 cases; no eval config file; judge model unset (A1/A2).
- `.github/workflows/ci.yml` unit tests only (A2: gate with pytest/AgentEvaluator or replay; adk eval
  exit code 0 on failures through 2.12.0; repeats, cost ceiling, NOT RUN as failure).
- Prompts are Python constants in `app/prompts.py` (prompt hashes for the manifest).
- `docs/notices/model-retirement.md`: retirement 2026-11-17 (three weeks).
- A3 (side-by-side, holdout once, hand-offs) and A4 (Cloud Run tagged revision canary, joint
  rollback, no deployment executed) graded from the answer.
Context unchanged.
