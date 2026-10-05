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
| `prompt.txt` | The current drafting prompt: about 1,600 words of prohibitions and bookkeeping with the judgment buried in Section 11 |
| `draft_stage.py` | The stage: builds the request, calls the double, writes `outputs/<case>.json` |
| `outputs/` | The retained baseline run |
| `score.py` | Evaluator-side observations per case (decision match, policy recall, condition count, schema validity); no categories, no fixes |
| `request.txt` | The exact prompt the trial agent receives |

Run from this directory:

```bash
python3 draft_stage.py
python3 score.py
```

## Baseline, for the reviewer

Remove this section from the copy given to the trial agent. The baseline
score is 3 of 5 decisions matched, mean policy recall 0.50, one schema
failure. The five defects as they appear in `outputs/`:

| Case | Defect | How it shows |
| --- | --- | --- |
| dev-002 | `missed_policy` | H3 is absent from `retrieved_policies`; the output approves a side extension the label refuses on H3(c) and cites only D1 |
| dev-003 | `missed_policy` | G4 cites Table 2 of the Design SPD but the table was not retrieved; recall 0.5 |
| dev-003 | `weak_condition` (contradiction) | A 2.4 m by 43 m splay condition is imposed although statement-3 records the highway authority's written waiver |
| dev-004 | `wrong_attribution` | The 7.8 m ridge height from elevation-H is attributed to roof-plan-G in `facts_used` |
| dev-005 | `contract_failure` | The request exceeds the double's byte limit; the output is truncated and fails schema validation |

All approvals also carry free-text conditions without a purpose
(`weak_condition`), because the prompt supplies no exemplars.

What the double rewards, each independently: labelling facts inline as
`[source-id] text` fixes the attribution; adding the missing policy and the
SPD table to retrieval fixes the missed policies and the dev-002 outcome;
two exemplar blocks, one of which shows a written waiver, remove the splay
condition and structure conditions as purpose plus text; a shorter prompt
fixes the schema failure. A checker added on top of the outputs changes none
of the five.

Record the trial beside this directory: the exact request, the agent's
NOTES.md, its first change, the order in which it ran, categorised and edited,
and the final `score.py` table. Keep failed trials.
