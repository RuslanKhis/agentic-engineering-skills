G07 now has a written weekly procedure and a place in the release record, but no week has been reviewed yet. I didn't run any tests or commands, and nothing in this change touches `app/`, so `G05/A1` isn't affected.

**What I changed**
- **`docs/release/quality-loop.md`** (new) sets the rule that every ISO week ends with one record row. A row only counts as reviewed if it names a reviewer and evidence. Otherwise it says `NOT RUN`, which covers A1 and A3. The procedure is: read `agent_events`, group failures, convert recurring ones with `events_to_eval_set.py` and a redaction hook, review by hand, add to the eval set, and record the result (A2).
- **`release/manifest.yaml`** now has a `quality_reviews` block. Week 2026-W43 and the open week 2026-W44 are both recorded as `NOT RUN`, because I found no evidence of a review. `insights_gate` is set to `false`.

**What I left undone**
- **A1 and A2 can't be checked yet.** Priya's read of the first real weekly record is still the only check. The G07 ticket's Evidence section is also still empty.
- **No eval case was added.** `eval/support.evalset.json` is named in the manifest but isn't in this checkout.
- **AQuA was not used.** The `agents-cli-aqua` skill isn't installed and I had no network. The doc says AQuA is optional and unverified, and the manifest still says "not yet automated".

**Questions nobody could answer, and what I assumed** (all in the doc)
1. Did anyone review W43? I assumed no.
2. Should AQuA insights block a promotion? I assumed no, so they only open candidate cases. Priya should decide.
3. What counts as a failure that "recurs"? I assumed the same fingerprint in two or more weeks, or three or more times in one week.
4. C4 says traces carry no message content, yet AQuA reviews conversations from the analytics table. Someone needs to confirm what `agent_events` actually stores before adopting AQuA.
5. The redaction module for the converter's `--redact-hook` isn't defined in the repo.