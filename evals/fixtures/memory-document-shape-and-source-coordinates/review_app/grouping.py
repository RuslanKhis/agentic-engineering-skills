"""Turn the records selected for a question into the units the writer and reviewer see.

Input: extracted records (extract/records.jsonl) and the selected pack, an
ordered list of record IDs from the retriever. Output: units with a key, the
text and the pages they came from. Units longer than MAX_UNIT_CHARS are split
so each fits the writer's per-source budget.
"""
from __future__ import annotations

GROUPER_VERSION = "g-2026.09.30"
MAX_UNIT_CHARS = 160
SKIP_KINDS = {"footnote", "page_image"}


def unit_key(record: dict) -> str:
    if record["kind"].startswith("table"):
        return f"{record['document']}:{record['table_id']}"
    return f"{record['document']}:{record['label']}"


def _render_table_cell(record: dict) -> str:
    return record["text"]


def group_for_pack(records: dict[str, dict], pack: list[str]) -> list[dict]:
    units: dict[str, dict] = {}
    last_key = None
    seen_cells: set[tuple[str, str]] = set()
    for record_id in pack:
        record = records[record_id]
        if record["kind"] in SKIP_KINDS:
            continue
        if record.get("continues") and last_key is not None:
            units[last_key]["text"] += " " + record["text"]
            units[last_key]["pages"].append(record["page"])
            continue
        key = unit_key(record)
        unit = units.setdefault(key, {"key": key, "text": "", "pages": [], "record_ids": []})
        if record["kind"] == "table_cell":
            cell = (record["table_id"], record["text"])
            if cell in seen_cells:
                continue
            seen_cells.add(cell)
            piece = _render_table_cell(record)
        else:
            piece = record["text"]
        unit["text"] = (unit["text"] + " " + piece).strip()
        unit["record_ids"].append(record_id)
        if record["page"] not in unit["pages"]:
            unit["pages"].append(record["page"])
        last_key = key
    return [part for unit in units.values() for part in split_unit(unit)]


def split_unit(unit: dict) -> list[dict]:
    text = unit["text"]
    if len(text) <= MAX_UNIT_CHARS:
        return [unit]
    parts = []
    for index, start in enumerate(range(0, len(text), MAX_UNIT_CHARS)):
        parts.append({**unit, "key": f"{unit['key']}#{index + 1}", "text": text[start:start + MAX_UNIT_CHARS]})
    return parts
