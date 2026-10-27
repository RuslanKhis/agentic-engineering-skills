"""Application checks on policy-qualification findings."""
from __future__ import annotations

from pipeline.labels import label_index, occurrence_label

FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["findings"],
    "properties": {
        "findings": {"type": "array", "items": {
            "type": "object",
            "required": ["statement", "support"],
            "properties": {
                "statement": {"type": "string"},
                "support": {"type": "string", "enum": ["supported", "unsupported", "unresolved"]},
                "labels": {"type": "array", "items": {"type": "string"}},
                "qualifications": {"type": "array", "items": {"type": "string"}},
            },
        }},
    },
}


def check_findings(result: dict, pack: dict, strict: bool = False) -> list[str]:
    """Return the problems with a qualification result; empty means accepted.

    strict also requires each finding that cites a passage to carry the qualifications
    of every passage it requires (continuations, footnotes).
    """
    errors = []
    by_id = {p["id"]: p for p in pack["passages"]}
    index = label_index(pack["passages"])
    required_labels = {occurrence_label(by_id[i]) for i in pack["required"]}
    cited = set()
    for n, finding in enumerate(result.get("findings", []), 1):
        labels = finding.get("labels") or []
        if not labels:
            errors.append(f"finding {n} has no labels")
        for label in labels:
            if label not in index:
                errors.append(f"finding {n} cites unknown label {label}")
            cited.add(label)
        if strict:
            needed = {occurrence_label(by_id[r]) for label in labels if label in index
                      for r in index[label].get("requires", [])}
            missing = needed - set(finding.get("qualifications") or []) - set(labels)
            if missing:
                errors.append(f"finding {n} omits qualifications {sorted(missing)}")
    for label in sorted(required_labels - cited):
        errors.append(f"required passage {label} is not cited")
    return errors
