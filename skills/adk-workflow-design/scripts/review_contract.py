"""Synthetic review-frame example. Stdlib only; no ADK or semantic verification.

Trusted application state owns all identities and associations. The model returns
judgments for fixed slots; publication policy is separate from shape acceptance.
See references/review-contracts.md before adapting this teaching example.
"""

from dataclasses import asdict, dataclass
import hashlib
import json


class ContractError(ValueError):
    """The response cannot be consumed under the current draft's contract."""


@dataclass(frozen=True)
class Evidence:
    id: str
    text: str


@dataclass(frozen=True)
class Issue:
    id: str
    question: str
    evidence_ids: tuple[str, ...]
    material: bool = True
    required_controls: tuple[str, ...] = ()
    contrary_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class Claim:
    id: str
    text: str
    issue_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class Draft:
    revision: str
    outcome: str
    claims: tuple[Claim, ...]
    controls: tuple[str, ...] = ()


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _index(values, name):
    result = {value.id: value for value in values}
    if len(result) != len(values) or any(not key for key in result):
        raise ContractError(f"{name}: duplicate or empty identity")
    return result


def compile_frame(draft, issues, evidence):
    """Compile from trusted, current state, including source text and revision.

    A hash binds content; it is not authentication. Never accept a client-supplied
    frame in place of recompiling from the application's owned state.
    """
    issue_by_id = _index(issues, "issues")
    source_by_id = _index(evidence, "evidence")
    _index(draft.claims, "claims")
    if not draft.revision or draft.outcome not in {"approve", "refuse", "unresolved"}:
        raise ContractError("draft: revision and known outcome required")
    if not issues:
        raise ContractError("at least one issue required")
    for issue in issues:
        if (len(set(issue.evidence_ids)) != len(issue.evidence_ids)
                or not set(issue.evidence_ids) <= source_by_id.keys()
                or not set(issue.contrary_ids) <= set(issue.evidence_ids)):
            raise ContractError("issue has duplicate, unknown or unlinked evidence")
    for claim in draft.claims:
        if (not claim.issue_ids or len(set(claim.issue_ids)) != len(claim.issue_ids)
                or not set(claim.issue_ids) <= issue_by_id.keys()):
            raise ContractError("claim needs known, unique issue associations")
        linked_sources = set().union(*(set(issue_by_id[key].evidence_ids)
                                      for key in claim.issue_ids))
        if (len(set(claim.evidence_ids)) != len(claim.evidence_ids)
                or not set(claim.evidence_ids) <= linked_sources):
            raise ContractError("claim evidence must belong to its established issues")
    payload = {
        "draft": asdict(draft),
        "issues": [asdict(issue) for issue in issues],
        "evidence": [asdict(source) for source in evidence],
    }
    frame = {"frame_id": hashlib.sha256(_json(payload).encode()).hexdigest(),
             "revision": draft.revision, "outcome": draft.outcome,
             "controls": list(draft.controls), "claims": {}, "issues": {}}
    for kind, values in (("claims", draft.claims), ("issues", issues)):
        for position, value in enumerate(values, 1):
            slot = {"identity": value.id,
                    "evidence": {f"s{n}": asdict(source_by_id[source_id])
                                 for n, source_id in enumerate(value.evidence_ids, 1)}}
            if kind == "claims":
                slot.update(text=value.text, issue_ids=list(value.issue_ids))
            else:
                slot.update(question=value.question, material=value.material,
                            required_controls=list(value.required_controls),
                            contrary_ids=list(value.contrary_ids))
            frame[kind][f"{kind[0]}{position}"] = slot
    return frame


def _object(properties):
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


def _enum(*values):
    return {"type": "string", "enum": list(values)}


