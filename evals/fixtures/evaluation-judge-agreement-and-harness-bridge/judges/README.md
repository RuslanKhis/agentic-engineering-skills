# Judges

Two LLM judges rate helpfulness on the same 1-5 rubric (helpfulness-v2). Their scores on the 60
traces the support-lead panel labelled are in `scores-judge-a.csv` and `scores-judge-b.csv`; the
human ratings are in `../labels/human-ratings.csv`. Two judge-B calls failed and have no score.

`../scripts/judge_agreement.py` prints how often the judges agree. Last run: exact match 0.25,
kappa 0.07.

Inspect: someone suggested running the agent under Inspect (inspect_ai) to reuse its epochs and
reducers for repeated trials. Not tried.
