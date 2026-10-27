I rewrote the Spider 2.0 plan and fixed the harness, but I could not run the test suite. I had no shell tool, so I checked the code by reading it only. Please run `python -m unittest discover -s tests -t .`.

## What I changed

**`eval/harness.py`**
- The draft gated on set-equality EX. That is BIRD-style execution accuracy, and it ignores row order and duplicate rows. A reversed top-3 ranking passes it, so it is too loose to gate on.
- The gate is now `public_response_accuracy`, which is the existing oracle's pass rate. That oracle checks exact values, row count and ranking order, and its 200-to-700 control fails it.
- BIRD-style EX stays as `bird_style_ex`, labelled as a diagnostic.
- `report()` returns both numbers, a 95% Wilson interval and the list of failed cases.
- The gate also requires at least 30 cases. You have 4, so one miss moves the score 25 points and the gate currently returns False. I chose 30 myself, so change `MIN_CASES` if you disagree.

**`tests/test_oracle.py`**: three new tests, none of them run yet.
- A reversed ranking passes EX but fails the oracle.
- The gate uses the oracle and refuses a case set that is too small.
- The 200-to-700 negative control lowers the reported accuracy.

**`eval/spider2_plan.md`** is rewritten as a proposal that has not been approved or run.

## Should you run Spider 2.0-Lite, and how?

Yes, as a capability probe only. It does not replace acceptance for Fernhill's own metrics. Several things in the draft need to change first:
- **Owner key.** Don't use the Owner service-account key (`keys/sandbox-owner.json`). If it exists, it needs deleting and recording as a credential clean-up. That needs the project owner, and I haven't touched it.
- **Upstream `evaluate.py`.** Don't run it against BigQuery. It has no dry run, byte ceiling or labels and uses up to 20 threads against TB-scale public data billed to your project. Instead, run the queries through your own `analytics/executor.py`:
  - Use a keyless identity with only `roles/bigquery.jobUser`, in a dedicated campaign project.
  - Don't reuse `analytics-agent@…`.
  - Save the results and score them offline.
- **Scope.** Only 205 of the 547 tasks run on BigQuery. Report the score as X/205 at a named upstream commit and label it indicative. Its comparison is loose, with extra columns allowed, numbers matching within 0.01, and no row-order check. Its gold answers have been public since December 2024.
- **Schemas.** Spider2 needs its own schema context and entry point. Don't add its tables to `domains.py` or loosen the production checks to make it work.
- **Your open questions.** Public datasets are still billed by bytes scanned to the querying project, so the cost isn't zero. The run time is unknown until a pilot of about 10 tasks measures it.

The plan has an approval table to fill in before any live run: per-query byte ceiling, total byte budget, task count, concurrency and model spend. The plan's proposed values are placeholders.

## Questions I couldn't ask, and what I assumed
- Who sets the Spider2 byte budget and project? I left them as proposals.
- Is a 0.85 gate right? I kept it but applied it to the oracle.
- Is 30 cases the right minimum? I assumed so.

## Not done
- No tests run.
- No live runs, and nothing on Spider2 or the cloud touched.
- The cited Spider2 and BIRD details come from the skill's earlier reading notes (2026-10-25), not re-verified; re-check the Spider2 commit before running.
- You need 30 or more frozen eval cases before the gate means anything; I added none.
- `google-adk` isn't installed, so the agent's own behaviour is untested.