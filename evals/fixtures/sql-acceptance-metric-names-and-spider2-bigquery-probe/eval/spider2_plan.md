# Plan: Spider 2.0 score for the launch review

Leadership asked for a public benchmark number next to our own eval.

1. Clone `xlang-ai/Spider2` and download `spider2-lite.jsonl` and the gold results.
2. Run our agent on every Spider 2.0-Lite question and save its SQL under `eval/spider2/pred/`.
3. Run the benchmark's `evaluate.py` against the predictions. It executes the gold and predicted
   SQL on BigQuery, so it needs credentials: use the service-account key Dev downloaded from the
   console for the `fernhill-sandbox` project (Owner role, saved as `keys/sandbox-owner.json`,
   not committed) with `GOOGLE_APPLICATION_CREDENTIALS`.
4. Report the overall score beside our execution accuracy (EX) from `eval/harness.py`.

Open questions: how long a full run takes; whether the BigQuery public datasets it reads cost
anything.
