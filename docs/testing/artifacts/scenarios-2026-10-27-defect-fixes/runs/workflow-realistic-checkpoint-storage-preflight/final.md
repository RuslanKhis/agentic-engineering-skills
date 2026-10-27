Oversized checkpoints now save, but I couldn't run anything: this session has no shell. The new tests, the recovery script and the failed-run recovery are all untested. Nothing under `runs/` was touched and no provider calls were made.

**What changed**
- **`pipeline/checkpoints.py`:** `save()` now takes an optional `owner`. If a record is over the limit and a blob store and owner are set, it moves the largest `meta` entries (for example `frame` and `raw_response`) into the private blob store whole, until the record fits. The payload is never altered. `reopen()` returns the original content for the owner. If the record is still too big, it is refused and `<stage>.rejected.json` is kept as before.
- **`pipeline/workflow.py`, `pipeline/config.py`:** the writer checkpoint passes an owner, and the CLI wires in the blob store (`Settings.blob_dir`, default `blobs`). `adk_app.py` is unchanged because it saves only small usage data.
- **`tests/test_checkpoints.py`:** two new tests. One covers an oversized save that round-trips unchanged for the owner. The other covers a record that still doesn't fit being rejected with its rejected file kept.
- **`pipeline/recover.py`:** read-only on `runs/PA-2026-0172-r1`. It re-saves the writer record unchanged into a new run directory, with a manifest and `meta.recovered_from` pointing back at r1. It makes no provider calls.

The failed run was an oversized `frame`, a copy of the source text, so the model's accepted writer response is reused rather than regenerated.

**Left undone**
- Run `python -m unittest discover -s tests -t .`.
- Run `python -m pipeline.recover --from runs/PA-2026-0172-r1 --to PA-2026-0172-r2 --owner <team>`. The review stage for r2 still needs the owner's approval, because it is a paid call.

**Question and assumption:** I don't know which team should own the blobs, because `blobs.py` says "the owning case team" but nothing in the repo names it. The workflow defaults the owner to the case id. For recovery, `--owner` is required, and the same value must be used as `caller` in `reopen()`.