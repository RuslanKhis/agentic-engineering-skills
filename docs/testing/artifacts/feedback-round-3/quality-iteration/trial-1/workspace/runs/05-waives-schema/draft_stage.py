#!/usr/bin/env python3
"""Draft stage for the quality-iteration trial seed. Standard library only.

Loads cases/*.json, builds a request from prompt.txt plus the case inputs,
calls ``model(request)`` and writes outputs/<case>.json. ``model`` is a
deterministic rule-based MODEL DOUBLE, not a real model and not a provider
call. It exists so that improvements to the prompt, the inputs and retrieval
are observable in the outputs. It never reads a case label.

What the double does, in plain words (each trigger is a line in ``model``):

* It cites only policies whose text appears in the request. A policy that
  retrieval did not supply is never cited, so the output misses it.
* It refuses only when Policy H3's text is present and a fact says the
  extension projects more than 3.0 m beyond an attached neighbour. Without
  H3 in the request it approves.
* When the request lists facts as plain lines with the source IDs in a
  separate list (the current prompt's "FACTS ... SOURCE IDS" layout), the
  double attributes every measurement in the case to the source of the first
  measurement it saw. When facts are labelled inline as "[source-id] text",
  it attributes each measurement to its own source.
* When Policy G4's text is present, it imposes the Table 2 visibility splay
  as a condition, unless the request shows how a written waiver is handled:
  either an exemplar decision whose text contains "waived" or "not required",
  or a "waives" field in the output schema. With that shown, it reads the
  facts for a written waiver and omits the splay.
* When the request contains two or more exemplar decisions (blocks beginning
  "EXEMPLAR"), conditions are written as {"purpose", "text"} objects.
  Otherwise conditions are free-text strings.
* When the request exceeds REQUEST_BYTE_LIMIT bytes, the double returns
  truncated text that is not valid JSON; the stage records a schema failure
  for that case. The limit is a stand-in for a provider output/input cap.

Run from this directory: ``python3 draft_stage.py``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
POLICY_SET = HERE / "policies.json"
# Retrieval repair (iteration 1). Policies named inside a retrieved policy's
# text are looked up by these aliases; the policy ID itself is always an alias.
CROSS_REFERENCE_ALIASES = {"SPD-T2": ("Table 2 of the Design SPD", "Design SPD Table 2")}
# Words that occur in most policies and carry no applicability signal.
RETRIEVAL_STOPWORDS = {"shall", "where", "that", "with", "than", "more", "such", "from", "there", "will",
                       "this", "before", "least", "unless", "onto", "into", "each", "when", "only", "also"}
RETRIEVAL_MIN_TERMS = 2
REQUEST_BYTE_LIMIT = 10_500
MEASUREMENT = re.compile(r"\b\d+(?:\.\d+)?\s?(?:m|sq m|mph)\b")


def load_cases() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted((HERE / "cases").glob("dev-*.json"))]


def _terms(text: str) -> set[str]:
    """Content words of four or more letters, singularised naively."""
    words = re.findall(r"[a-z][a-z-]{3,}", text.lower())
    return {w[:-1] if w.endswith("s") else w for w in words} - RETRIEVAL_STOPWORDS


def retrieve(case: dict) -> list[str]:
    """Deterministic retrieval repair over policies.json. Adds, in place, any
    policy that (1) is named inside the text of a policy already retrieved,
    or (2) shares at least RETRIEVAL_MIN_TERMS content terms with the case
    facts. Returns the IDs added. Never reads the label."""
    policy_set = json.loads(POLICY_SET.read_text())["policies"]
    have = {p["policy_id"] for p in case["retrieved_policies"]}
    fact_terms = _terms(" ".join(f["text"] for f in case["facts"]))
    added: list[str] = []
    for pid, policy in policy_set.items():
        if pid in have:
            continue
        aliases = (pid, f"Policy {pid}") + CROSS_REFERENCE_ALIASES.get(pid, ())
        cross_referenced = any(a in p["text"] for p in case["retrieved_policies"] for a in aliases if a != pid)
        applicable = len(_terms(policy["text"]) & fact_terms) >= RETRIEVAL_MIN_TERMS
        if cross_referenced or applicable:
            case["retrieved_policies"].append({"policy_id": pid, "heading": policy["heading"], "text": policy["text"]})
            have.add(pid)
            added.append(pid)
    return added


def build_request(prompt: str, case: dict) -> str:
    """Render the request exactly as the current prompt asks: facts as plain
    lines, source IDs in a separate list, then the policies."""
    lines = [prompt.rstrip(), "", "FACTS"]
    lines += [fact["text"] for fact in case["facts"]]
    lines += ["", "SOURCE IDS", ", ".join(fact["source_id"] for fact in case["facts"]), "", "POLICIES"]
    for policy in case["retrieved_policies"]:
        lines += [f"{policy['policy_id']}: {policy['heading']}", policy["text"], ""]
    return "\n".join(lines)


def _facts(request: str, case: dict) -> list[dict]:
    inline = all(f"[{fact['source_id']}]" in request for fact in case["facts"])
    facts = []
    first_measurement_source = None
    for fact in case["facts"]:
        measurements = MEASUREMENT.findall(fact["text"])
        source = fact["source_id"]
        if measurements:
            if first_measurement_source is None:
                first_measurement_source = source
            elif not inline:
                source = first_measurement_source  # trigger: wrong attribution
        facts.append({"source_id": source, "text": fact["text"], "measurements": measurements})
    return facts


def model(request: str, case: dict) -> str:
    """Deterministic MODEL DOUBLE. See the module docstring for each trigger."""
    if len(request.encode("utf-8")) > REQUEST_BYTE_LIMIT:
        return '{"decision": "approve", "reasons": [{"issue": "parking", "policy_ids": ["T2"], "fin'
    present = [p for p in case["retrieved_policies"] if p["text"] in request]
    ids = {p["policy_id"] for p in present}
    facts = _facts(request, case)
    exemplars = request.count("EXEMPLAR") >= 2
    waiver_aware = '"waives"' in request or re.search(r"EXEMPLAR[\s\S]*?(waived|not required)", request) is not None
    harmful = "H3" in ids and any(
        float(m.split()[0]) > 3.0 for f in facts if "beyond the rear wall" in f["text"]
        for m in f["measurements"] if m.endswith(" m"))
    decision = "refuse" if harmful else "approve"

    def finding(keyword: str) -> str:
        for f in facts:
            if keyword in f["text"]:
                return f"{f['text']} ({f['source_id']})"
        return "No fact bears on this policy."

    reasons, conditions = [], []
    for policy in present:
        pid = policy["policy_id"]
        if pid == "H3":
            text = finding("beyond the rear wall") if harmful else next((f"{f['text']} ({f['source_id']})" for f in facts if f["measurements"]), "No measured fact supplied.")
            reasons.append({"issue": "scale and neighbour amenity", "policy_ids": ["H3"],
                            "finding": ("Projection beyond the attached neighbour exceeds 3.0 m, contrary to H3(c): " if harmful
                                        else "Subordinate scale and amenity acceptable under H3: ") + text})
        elif pid == "D1":
            reasons.append({"issue": "materials", "policy_ids": ["D1"], "finding": "Materials: " + finding("match")})
            if decision == "approve":
                conditions.append(("design quality", "External materials shall match those specified on the drawings."))
        elif pid == "T2":
            reasons.append({"issue": "parking", "policy_ids": ["T2"], "finding": "Parking: " + finding("two cars")})
            conditions.append(("parking", "Two off-street parking spaces shall be retained."))
        elif pid == "G4":
            waived = waiver_aware and any(re.search(r"not required|waive", f["text"]) for f in facts)
            reasons.append({"issue": "highway safety", "policy_ids": ["G4"],
                            "finding": ("Setback acceptable and splay waived in writing: " if waived else "Setback acceptable: ") + finding("set back")})
            if waived:
                conditions.append(("highway safety", "The gate shall open inward and remain set back at least 5.0 m from the carriageway edge."))
            else:
                conditions.append(("highway safety", "A visibility splay of 2.4 m by 43 m shall be provided before the gate is first used."))
        elif pid == "SPD-T2":
            reasons.append({"issue": "visibility splay", "policy_ids": ["SPD-T2"], "finding": "Table 2 applies to a classified road: " + finding("classified")})
    if decision == "refuse":
        conditions = []
    out = {"decision": decision, "reasons": reasons,
           "conditions": [{"purpose": p, "text": t} if exemplars else f"{t}" for p, t in conditions],
           "facts_used": [{"source_id": f["source_id"], "measurements": f["measurements"]} for f in facts if f["measurements"]]}
    return json.dumps(out)


def main() -> None:
    prompt = (HERE / "prompt.txt").read_text()
    out_dir = HERE / "outputs"
    out_dir.mkdir(exist_ok=True)
    for case in load_cases():
        added = retrieve(case)
        request = build_request(prompt, case)
        raw = model(request, case)
        try:
            record = {"case": case["id"], "schema_valid": True, "output": json.loads(raw)}
        except json.JSONDecodeError as exc:
            record = {"case": case["id"], "schema_valid": False, "error": str(exc), "raw": raw}
        record["request_bytes"] = len(request.encode("utf-8"))
        record["retrieval_added"] = added
        (out_dir / f"{case['id']}.json").write_text(json.dumps(record, indent=2) + "\n")
        print(case["id"], "schema_valid" if record["schema_valid"] else "SCHEMA FAILURE", record["request_bytes"], "bytes")


if __name__ == "__main__":
    main()
