"""Read tickets, plan goals and design tables for the plan checks. Standard library only; never runs project code.

Shared by ``plan_status.py`` and ``check_tickets.py``. ``check_schedule.py``
keeps its own estimate parser; this module reads what that one skips: every
front-matter field, the acceptance items and the Evidence section a ticket
session writes (contract lines, ``actual:``, ``Rulings:``, resources and a
``Progress:`` block).
"""

from __future__ import annotations

from pathlib import Path
import re

from check_schedule import InputError, parse_range, read_plan

STATUSES = ("planned", "proposed", "ready", "in_progress", "blocked", "verified_local", "verified_live", "done")
FINISHED = ("verified_local", "verified_live", "done")
TYPES = ("implementation", "journey", "presentation", "teardown", "discovery", "governance", "portability")
ACCEPTANCE = re.compile(r"(?m)^\s*[-*]\s*\[([ xX])\]\s*(A\d+)\b(.*)$")
CONTRACT_ID = re.compile(r"(?<![\w/-])C\d+(?![\w/-])")
RULE_ID = re.compile(r"(?<![\w/-])SB\d+(?![\w/-])")
EVIDENCE_LINE = re.compile(r"(?<![\w/-])((?:C|SB)\d+)\s*:?\s*(evidenced|partially evidenced|partial|not evidenced|"
                           r"unproven|not run)\b[,;\s]*([^,;\n]*)", re.IGNORECASE)
ACTUAL = re.compile(r"(?mi)^\s*[-*]?\s*\**actual\**\s*:\s*(.+?)\s*$")
MANUAL_LINE = re.compile(r"(?mi)^\s*[-*]?\s*\**manual\**\s*:\s*(.+?)\s*$")
RESOURCE = re.compile(r"(?mi)^\s*[-*]?\s*([^:\n]+?):\s*(absent|retained|unknown)\b[^\n]*;\s*cleanup\s*:")
SETTLED = re.compile(r"\bsettled\s*:|→\s*D\d+|->\s*D\d+|\brejected\s*:", re.IGNORECASE)


def split_list(value: str) -> list[str]:
    """Split ``[a (x, y), b]`` at top-level commas so a purpose in parentheses stays with its item."""
    text = value.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    items, depth, current = [], 0, ""
    for char in text:
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        if char == "," and depth == 0:
            items.append(current)
            current = ""
        else:
            current += char
    items.append(current)
    cleaned = [i.strip().strip("'\"") for i in items]
    return [i for i in cleaned if i and i.lower() not in ("none", "empty", "-")]


def strip_comment(value: str) -> str:
    value = value.strip()
    if value[:1] in "'\"" and value[-1:] == value[:1] and len(value) >= 2:
        return value[1:-1]
    return value.split(" #", 1)[0].rstrip() if " #" in value else value


def front_matter(text: str, where: str) -> tuple[dict, str]:
    """Return (fields, body). List fields keep raw text; callers split them with ``split_list``."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        raise InputError(f"{where}: front matter is not closed")
    fields, parent = {}, None
    for raw in text[3:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise InputError(f"{where}: cannot read front-matter line {raw.strip()!r}")
        key, value = raw.split(":", 1)
        if raw[:1] in " \t" and parent is not None:
            fields[parent][key.strip()] = strip_comment(value)
            continue
        value = strip_comment(value)
        if value == "":
            fields[key.strip()], parent = {}, key.strip()
        else:
            fields[key.strip()], parent = value, None
    return fields, text[end + 4:].lstrip("\n")


def sections(body: str) -> dict[str, str]:
    """Map each ``## Heading`` (lower case) to its text."""
    found, marks = {}, list(re.finditer(r"(?m)^##\s+(.+?)\s*$", body))
    for index, mark in enumerate(marks):
        stop = marks[index + 1].start() if index + 1 < len(marks) else len(body)
        found[mark.group(1).strip().lower()] = body[mark.end():stop]
    return found


def acceptance_items(text: str) -> dict[str, dict]:
    return {m.group(2): {"checked": m.group(1).lower() == "x", "text": m.group(3)} for m in ACCEPTANCE.finditer(text)}


def label_block(text: str, label: str) -> list[str]:
    """Lines of a ``Label:`` block: the rest of its line plus the items nested under it.

    When the label is itself a list item (``- Rulings:``), only lines indented deeper belong to it, so a
    sibling item such as a resource line ends the block.
    """
    pattern = re.compile(rf"^(\s*)([-*]\s+)?\**{re.escape(label)}\**\s*:\s*(.*)$", re.IGNORECASE)
    found, out, indent, listed = False, [], 0, False
    for line in text.splitlines():
        if not found:
            match = pattern.match(line)
            if match:
                found, indent, listed = True, len(match.group(1)), bool(match.group(2))
                if match.group(3).strip():
                    out.append(match.group(3).strip())
            continue
        if not line.strip():
            if out:
                break
            continue
        depth = len(line) - len(line.lstrip())
        item = re.match(r"^\s*[-*]\s+", line)
        if depth > indent or (not listed and item and depth >= indent):
            out.append(line.strip().lstrip("-* ").strip())
        else:
            break
    return out


