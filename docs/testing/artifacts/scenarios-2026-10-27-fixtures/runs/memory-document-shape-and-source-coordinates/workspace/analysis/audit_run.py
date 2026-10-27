"""Read-only audit of runs/run-0412: where does each record's text go between extract, pack and units?

Usage: python3 analysis/audit_run.py <workspace_root>
Uses only saved data; no model calls, no writes.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
from review_app.grouping import group_for_pack, MAX_UNIT_CHARS  # noqa: E402
from review_app.records import load_records  # noqa: E402
from review_app.storage import EnvelopeStore  # noqa: E402

store = EnvelopeStore(root / "runs")
manifest = json.loads((root / "runs/run-0412/manifest.json").read_text())
env = {}
for stage, eid in manifest["envelopes"].items():
    env[stage] = store.get(eid)  # digest-checked
print("envelopes reopened with digest check:", sorted(env))

records = load_records(root / "extract/records.jsonl")
ext_manifest = json.loads((root / "extract/manifest.json").read_text())
print(f"extract: {len(records)} records (manifest says {ext_manifest['records']})")

pack = env["select_pack"]["payload"]["record_ids"]
units = env["group"]["payload"]["units"]
print(f"pack: {len(pack)} ids (top_k={env['select_pack']['producer']['top_k']}), unique {len(set(pack))}")

# 1. Does today's grouper reproduce the saved group envelope?
again = group_for_pack(records, pack)
print("grouper reproduces saved units:", again == units)

# 2. Retrieval coverage: records the pack never selected, by page/kind
missing = [r for r in records if r not in pack]
print("\nNOT in pack:", [(r, records[r]["page"], records[r]["kind"]) for r in missing])
print("pack in document order:", pack == sorted(pack))

# 3. Key collisions: same unit key built from different clause_paths
by_key = {}
for rid in pack:
    rec = records[rid]
    if rec["kind"] in {"footnote", "page_image"}:
        continue
    k = f"{rec['document']}:{rec['table_id']}" if rec["kind"].startswith("table") else f"{rec['document']}:{rec['label']}"
    by_key.setdefault(k, set()).add(tuple(rec["clause_path"]))
print("\nkeys covering >1 clause path (non-table):")
for k, paths in by_key.items():
    if len(paths) > 1 and "T4.1" not in k:
        print("  ", k, sorted(paths))

# 4. Per-record accounting
norm = lambda s: re.sub(r"\s+", " ", s).strip()
joined = {}
for u in units:
    base = u["key"].split("#")[0]
    joined[base] = joined.get(base, "") + u["text"]
alltext = " ".join(joined.values())
in_units = set()
for u in units:
    in_units.update(u["record_ids"])
dropped, wrong_home, nowhere = [], [], []
for rid in pack:
    rec = records[rid]
    if rec["kind"] in {"footnote", "page_image"}:
        continue
    if rid not in in_units:
        dropped.append(rid)
    t = norm(rec["text"])
    if t and t not in norm(alltext):
        nowhere.append(rid)
print("\npack records listed in no unit's record_ids:", dropped)
print("pack records whose text is absent from every unit (cut/lost):", nowhere)
# the two classes separately, to show text-present-but-unattributed
print("text present but not attributed (continuations):",
      [r for r in dropped if norm(records[r]["text"]) in norm(alltext)])

# 5. Table cell loss by (row, col)
cells = [r for r in pack if records[r]["kind"] == "table_cell"]
lost = [(r, records[r]["row"], records[r]["col"], records[r]["text"]) for r in cells if r not in in_units]
print(f"\ntable cells in pack: {len(cells)}; dropped by (table, text) de-dup: {len(lost)}")
for x in lost:
    print("  ", x)
rows = Counter(records[r]["row"] for r in cells)
print("rows present in pack:", dict(rows), "| table rows in extract:",
      sorted({r['row'] for r in records.values() if r.get('table_id') and 'row' in r}))

# 6. Split points
print(f"\nsplits (MAX_UNIT_CHARS={MAX_UNIT_CHARS}):")
for u in units:
    if "#" in u["key"]:
        print(f"  {u['key']}: starts {u['text'][:18]!r} ends {u['text'][-18:]!r}; record_ids {len(u['record_ids'])}, pages {u['pages']}")

# 7. Largest unit pre-split vs envelope store: adapter has no size limit (storage.py docstring)
print("\nlongest pre-split unit chars:", max(len(joined[k]) for k in joined))
