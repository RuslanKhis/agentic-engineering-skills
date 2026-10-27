# Situation (judge only): evaluation-judge-agreement-and-harness-bridge

Context unchanged. Workspace: support-assistant base plus:

- `labels/human-ratings.csv`: 60 traces, ordinal 1-5 (support-lead panel, rubric helpfulness-v2).
- `judges/scores-judge-a.csv`, `judges/scores-judge-b.csv` (two judge-B scores missing),
  `judges/judge-a.md` (model alias `gemini-flash-latest`, unpinned), `judges/judge-b.md`
  (`gemini-3.5-pro`); neither prompt file carries a version beyond the rubric name.
- `scripts/judge_agreement.py`: the team's current measure: exact match and **nominal** Cohen's
  kappa between the two judges only, never against the humans; it replaces missing scores with
  "0" (a fake category) instead of excluding them or reporting not run. Last run: 0.25 / 0.07.
- Judge A is lenient (compressed to 4-5); judge B is closer to the humans but noisy.

## Assertion map

A1 Krippendorff's alpha, ordinal level recorded, meaning of 1/0/negative, each judge vs humans as
well as vs each other; A2 Inspect agent_bridge with Gemini(model='inspect') + placeholder key,
streaming cannot be bridged, proven only without tool round trips; A3 NaN/missing figure = not
run (and the "0" substitution is wrong); ADK evaluators and scripted Runner tests stay primary;
A4 pin judge ids (replace the `gemini-flash-latest` alias) and rubric versions; model-dependent
runs reported not run.
