#!/usr/bin/env python3
"""Append the labelled held-out cases to evals/activation.json as text (27 October 2026).

Reads labels.json and the raw generator replies beside this file, takes each kept
request verbatim, and inserts the cases before the closing bracket of the cases
array so that every existing case stays byte-for-byte unchanged. Refuses to run
when any held-out id is already present.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from model_backends import extract_json  # noqa: E402

TAIL = "\n    }\n  ]\n}\n"


def main() -> int:
    labels = json.loads((HERE / "labels.json").read_text(encoding="utf-8"))["labels"]
    path = ROOT / "evals" / "activation.json"
    text = path.read_text(encoding="utf-8")
    existing = {case["id"] for case in json.loads(text)["cases"]}
    blocks = []
    for label in labels:
        if label.get("dropped"):
            continue
        if label["id"] in existing:
            raise SystemExit(f"{label['id']} is already in activation.json")
        raw_name, index = label["source"]
        raw = json.loads((HERE / "raw" / raw_name).read_text(encoding="utf-8"))
        request = extract_json(raw["reply_text"])["requests"][index - 1]
        expected_kind = "fits" if label["should_trigger"] else "elsewhere"
        if request["kind"] != expected_kind:
            raise SystemExit(f"{label['id']}: source is {request['kind']}, label expects {expected_kind}")
        rationale = "held-out, generated from a neutral brief" + (
            "." if label["should_trigger"] else f"; belongs to {label['destination']}.")
        fields = [("id", label["id"]), ("skill", label["skill"]), ("prompt", request["text"]),
                  ("should_trigger", label["should_trigger"]), ("rationale", rationale),
                  ("split", "heldout")]
        body = ",\n".join(f"      {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in fields)
        blocks.append("    {\n" + body + "\n    }")
    if not text.endswith(TAIL):
        raise SystemExit("activation.json does not end as expected; append by hand")
    text = text[: -len(TAIL)] + "\n    },\n" + ",\n".join(blocks) + "\n  ]\n}\n"
    json.loads(text)
    path.write_text(text, encoding="utf-8")
    print(f"appended {len(blocks)} held-out cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
