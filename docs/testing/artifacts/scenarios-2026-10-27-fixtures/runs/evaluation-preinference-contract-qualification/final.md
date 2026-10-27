I changed the code, but I couldn't run anything: Bash is disabled in this session, so none of the tests have been executed. The diagnosis and the fixes come from reading the code and counting characters by hand. Run `python -m unittest discover -s tests -t .` before you trust them. No provider calls were made, `runs/` and `campaign/ledger.json` are untouched, and nothing was installed.

**Why the saved runs failed**
- **r1 (`PQ-0007-r1`):** the prompt never told the model to cite labels, so all three findings came back unlabelled. The schema also didn't require `labels`.
- **r2 (`PQ-0007-r2`):** `render_pack` cut the rendered pack at 600 characters. By my count it is about 660, with the passage order putting the continuation and footnote last. That cut the continuation mid-text and dropped footnote 3 and the image line. The model then correctly reported that footnote 3 "is not in the passages". The larger model and extra thinking could not fix a prompt that lacked the evidence, so the $1.12 went on an input bug.
- **Strict check missing on the real path:** `run_qualification` called `check_findings` without `strict=True`, while the correction test uses strict. That test passed without proving the served route applied the same check.

**What I changed**
- **`pipeline/qualification.py`:**
  - Raised the size limit to 4000 characters, and a pack over it now raises `PackTooLarge` instead of being silently cut.
  - Added `preflight()`, which refuses before any send if a required passage, or a passage that one depends on, is missing from the selected pack.
  - The prompt now says to cite exact labels, to cite or list continuations, footnotes and headers, and to treat a no-text passage as unresolved.
  - The image passage appears as "no text available" instead of being dropped silently.
  - The route now calls `check_findings(..., strict=True)`.
- **`pipeline/contract.py`:** `labels` is now required, with at least one item, in the findings schema.
- **`tests/test_qualification_route.py` (new):** exercises `run_qualification` with `ScriptedTransport` and a temp checkpoint store. It checks:
  - the full pack reaches the prompt;
  - the prompt and schema ask for labels;
  - the corrected reference passes the route;
  - unlabelled results and results missing a footnote qualification are rejected, with the failure checkpoint kept;
  - an oversize pack and a pack missing a required footnote are refused with zero sends.

**Nothing loosened:** source spans, label rules, the ledger and the strict check are all unchanged or tighter.

**Not verified**
- `google-adk` isn't installed, so the real Runner path was not exercised, and I didn't imitate its events. `adk_qualification.py` calls the same `run_qualification`, so it picks up these changes, but that is by reading the code, not by running it.
- I don't have the reference findings or the invalid examples you hold. The reference in the correction test is one I could only check by hand against the pack. Please check it against the policy text and add your invalid examples as negative tests.
- I haven't checked that your gateway accepts this strict JSON schema. The schema doesn't set `additionalProperties: false` and leaves `qualifications` optional, which OpenAI-style strict mode normally rejects.

**Questions I couldn't ask, and what I assumed**
1. **Duplicate cell labels:** `occurrence_label` ignores the row, so cells `d7-c1` to `d7-c4` all get the label `D7-2024/p14/table-D7.1/c2`. The check therefore only requires one of the four cells to be cited, and "c2" resolves to whichever is last in the index. The correction test uses that label, so I left it alone and assumed you want to decide the label scheme. I'd add the row to the label and update the test and your reference findings together.
2. **Ledger:** the qualification route never reserves or settles against `campaign/ledger.json`, unlike the main workflow. I assumed adding that was outside this fix, but the route can currently spend without the allowance check. Wiring it in before the next paid run is worth doing.
3. **Size limit:** I assumed 600 characters was a prompt-size guess rather than a real limit, and chose 4000 to fit the pack with room to spare.

**Before the next paid run:** run the full offline suite, then ask Morgan Hale for approval for a single run on PQ-0007, with the ledger wiring and the label question settled first.