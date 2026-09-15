# Generated memory feature: test evidence

This snapshot contains the [original fixture](original/README.md),
[generated implementation](generated/profile_store.py), generated tests and
independent acceptance tests. The [CLI report](../../codex-memory-smoke.md)
records the prompt, routing evidence, versions, results and practical limits.

Set `PYTHON` to an interpreter containing the recorded dependencies, then run
from this directory:

```bash
cd generated
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  "$PYTHON" -B -m pytest tests ../acceptance -q -p no:cacheprovider
```

The saved implementation passed 72 tests. Rerunning it checks the generated
code; a new skill-behaviour test needs the original fixture in a fresh project.
