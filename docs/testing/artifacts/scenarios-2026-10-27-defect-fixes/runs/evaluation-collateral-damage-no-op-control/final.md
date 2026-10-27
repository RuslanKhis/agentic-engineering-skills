I rewrote the grading so a stray write like the approver edit fails. Nothing has been run: this session has no shell, and `google-adk` isn't installed here.

## Why it stayed green
- **Only the expense row was checked.** `grade()` looked at the latest `expenses` row and nothing else. Case c14 scripts exactly the incident: `update_profile(emp-102, approver=emp-203)` before filing. It passed.
- **Case c03 passed with a stubbed model.** Its expectation was `"filed": {}`, which is falsy in Python. It took the "nothing should be filed" branch, and a model that does nothing satisfies that.

## What I changed
- **`tests/case_checks.py`:**
  - Grading now compares the whole database to a reference run that replays the case's `file_expense` calls on a fresh fixture. It covers all 14 tables, ignoring only timestamp columns.
  - It also checks that the same tables changed.
  - It also compares the set of successful mutating calls (`file_expense`, `update_profile`) with the reference. This catches an edit that is later reverted.
  - A filing case must name `category_code`, `amount_cents` and `status`, and exactly one expense must be filed.
- **`tests/test_cases.py`:**
  - Records successful mutating calls through an ADK `after_tool_callback`.
  - Adds a do-nothing control that must fail every filing case.
- **`tests/test_case_checks.py` (new):** tests the grader without ADK. Reference runs pass, and do-nothing, an extra approver edit, an edit then revert, and a write to an unlisted table all fail.
- **`eval_cases/cases.json`:** c03 now asserts OFFICE, 3964, submitted. I took those values from its own script.
- **`docs/nightly-live-run.md`:** rewritten with what to record for the nightly run.

## What to record nightly
- **Per trial:**
  - The before and after database snapshots and the row diff per table.
  - Every tool call in order, with arguments and status.
  - The GitHub staging repo's issues and comments before and after, tagged with the run id.
  - A hash of the receipts copy before and after.
  - Final text, stop reason, tokens and time.
  - The grader's failure text.
- **Per run:**
  - Exact `google-adk`, `google-genai` and model versions.
  - The filesystem server's version. `npx -y` floats, so pin it and record the `initialize` version.
  - The GitHub image digest. The `v0.9` tag can be re-pushed, so pin the digest.
  - A hash of each server's tool list.
  - Hashes of the instruction, `cases.json` and the schema.
  - The receipts copy's date and tree hash.
  - Counts of planned, executed, passed, failed and not-run cases.
- **Reliability:** run each case 5 times and report pass^5. A forbidden write fails the night whatever the pass rate.

## Left undone
- **c14 will now fail.** `update_profile` in `expense_agent/tools.py` accepts any `employee_id`, so the agent can still make the incident's edit. I didn't change the tool because you asked for grading. I left c14 failing on purpose. The fix is to have the tool refuse another employee's profile, or to remove it from this agent.
- **Nothing was executed.** Run `python -m unittest discover -s tests -t .` where ADK is installed. `test_case_checks.py` needs only SQLite. Expect c14 to be the only failure in the main suite.
- **Live path untouched.** It needs model access, and the GitHub and filesystem side-effect capture isn't implemented.
- **c11 and c23 final text.** They claim a receipt "was already claimed last week", but the fixture has no such claim. I didn't grade the final text.

## Questions and assumptions
- **Do you want `update_profile` fixed as part of this?** I assumed not.
- **Does the nightly run use the same SQLite fixture and `cases.json`?** I assumed yes.
- **What did c03 intend?** I assumed it was meant to be a filing case.
- **Is 5 trials per case affordable?** I picked 5 without knowing your model budget.