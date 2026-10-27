# Weekly production quality loop (C6, G07)

Owner: Priya. Record: `quality_reviews` in `release/manifest.yaml`.

## Rule

Every ISO week (Monday to Sunday) ends with one row in `quality_reviews.weeks`.
A row says `REVIEWED` only when it names a reviewer and evidence. A missing row,
a review that failed, or a review that read a source the release does not write
is `NOT RUN`. Missing evidence is never a pass (A3). Fill the row on the Monday
after the week ends (A1).

## Weekly procedure

1. **Window.** Set the week's start and end (UTC).
2. **Read.** Query `support_analytics.agent_events` (D4) for the window. Start with
   invocations that had a tool error, a budget stop, a safety-filter stop or user
   feedback, then a small uniform sample of ordinary ones. Write the sampling rule and
   counts in the row's evidence.
3. **Triage.** Group failures by a fingerprint (for example `tool:get_order:error`). A
   failure is *recurring* when its fingerprint appears in two or more weeks, or three
   or more times in one week. (Assumption, Q3.)
4. **Convert.** For each recurring failure, export the session from the session
   service (Cloud SQL). Traces and the analytics table carry no message content (C4),
   so they cannot supply it. Then run
   `python .claude/skills/adk-agent-observability/scripts/events_to_eval_set.py --session <export> --out <file> --select tool_error`
   (or `--select all`) with `--redact-hook` set to the project redaction policy.
   Review the output by hand: write the reference answer, check redaction, and remove
   duplicates (A2).
5. **Place.** Add the reviewed case to `eval/support.evalset.json` with metadata:
   incident or fingerprint, `drift_mode`, `freshness_expires`, reviewer, and the old
   release's observed response kept beside the case (not in `final_response`).
   Cases that guided a fix go to the dev set; unseen reviewed cases go to the holdout.
   The PR gate (C5, D5) stays deterministic; do not add a model-judged check as a gate.
6. **Record.** Fill the row: `result`, `reviewer`, `evidence`, `recurring_failures`,
   `cases_added` (case ids). If a failure recurred but no case was added, say why
   (for example `not reproduced`).

## AQuA (optional, not installed)

`google/adk-recipes:agents-cli-aqua` is not installed here and cannot be fetched in
this session, so no `agents-cli aqua` command was run or checked. When adopted, install
it with the extension command in `adk-release-engineering`'s production-feedback
reference, then follow the installed `agents-cli-aqua` skill for the commands. Its
insights (`NEW`, `RECURRING`, `RESOLVED`) feed step 3 as candidates. Map its JSON
output onto the record's `recurring_failures` rows once the field names are known.
`RESOLVED` is confirmed against the case that fixed the failure, not the AQuA status.
An investigation that did not run in the window is `NOT RUN`. Until then the review is
manual and the manifest keeps "not yet automated".

## Open questions (nobody could answer; assumption in use)

- **Q1.** Did anyone review week 2026-W43? Assumed no: recorded `NOT RUN`.
- **Q2.** Should AQuA insights block a promotion? Assumed no (`insights_gate: false`);
  an insight is a candidate case. Priya decides; if yes, name the status and slice.
- **Q3.** What counts as "recurs" (A2)? Assumed the threshold in step 3.
- **Q4.** C4 says traces carry no message content, but AQuA reviews conversations
  from the analytics table. Confirm what `agent_events` stores before adopting AQuA.
- **Q5.** `eval/support.evalset.json` (34 cases) is named in the manifest but is not
  in this checkout, so no case was added and the case metadata was not checked
  against existing cases.
- **Q6.** Redaction policy module for `--redact-hook` is not defined in the repository.

## Verification status

Manual only: Priya reads the first weekly record. No automated check exists. Nothing
here was run against BigQuery or the session service.
