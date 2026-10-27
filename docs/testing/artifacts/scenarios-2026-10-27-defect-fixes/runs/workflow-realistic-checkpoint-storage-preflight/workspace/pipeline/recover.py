"""Re-save a refused checkpoint into a NEW run directory, with no provider call.

The source run is only read. Its writer record (payload and meta, unchanged) is saved again
through the store, which now moves oversized meta into the private blob store by reference.

    python -m pipeline.recover --from runs/PA-2026-0172-r1 --to PA-2026-0172-r2 --owner <case team>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.blobs import PrivateBlobStore
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings


def recover(src_run: Path, new_run_id: str, owner: str, settings: Settings, stage: str = "writer") -> Path:
    rejected = json.loads((src_run / f"{stage}.rejected.json").read_text(encoding="utf-8"))
    store = CheckpointStore(settings.checkpoint_dir, settings.checkpoint_limit_bytes,
                            PrivateBlobStore(settings.blob_dir))
    if (store.root / new_run_id).exists():
        raise FileExistsError(f"{new_run_id} already exists; pick a new run id")
    manifest = json.loads((src_run / "manifest.json").read_text(encoding="utf-8"))
    store.write_manifest(new_run_id, {**manifest, "run_id": new_run_id, "recovered_from": src_run.name,
                                      "recovered_stage": stage})
    meta = {**rejected["meta"], "recovered_from": {"run": src_run.name, "saved_at": rejected["saved_at"]}}
    return store.save(new_run_id, stage, rejected["payload"], meta, owner=owner)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="src", type=Path, required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--owner", required=True)
    args = parser.parse_args()
    print(recover(args.src, args.to, args.owner, Settings.from_env()))


if __name__ == "__main__":
    main()
