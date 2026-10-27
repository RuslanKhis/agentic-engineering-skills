# Plan: Spider 2.0-Lite probe for the launch review

Status: **proposal, not approved, not run.** Nothing here has been executed.

## What the number is, and is not

- Spider 2.0-Lite is a capability probe for generated SQL on BigQuery's dialect and wide public
  schemas. It is not acceptance for Fernhill's metrics, grain or ranking. The launch gate is
  `public_response_accuracy` in `eval/harness.py` (exact values, cardinality, order).
- Of Lite's 547 tasks, 205 run on BigQuery (180 `bq`, 25 `ga` ids; the upstream README table says
  214). Report **correct out of 205 at a named upstream commit** (reference reading: xlang-ai/Spider2
  commit cafb867, MIT, read 2026-10-25; re-check the commit when we actually run). Do not quote the
  README's 214, nor the 547-task score `evaluate.py` prints.
- Its comparison is loose: gold columns need only appear among predicted columns, extra columns are
  allowed, NULL equals 0, numbers match within an absolute 0.01, several gold files pass on any one,
  and BigQuery tasks ignore row order. It will pass wrong rankings. Label it "indicative".
- Gold answers have been public since 2024-12-24: contamination is possible; say so beside the number.
- Do not call any of this "BIRD-style EX" without naming the definition (set equality of rows).

## Changes to the draft plan

1. **No Owner service-account key.** Do not use `keys/sandbox-owner.json`. Upstream's setup (Owner
   role plus a downloaded key) is far broader than the job needs. If that key already exists, it is
   a credential to delete and record as clean-up (needs the project owner; I cannot act on cloud).
2. **Do not run upstream `evaluate.py` against BigQuery.** It runs gold and predicted SQL with no dry
   run, byte ceiling or labels, on up to 20 threads, against TB-scale public datasets billed to our
   project. Instead:
   - Run predictions through the agent's own executor (`analytics/executor.py`: dry run, bytes cap,
     labels), as a keyless identity (attached/impersonated) with only `roles/bigquery.jobUser` on a
     dedicated campaign project. Not `analytics-agent@...`, whose Data Viewer is on `sales` only and
     which must not gain roles for this; use a separate identity and project.
   - Save result tables to local files; score them offline with the comparison above (a
     reimplementation or `evaluate.py`'s comparison functions pointed at saved results, after
     reading its code).
3. **The route question.** Spider2 questions will not match `sales` templates and need Spider2 schemas,
   not `domains.py`. Running them needs a Spider2-specific author context and a separate eval entry
   point. Do not add Spider2 tables to the production semantic domains or loosen the production
   executor/checks to make it work.
4. Downloaded Spider2 data is untrusted: put it in its own empty directory, run scripts from
   elsewhere, pass paths as arguments, `python -I`. Don't vendor its data (licence); link it.

## Approval needed before any live run (write these numbers in before asking)

| Item | Value (proposed, owner to set) |
| --- | --- |
| Project | dedicated, isolated campaign project, budget alert on |
| Identity | keyless, `roles/bigquery.jobUser` only |
| Tasks | 205 BigQuery tasks; start with a 10-task pilot to measure real bytes |
| Per-query ceiling | e.g. 10 GiB `maximum_bytes_billed` (the 2 GiB production cap will make many tasks refuse; count those as failures, not errors) |
| Total byte budget | set from pilot `total_bytes_billed`; stop when reached |
| Concurrency | 1-4, not 20 |
| Model spend | N generation calls; set a cap |

Answers to the open questions: public-dataset queries are still billed to the querying project by
bytes scanned (the free monthly tier is small relative to TB-scale tables), so cost is not zero; wall
time is unknown until the pilot measures it, so do not promise a duration.

## Report format

"Spider 2.0-Lite (BigQuery subset): X/205 at xlang-ai/Spider2 @ <commit>, our executor, indicative,
public gold." Alongside the launch numbers: public-response accuracy with its 95% interval and case
count, and BIRD-style EX labelled as a diagnostic.
