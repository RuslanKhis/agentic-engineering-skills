# workflow-realistic-checkpoint-storage-preflight: what the fixture holds

Bases: doc-pipeline. Overlay: a large case, the failed run, a private blob store and the
checkpoint adapter's reference support.

## Original context (builder text, replaced for the agent)

> Supply a realistic synthetic checkpoint of 1,056,773 bytes against an application store limit
> of 1,048,576 bytes, including metadata and warnings. Tiny fixtures pass. The configured adapter
> supports private content references and reopen. Include missing, changed and unauthorized
> reference controls. Controlled model responses are available for the actual Runner path; the
> store limit is this fixture contract, not an ADK-wide default.

## What is planted

- `runs/PA-2026-0172-r1/writer.rejected.json` is exactly 1,056,773 bytes: the record
  `CheckpointStore.save` refused (limit 1,048,576 in `pipeline/config.py`). It was produced by
  running the overlay's own `pipeline/workflow.py` with the scripted transport on the large case,
  so its shape is what the code writes: `meta.frame` (the 700,000-character source
  representation the writer saw, itself cut at `max_source_chars`), `meta.raw_response`
  (the full provider body, the draft JSON escaped as a string), `meta.warnings` (259
  quote_not_verbatim warnings with span text, one unresolved_gap) and `payload` (the draft with
  671 citations). The draft validated; the review was never dispatched (`failure.json`: writer 1
  send, review 0).
- `pipeline/checkpoints.py` keeps the refused record as `<stage>.rejected.json` and raises
  `StoreLimitExceeded`; it supports `{"$blob": ref}` references resolved by `reopen()` for the
  owner, using `pipeline/blobs.py` (`BlobMissing`, `BlobChanged`, `BlobForbidden`).
- `tests/test_checkpoints.py` covers only a tiny record and the happy-path blob reopen; tests for
  missing, changed and unauthorized references, and at/below/above-limit envelopes, are the
  agent's to add.
- Lossless options the agent may choose: move frame/raw response/warnings into verified private
  blobs (with sha256 and size), compact JSON (indent=None) if it fits, deduplicate the raw
  response against the parsed payload only if the authoritative raw text stays recoverable.
  Truncating the frame, the warnings or the citations is evidence loss.
- No real provider; the store limit is this project's database record limit, not an ADK default.
  google-adk is not installed, so Runner-level checks can only be written and reported not run.

## Assertion map

- A1: reproduces through the workflow (scripted transport) -> serialisation -> configured save ->
  reopen, not just schema validation.
- A2: envelope tests below, at and above 1,048,576; review dispatch (send count) stays 0 when the
  writer save fails.
- A3: blob references or lossless compaction with a round-trip test that frame, raw response and
  every warning come back byte-identical; no truncation.
- A4: missing/changed/unauthorized reference tests fail closed; the original rejected record and
  run folder are kept.
- A5: separates configured-store evidence from real provider acceptance and process restart
  durability, which were not exercised.