def response_schema(frame):
    """The exact small schema consumed by consume_review, not a provider claim."""
    properties = {"frame_id": _enum(frame["frame_id"])}
    for kind in ("claims", "issues"):
        judgment = (_enum("supported", "unsupported", "uncertain", "contradicted")
                    if kind == "claims" else
                    _enum("acceptable", "adverse", "controlled", "unsupported",
                          "uncertain", "contradicted", "no_relevant_evidence"))
        properties[kind] = _object({
            key: _object({"judgment": judgment, "evidence": _object({
                source: _enum("supports", "contradicts", "irrelevant", "uncertain")
                for source in slot["evidence"]})})
            for key, slot in frame[kind].items()})
    return _object(properties)


def _validate_shape(value, schema, path="response"):
    # Deliberately supports only the object/string subset emitted above.
    if schema["type"] == "string":
        if not isinstance(value, str) or value not in schema["enum"]:
            raise ContractError(f"{path}: invalid value or stale frame")
        return
    if not isinstance(value, dict) or value.keys() != schema["properties"].keys():
        raise ContractError(f"{path}: exact slots required")
    for key, child in schema["properties"].items():
        _validate_shape(value[key], child, f"{path}.{key}")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def consume_review(raw, draft, issues, evidence, *, max_output_bytes):
    """Parse against a freshly compiled frame, then apply synthetic release rules.

    The caller owns authentication, atomic revision checking and actual release.
    No side effects occur here. Accepted model labels remain model judgments.
    """
    if max_output_bytes <= 0 or len(raw.encode("utf-8")) > max_output_bytes:
        raise ContractError("response exceeds the configured byte allowance")
    frame = compile_frame(draft, issues, evidence)
    schema = response_schema(frame)
    try:
        review = json.loads(raw, object_pairs_hook=_unique_object)
    except (ValueError, RecursionError) as error:
        raise ContractError(f"invalid JSON: {error}") from error
    _validate_shape(review, schema)
    blockers, warnings = [], []
    if draft.outcome == "unresolved":
        blockers.append("outcome: unresolved")
    if not draft.claims and draft.outcome != "unresolved":
        blockers.append("outcome: no decision claim")
    for key, slot in frame["claims"].items():
        assessment = review["claims"][key]
        values = assessment["evidence"].values()
        if (assessment["judgment"] != "supported" or "supports" not in values
                or any(value in {"contradicts", "uncertain"} for value in values)):
            blockers.append(f"claim {slot['identity']}: support unresolved")
    issue_judgments = {}
    for key, slot in frame["issues"].items():
        assessment = review["issues"][key]
        judgment = assessment["judgment"]
        issue_judgments[slot["identity"]] = judgment
        values = assessment["evidence"].values()
        problem = (judgment in {"unsupported", "uncertain", "contradicted",
                               "no_relevant_evidence"}
                   or "supports" not in values
                   or any(value in {"contradicts", "uncertain"} for value in values)
                   or bool(slot["contrary_ids"]))
        if problem:
            message = f"issue {slot['identity']}: {judgment}; evidence unresolved"
            (blockers if slot["material"] or draft.outcome == "approve"
             else warnings).append(message)
        if draft.outcome == "approve":
            missing = set(slot["required_controls"]) - set(draft.controls)
            if missing:
                blockers.append(f"issue {slot['identity']}: missing controls {sorted(missing)}")
            if judgment == "adverse":
                blockers.append(f"issue {slot['identity']}: adverse finding")
            if judgment == "controlled" and not slot["required_controls"]:
                blockers.append(f"issue {slot['identity']}: no registered control")
    if draft.outcome == "refuse" and not any(
            issue_judgments[identity] == "adverse"
            for claim in draft.claims for identity in claim.issue_ids):
        blockers.append("refusal: no reviewed adverse issue linked to a decision claim")
    return {"accepted": True, "publishable": not blockers,
            "blockers": blockers, "warnings": warnings,
            "sizes_bytes": {"frame": len(_json(frame).encode()),
                            "schema": len(_json(schema).encode()),
                            "response": len(raw.encode())}}
