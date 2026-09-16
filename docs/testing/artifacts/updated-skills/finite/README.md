# Codex — finite ADK answer adapter

Fresh `$adk-engineer` invocation on 16 September 2026. Codex read the installed router, frontend, workflow and optimisation skills and adapted the finite-answer asset into the actual application. See [the laptop report](../../../updated-skills-laptop.md).

- `task.md`: original public contract.
- `before/`: deliberately faulty starting project; not a working example.
- `project/`: completed adapter, 30 authored tests, README and retained MIT notice.
- `acceptance/`: 10 independently authored methods, held outside the task project before generation.
- Baseline and final outputs record what actually ran; machine paths are normalised.

Final independent execution: **30 authored tests + 10 acceptance tests passed** on **Python 3.11.4**, using only the standard library.

From the repository root:

```bash
FINITE_CASE="$PWD/docs/testing/artifacts/updated-skills/finite"
PYTHONPATH="$FINITE_CASE/project" \
  python3.11 -B -m unittest discover -s "$FINITE_CASE/project/tests" -v
PYTHONPATH="$FINITE_CASE/project" \
  python3.11 -B -m unittest discover -s "$FINITE_CASE/acceptance" -v
```

Checks cover provisional delta snapshots, final aggregate replacement, thoughts/tool text, trusted invocation identity, late failures, cancellation, owned cleanup and unchanged application configuration. The task assumes a finite decoded input with application-owned byte admission. It does not verify a browser, live ADK transport, provider behaviour or production resource limits.
