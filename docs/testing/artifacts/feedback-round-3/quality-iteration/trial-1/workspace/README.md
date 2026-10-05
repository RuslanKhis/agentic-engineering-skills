# Quality-iteration trial seed

A self-contained workspace for the R2 maintainer test from the round-3
feedback: give a coding agent a working draft stage with five labelled cases
and the instruction "improve the decisions", then observe whether it runs and
categorises errors before editing code, and whether its first change targets
the largest error category rather than adding a checker.

Everything here is synthetic. `draft_stage.py` calls a deterministic
rule-based **model double**; no real model or provider is called. The double's
triggers are documented in plain words in the module docstring of
[`draft_stage.py`](draft_stage.py), so a reviewer can see what each
improvement moved.

## Contents

| Path | What it is |
| --- | --- |
| `cases/dev-00N.json` | Five householder cases: facts with source IDs, the policies a retrieval stage returned, and the officer's label |
| `policies.json` | The full synthetic policy set, including the Design SPD table, for an agent that decides to repair retrieval |
| `prompt.txt` | The current drafting prompt (version 42, about 300 words, built on the skeleton); the original 1,600-word version 41 is retained in `runs/00-baseline-retained/prompt.txt` |
| `draft_stage.py` | The stage: builds the request, calls the double, writes `outputs/<case>.json` |
| `outputs/` | The latest run; the baseline is retained in `runs/00-baseline-retained/` and every measured iteration in `runs/<NN>-<name>/` (see `NOTES.md` and `analysis/`) |
| `score.py` | Evaluator-side observations per case (decision match, policy recall, condition count, schema validity); no categories, no fixes |
| `request.txt` | The exact prompt the trial agent receives |

Run from this directory:

```bash
python3 draft_stage.py
python3 score.py
```
