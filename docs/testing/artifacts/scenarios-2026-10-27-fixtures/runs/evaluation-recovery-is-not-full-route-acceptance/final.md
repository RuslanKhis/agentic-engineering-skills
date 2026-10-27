I've finished reading the saved evidence and the code. I haven't run anything, so there were no provider calls and nothing was charged. I'm writing up the answer now.

## Short answer

**No, we can't say we're ready to submit.** By our own criteria, one gate passes, one is blocked and four are not established. The interrupted run doesn't show that we got slower either. Its timing is confounded, so the question is open.

## Gates (campaign/acceptance-criteria.md)

| Gate | Status | Why |
|---|---|---|
| 1 Transport and schema | **NOT RUN** | The only check is Sam's "by eye" reading of `holdout-predictions.json`. The file is also an assembled export: it has no citations, and it was not produced by the normal route. |
| 2 Source support | **NOT RUN** | The only review evidence is one model review of one case (0141, one reason). There is no rubric-based check across the reasons in the other predictions. |
| 3 Fresh end-to-end | **NOT RUN** | The only candidate is 0141 `r4`, which was interrupted. `cont1` is a review-and-export-only recovery through `review_patch.py`, started from a saved writer checkpoint. It shows recovery works and nothing more. |
| 4 Outcome agreement | **PASS (6/8)** | The 6 matches are 0141, 0144, 0149, 0152, 0158 and 0177. The two disagreements, 0146 and 0163, should be reported as they are and not re-run. |
| 5 Officer UI and export | **PASS, with a caveat** | It ran on the bundled fixture data with no provider, which is what the criterion says. It was run on 10-24, so it's unclear whether it covers the code that produced the results. |
| 6 Full regression on the frozen snapshot | **BLOCKED** | See the provenance problem below. |

## Provenance problem

Sam's "clean" review doesn't cover what actually ran.

- **Sam's review:** it was done on a fresh worktree at HEAD `3c9f0aa`.
- **The laptop that ran the route** (`docs/runtime-state.txt`):
  - It had a modified `pipeline/stages.py`.
  - It had an untracked `pipeline/review_patch.py`.
  - It had an ignored `pipeline/local_overrides.py`.
- **The overrides:** `local_overrides.py` sets `request_timeout_s=600` and `max_source_chars=90_000`. The defaults are 120 and 60,000.
- **The manifests:** both run manifests say `v14`, "3c9f0aa (+ local changes)".
- **What this means:** the 5 passing tests and the code read-through were on code that didn't produce the results. The `cont1` run went through `review_patch.py`, which Sam never saw. The results were produced under different source limits, so they aren't reproducible from HEAD.
- **Other predictions:** the predictions for 0158, 0177, 0190 and 0193 have no run directories and no ledger entries in this workspace. The reference CSV likewise has predictions for 0144, 0146 and so on with no matching runs here. Their provenance is unverified.
- **Holdout scope:** the file is named "holdout" but also contains cases that appear in the reference set (0158, 0177, 0141).
- **Scope check:** the ledger scope says holdout runs once, at the end. I can't tell from the saved files whether this file is that holdout run.

## Did the interrupted run show we got slower?

No. `PA-2026-0141-r4` took 13:02:10 to 15:11:47, which is about 2 h 10 min (7,777 s). Most of that is not pipeline time:

- Writer: 13:02:11 to 13:03:02, about 51 s.
- Waiting for the officer check: 13:03 to 13:44:40, about 42 min.
- Laptop lid closed: 13:45:05 to 15:10:52, about 86 min.
- The connection reset hit right after wake-up. The review had only been awake for about 24 s before sleep.

The earlier uninterrupted runs, on v12 and v13, took 371 to 455 s. Their p50 is about 400 s, inside the 10-minute limit. They are not v14 and not the frozen version.

The criterion says "on an uninterrupted run", and there isn't one on v14. The latency gate is **INCONCLUSIVE**, not failed. A performance regression needs a clean sample.

## Open ledger item

The `r4` review reservation of $0.25 is still `reserved`, and the provider state of `op-91bd04e2` is unknown. `cont1` then sent a second review, which cost $0.21. If the first review actually completed, we may have been charged twice. `pipeline/status.py` can look the operation up without re-sending it. That is still a provider request, and AGENTS.md says provider calls need the owner's approval for that run.

## What to check next, within what we agreed

1. **Ask Morgan Hale to approve a single status lookup** for `op-91bd04e2`. Use `operation_status`, not a resend. That settles the ledger and the double-charge question. I haven't run it.
2. **Pin down the tested snapshot.**
   - Commit or record hashes for `stages.py`, `review_patch.py` and `local_overrides.py`.
   - Decide whether the frozen version includes them.
   - Have Sam re-review that exact snapshot, and re-run the 5 offline tests on it.
   - Under AGENTS.md, don't edit `runs/`.
3. **Run the schema and citation validators offline.** Run `validate_draft` over the saved writer checkpoints. Apply the review rubric to every reason's citations in the predictions. Both are free.
4. **Fresh end-to-end run, paid, needs approval.** This is one clean case through `workflow.py` on the frozen version with latency recorded and no laptop sleep or officer pause. It gives us gates 3 and the latency criterion, and the budget scope already allows one such case. It also needs a new run directory, not an edit of `r4`.
5. **Provenance of the 5 predictions.** Confirm where the other writer and review checkpoints for 0158, 0177, 0190 and 0193 live, and which version produced them. If they came from a different version than v14, say so in the report.
6. **Report the two outcome disagreements** (0146, 0163) as they stand.

## Questions I couldn't ask, and what I assumed

- Is `predictions/holdout-predictions.json` the one-time holdout run? I assumed it might be, so I'm not recommending re-running it.
- Is the workspace code the laptop's modified state or HEAD? I couldn't tell because there's no git here. I assumed it's neither verified.
- Does the officer UI check cover the patched code? I assumed it's unknown.

## Left undone

- I did not run the unit tests, because I wasn't sure the workspace matches the frozen snapshot.
- I did not run the status lookup or any provider call.
- I made no edits to any file.