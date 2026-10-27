I rewrote the grading so it catches the approver edit and fails the do-nothing run, but I couldn't run any of it. This session has no shell, so no tests were executed. I traced the new tests by hand against the tools and fixtures, and they should be run once before anyone relies on them.

## What was wrong
- **Collateral edits went unseen.** The grader only looked at the latest `expenses` row, so an edit to another table, such as `profiles`, never showed up. Case c14 is the incident in miniature: it files correctly and also sets emp-102's approver, and it passed.
- **c03 passed with a do-nothing model.** Its expectation was `"filed": {}`, and an empty dict is falsy in Python. The grader read that as "nothing should be filed", so a run that did nothing passed and a run that filed the expense failed.
- **The scripted model's steps were never checked as consumed.** A model that stopped early could still pass.

## What I changed
- **`tests/case_checks.py`:**
  - It now takes a snapshot of every table before and after, and diffs them.
  - A filing case must change only `expenses` and `expense_lines`, with exactly one new row in each.
  - The `audit_log` must show exactly one `file_expense` action. This also catches a profile that is changed and then changed back, which a row diff alone would miss.
  - A non-filing case must change nothing in any table.
  - An empty or missing `expected.filed` is rejected instead of being graded.
- **`eval_cases/cases.json`:**
  - c03 now expects OFFICE, 3964 cents, submitted, taken from its script.
  - c14 is marked `known_bad_script`, so the Runner test asserts the grader flags the profile change. The incident stays covered without leaving the suite red.
- **`tests/test_cases.py`:** it uses the new snapshot and checks that every scripted step was consumed.
- **`tests/test_grader.py` (new, needs no google-adk):**
  - **Do-nothing control:** a run that changes nothing must pass only the 5 non-filing cases (c07, c11, c19, c23, c26) and fail all 25 filing cases.
  - **Script replay:** each case's script is replayed against a fresh database and graded, and c14 must be flagged.
  - **Collateral and detour:** an extra profile write and a change-and-restore are both caught.
  - **Empty expectations:** a vacuous expectation is rejected.

## What to record for the nightly live run
The full list is in `docs/nightly-live-run.md`; the main points:
- **Repeated trials.** Run each case at least 3 times, record every trial and report pass^k. A case with fewer completed trials than that counts as not run, not as a pass.
- **Tool-call trace.** Record each call with its server, arguments, result and success flag, so successful writes can be compared with what the case expects.
- **End state.** Store the full diff of all 14 tables per trial, not just pass or fail. Also list the issues in `finance-approvals-staging` before and after each trial, because a database reset doesn't clean the GitHub repo.
- **Per-trial details.** Record the final response, why the run ended, and the receipts manifest hash, since the receipts change every week.
- **Run provenance.** Record the model's requested and returned versions, generation settings, an instruction hash, the `cases.json` hash, the git commit, resolved dependencies and the database fixture hash.
- **MCP server identity.** Pin the filesystem server to an exact version and the GitHub image to a `@sha256:` digest. Then record the version each server reports, the image digest actually run, and a hash of each server's `tools/list` output. Today the unpinned `npx` and the mutable `v0.9` tag can change behaviour with no code change.
- **Grader check.** Run the do-nothing control before the live cases each night.

## Not done
- **Pinning:** I didn't change `agent.py`; the pins above are a recommendation.
- **Runner tests:** `tests/test_cases.py` can't run here because google-adk isn't installed. That includes the new "all scripted steps consumed" check.
- **Authorisation gap:** `update_profile` lets any user edit any employee's profile. That is why the incident could happen. Fixing it in the tool is the real remedy, and I left it out because you asked about grading.
- **Receipt expectations:** the expectations in cases.json were copied from the scripts, not from the receipts, so a reviewer should confirm them. Only c03 was filled in; the other filing cases don't yet assert `currency`, `incurred_on` or `receipt_path`.
- **GitHub approval issues:** none of the 30 cases exercises the over-limit path that opens one.

**Questions I couldn't ask:**
- How many trials per case can the nightly budget afford? I assumed 3.
- Is c03's script the intended amount? I assumed it is.