I reached a diagnosis and made the offline repairs, but none of it has been run: I had no shell, so no tests ran. No provider call was made and no file under `attempts/`, `probes/`, `campaign/` or `runs/` was touched. The first thing to do is `python -m unittest discover -s tests -t .`. I expect 5 old and 6 new tests to pass, but I haven't seen that.

One mistake: I first tried to write a helper script outside the workspace. It was denied and I didn't retry it.

**Why green tests and red runs**
- **Batch 3, four 400s:** the writer schema (draft-v6) had condition-template text containing line breaks as enum values, and the gateway rejects that. The 22 October writer probe shows this directly. The earlier "gateway instability" diagnosis was wrong for these four.
- **22 October review probe:** it only sent a one-field `{"ok": boolean}` schema. It can't support "transient", so I withdrew that conclusion without editing the file.
- **Batch 2, case 0146:** a policy sentence wraps over two source lines (`p31:7` and `:8`), and the writer cited only the first. The reviewer was right. The reference draft in the local tests had the same flaw, citing line 4 of a three-line sentence.
- **Never exercised:** `export` reads `c["text"]`, which no draft shape contains, so any draft with conditions would have failed there. The scripted test transport accepts any request, so none of this could show up locally.
- **Stop rule:** two same-stage failures should have stopped batch 3, but all six cases were sent. No code enforces the rule.

**What I changed (spans, cohort rules, ledger and pins untouched)**
- **Schema:** it is now draft-v7. Conditions are chosen by `template_id` and the server owns the text.
- **Citation check:** the writer stage now rejects a citation that cuts off a wrapped sentence, and the check names the missing span.
- **Prompt:** writer-v8 tells the model to cite every line of a wrapped sentence.
- **Export:** it now renders condition text from the template id.
- **Tests:** six new tests, including a rejecting transport that models only the one rule observed in the probe, with a negative control. I also corrected two reference citations in the existing tests.

**The plan for the next paid run**
The re-entry record is in `reentry/2026-10-27/record.md`. It proposes a diagnostic canary (one writer and one review send on PA-2026-0141, no retries, about $0.65), then fixed cohort A only if the canary passes. The cohort rules stay unchanged and cohort A is estimated at $3.90 reserved. The ledger shows $16.63 remaining after $0.80 of unsettled reservations.

**Left undone or unknown**
- No source, config or code hashes (no shell), and no batch driver to enforce the stop rule.
- Fixtures for five of the six cohort cases aren't in this workspace, so nothing was checked against them.
- The cause of the two batch 3 timeouts is unknown. Their $0.80 stays uncertain until the provider's usage record settles it.
- It is untested whether the gateway accepts the whole draft-v7 schema or the real review schema.
- `validate_review` still accepts "accept" beside an unsupported claim.

**Questions I couldn't ask (assumptions in the record)**
- I assumed neither phase is approved, so nothing is sent until Morgan Hale confirms. Does AP-1 cover a diagnostic canary on a cohort case, and do you approve it and the cohort run?
- Where are the other five cohort fixtures and the officer labels?
- Can the usage records for the two timed-out calls be obtained?
- Must a citation include the whole wrapped sentence? I assumed yes.