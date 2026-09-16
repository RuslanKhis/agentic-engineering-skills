# Claude Code — safe API adapter

Fresh local `/safe-api-tool-calls` invocation on 16 September 2026, followed by one review-driven repair in the same session. See [the laptop report](../../../updated-skills-laptop.md).

- `project/`: final generated adapter, authored tests and unchanged fixture contract/pins.
- `prompt.txt`, `repair-prompt.txt`: instructions sent to Claude; machine paths are normalised.
- `before-review-repair/`: first generated version, preserved with the two discovered defects. Do not use it as a working implementation.
- `acceptance/`: five pre-existing acceptance methods plus two added after independent review.
- Result files distinguish the first run, repair, failing review regressions and final verification.

Final independent execution: **24 authored tests + 7 acceptance tests passed** on **Python 3.11.4 / HTTPX 0.28.1**. Initial authoring and repair checks used Python 3.12.9. Subtests and repeated runs are not added to these counts.

From the repository root, with a Python 3.11.4 environment containing `httpx==0.28.1`:

```bash
API_CASE="$PWD/docs/testing/artifacts/updated-skills/api"
python -B -m unittest discover -s "$API_CASE/project" -p 'test_*.py' -v
SAFE_API_EVAL_PROJECT="$API_CASE/project" \
  python -B -m unittest discover -s "$API_CASE/acceptance" -p test_adapter.py -v
```

The contract uses an authenticated caller-owned client and simulated provider. These tests do not verify real payment behaviour, distributed recovery, model tool use, or cloud deployment. Acceptance files were kept outside the task project; the original five also ship with the installed skill, so this is not a concealed benchmark.
