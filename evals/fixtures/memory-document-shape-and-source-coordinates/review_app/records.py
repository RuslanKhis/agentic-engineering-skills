"""Load the extracted records written by the extraction job."""
from __future__ import annotations

import json
from pathlib import Path


def load_records(path: str | Path) -> dict[str, dict]:
    records = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                record = json.loads(line)
                records[record["record_id"]] = record
    return records
