I have no shell tool in this session, so I couldn't run the test suite. The changes are written but untested.

## What I did
**Cause:** the PA-2026-0172 writer checkpoint was 1,056,773 bytes against a 1,048,576 limit. Most of it is the audit evidence in `meta` (`frame`, `raw_response`) plus the draft's many citations. `save()` could only refuse the record.

**Fix:**
- **`pipeline/checkpoints.py`:** when a record is over the limit and a blob store and owner are configured, `save()` moves the largest top-level fields to the private blob store. It takes `meta` fields first, then `payload` fields, and stops once the record fits. Each field is stored whole and replaced by `{"$blob": ref}`, so nothing is truncated or dropped. `reopen()` already resolves these references for the owner, and other callers get `BlobForbidden`.
- **No blob store or owner:** behaviour is unchanged. The record is refused and kept as `<stage>.rejected.json`.
- **`from_settings()`:** both `pipeline/workflow.py` and `pipeline/adk_app.py` now build the store through it, so the served ADK route gets the same fix. `adk_app.py` remains the only module that imports `google.adk`.
- **`pipeline/config.py`:** new `blob_dir = "blobs"` setting.
- **Tests:**
  - `tests/test_checkpoints.py` adds a spill round-trip with an owner check, and a still-refused case when there is no blob store.
  - `tests/test_pipeline.py` adds an end-to-end `run_case` with `ScriptedTransport` and a small limit.

I made no provider calls, and I didn't touch `runs/` or `campaign/ledger.json`.

## Not done
- **Tests:** run `python -m unittest discover -s tests -t .` before merging. This is `offline: not run`. I didn't read the real 1 MB record, so I haven't confirmed that spilling `meta` alone brings it under the limit. The code falls back to `payload` fields if it doesn't.
- **PA-2026-0172:** I didn't re-run it. A new run would need a writer call (reserved at $0.40) and a review call ($0.25), and both need your approval. The refused writer record in `runs/PA-2026-0172-r1` already has the full draft, so you could instead save it into a new run directory (`-r2`) and pay only for the review. I haven't written that recovery step.
- **ADK route:** `google-adk` isn't installed, so the ADK route is unexercised.

## Questions and assumptions
- **Who is the blob owner?** Nothing in the repo defines it. I assumed it comes from the `CASE_TEAM` environment variable. If that variable is unset, spilling is disabled and the old refusal applies. Please confirm the right source, such as a case field.
- **Blob lifetime:** blobs live under `blobs/<owner>/` and aren't part of `runs/`. They need to be retained as long as the run is.