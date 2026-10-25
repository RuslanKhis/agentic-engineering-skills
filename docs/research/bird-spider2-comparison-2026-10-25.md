# BIRD Mini-Dev and Spider 2.0 compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [bird-bench/mini_dev](https://github.com/bird-bench/mini_dev) at
commit `abd11b6` (2026-09-05) and [xlang-ai/Spider2](https://github.com/xlang-ai/Spider2)
at commit `cafb867` (2026-08-12), cloned on 25 October 2026 (blobless,
sparse, no benchmark data downloaded) into their own directories and read,
never run. No query touched BigQuery.

**Licence.** BIRD Mini-Dev has a CC BY-SA 4.0 badge and no LICENSE file:
link only, no data, code or text. Spider2 is MIT. The BigQuery public
datasets' own terms were not settled and are left to the project.

**Maintenance.** Both quiet (last commits in August and September 2026), no
tags.

**Conclusion.** The memo's metric names are right but the definitions are
looser than this toolkit's oracle: BIRD's EX is set equality, so it passes
a reversed ranking and a duplicated row, and Soft-F1 gives partial credit
for a wrong value. Spider 2.0-Lite routes 205 tasks to BigQuery, not the
README's 214, and its comparison never aligns rows. Its upstream set-up
runs unbounded queries under an Owner key. The SQL skill now names the
definitions, keeps its own oracle as the gate, and describes Spider 2.0-Lite
as a bounded capability probe.

## Method

The three metric functions, the task-id counts, the comparison function
(tolerance, NULL handling, per-column sorting), the evaluator's thread
default and denominator, the set-up guide's Owner role and key, and the
gold-release date were confirmed in the snapshots before editing. One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/bird-spider2-alignment-2026-10-25.md).

## Drift corrected

None; the skills did not mention either benchmark.

## Imported, by specialist

- **adk-sql-agent-engineering.** In `acceptance-and-extensions.md` §1: what
  EX, Soft-F1 and R-VES compute, why the oracle stays the gate, and why
  R-VES is not computed on BigQuery; a Spider 2.0-Lite paragraph with the
  BigQuery slice, its comparison rules, and how to run it as a bounded,
  keyless, approved campaign scored offline. After the trial: the full
  Soft-F1 and R-VES arithmetic, Spider2's index-based column subsets,
  absolute tolerance, multiple gold files, id routing and denominator, the
  campaign's caps in the approval, deleting an upstream key, and a 2.12
  note on the workflow example in `adk-runtime.md`.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- BIRD data, gold SQL and evaluation code (CC BY-SA badge, no LICENSE).
- Spider2's tolerance, NULL-as-zero and per-column order-insensitive
  matching as this skill's checker rules: weaker than its exact values,
  unique keys and ranking assertion.
- Spider2's Owner service account, JSON key and evaluator as executor (no
  dry run, ceiling or labels).
- Spider2 task text in `evals/`: contamination risk, and a link does the job.
- Leaderboard numbers, Spider 2.0-Snow and DBT, and LiveSQLBench.

## Limits

Nothing upstream was run. The metric behaviour on the skill's own fixtures
comes from a restatement written from the code, not from the upstream
scripts. The README's 214 could not be reconciled with the task file.