def read_evidence(text: str) -> dict:
    lines = {}
    for match in EVIDENCE_LINE.finditer(text):
        ident, state, rest = match.group(1), match.group(2).lower(), match.group(3).strip()
        tier = rest.lower()
        lines.setdefault(ident, []).append({"state": state, "tier": tier})
    actual_match = ACTUAL.search(text)
    actual = None
    if actual_match and not re.match(r"not reported|unknown|none", actual_match.group(1), re.IGNORECASE):
        try:
            actual = parse_range(re.sub(r"\s*(?:h|hours?)\b.*$", "", actual_match.group(1)), "actual")
        except InputError:
            actual = None
    rulings = [r for r in label_block(text, "Rulings") if r.lower() not in ("none", "-")]
    progress = label_block(text, "Progress")
    resources = [{"name": m.group(1).strip(), "state": m.group(2).lower()} for m in RESOURCE.finditer(text)]
    manual = [m.group(1).strip() for m in MANUAL_LINE.finditer(text)]
    return {"lines": lines, "actual": actual, "actual_reported": bool(actual_match), "manual": manual,
            "rulings": rulings, "open_rulings": [r for r in rulings if not SETTLED.search(r)],
            "progress": progress, "resources": resources}


def read_ticket(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fields, body = front_matter(text, str(path))
    if "goal" not in fields:
        return None
    parts = sections(body)
    evidence_text = parts.get("evidence", "")
    estimate = fields.get("estimate") if isinstance(fields.get("estimate"), dict) else {}
    try:
        total = parse_range(estimate.get("total") or fields.get("total"), f"{path} total")
    except InputError:
        total = None
    blocked = split_list(fields.get("blocked_by", "")) if isinstance(fields.get("blocked_by"), str) else []
    return {
        "goal": fields["goal"].strip(), "file": path, "fields": fields, "body": body, "sections": parts,
        "status": (fields.get("status") or "").strip().lower(), "type": (fields.get("type") or "").strip().lower(),
        "phase": str(fields.get("phase", "")).strip(), "total": total, "owner": str(fields.get("owner", "")).strip(),
        "blocked_by": blocked,
        "contracts": split_list(fields.get("contracts", "")) if isinstance(fields.get("contracts"), str) else [],
        "security": split_list(fields.get("security", "")) if isinstance(fields.get("security"), str) else [],
        "touches": split_list(fields.get("touches", "")) if isinstance(fields.get("touches"), str) else [],
        "deltas": split_list(fields.get("contract_deltas", "")) if isinstance(fields.get("contract_deltas"), str) else [],
        "acceptance": acceptance_items(parts.get("acceptance", "")),
        "evidence": read_evidence(evidence_text),
    }


def read_tickets(directory: Path) -> list[dict]:
    if not directory.is_dir():
        raise InputError(f"{directory}: not a directory")
    tickets = [t for t in (read_ticket(p) for p in sorted(directory.glob("*.md"))) if t]
    seen = {}
    for ticket in tickets:
        if ticket["goal"] in seen:
            raise InputError(f"goal {ticket['goal']} has two tickets: {seen[ticket['goal']].name} and {ticket['file'].name}")
        seen[ticket["goal"]] = ticket["file"]
    return tickets


def read_plan_goals(path: Path) -> list[dict]:
    """Schedule-block goals (as ``check_schedule`` reads them) plus the evidence written in each goal's section."""
    goals = read_plan(path)
    for goal in goals:
        section = goal.get("text", "")
        if not goal["status"]:
            match = re.search(r"Status and evidence:\**\s*([a-z_]+)", section)
            goal["status"] = match.group(1) if match and match.group(1) in STATUSES else ""
        goal["evidence"] = read_evidence(section.split("Status and evidence", 1)[-1]
                                         if "Status and evidence" in section else "")
        accepted = re.search(r"\*\*Acceptance:\*\*(.*?)(?:\n\s*-\s+\*\*|\Z)", section, re.DOTALL)
        goal["acceptance"] = ({m.group(1): {"checked": False, "text": m.group(2)}
                               for m in re.finditer(r"\b(A\d+)\b([^\n;]*)", accepted.group(1))} if accepted else {})
    return goals


def table_rows(path: Path, first_header: str, id_pattern: str, must_contain: tuple[str, ...] = ()) -> dict[str, dict]:
    """Rows of the first Markdown table whose header starts with ``first_header`` (case-insensitive)."""
    rows, header = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            header = None
            continue
        cells = [re.sub(r"[`*]", "", c).strip() for c in line.strip("|").split("|")]
        if header is None:
            lowered = [c.lower() for c in cells]
            if lowered and lowered[0].startswith(first_header) and all(any(m in c for c in lowered)
                                                                        for m in must_contain):
                header = lowered
            continue
        if set("".join(cells)) <= set("-: ") or not re.fullmatch(id_pattern, cells[0]):
            continue
        rows[cells[0]] = {"cells": dict(zip(header, cells)), "last": cells[-1], "row": line}
    return rows


def design_contracts(path: Path) -> dict[str, dict]:
    return table_rows(path, "id", r"C\d+", ("invariant", "enforcement"))


def design_rules(path: Path) -> dict[str, dict]:
    return table_rows(path, "rule", r"SB\d+", ("depth",))


def touches_overlap(a: list[str], b: list[str]) -> list[str]:
    """Paths written by both lists, treating a directory entry (trailing slash or prefix) as covering its files."""
    found = []
    for left in a:
        for right in b:
            l, r = left.rstrip("/"), right.rstrip("/")
            if l == r or r.startswith(l + "/") or l.startswith(r + "/"):
                found.append(left if len(left) >= len(right) else right)
    return sorted(set(found))
