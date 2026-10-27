"""Reader-facing safeguards for the writer's draft, in plain code (stdlib only, no model).

Adapted from the draft-consistency helper to this pipeline's draft shape: reasons carry
`citations` (span ids), conditions carry `reason_id`, and gaps are "stage: message" strings.
The draft has no structured `requires`/`waives` fields, so the waiver check reads the prose;
see `waiver_conflicts`.
"""
from __future__ import annotations

import re

STAGES = ("retrieval", "reconciliation", "draft")
STAGE_PREFIX = re.compile(r"^\s*(retrieval|reconciliation|draft|review|export)\s*:\s*", re.IGNORECASE)
WAIVER_PHRASES = ("waived", "not required", "no longer required", "does not require",
                  "not needed", "dispensed with")
IMPERATIVE = re.compile(
    r"^\s*(?:please\s+)?(?:approve|ignore|disregard|grant|refuse|accept|reject|override|delete|"
    r"forget|treat this|you must|you should|do not|don't)\b", re.IGNORECASE)
CLAUSE_SPLIT = re.compile(r"[;,]|\bso\b|\bbut\b|\bbecause\b|\bwhich\b", re.IGNORECASE)
NUMBER = re.compile(r"\d+(?:\.\d+)?")
STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "has", "have", "in", "is", "it", "its",
    "no", "not", "of", "on", "or", "shall", "that", "the", "this", "to", "was", "were", "with",
    "within", "which", "any", "all", "been", "are", "will", "than", "then", "where", "whether",
    "required", "waived", "longer", "does", "require", "needed", "provided", "before", "first",
    "used", "kept", "both", "sides", "over", "under", "authority", "highway", "confirms", "access",
    "applicant", "application", "stated", "shown", "evidenced",
}
TOP_GAPS = 5


class DraftRejected(Exception):
    """The draft failed a consistency check; the findings say what the writer must repair."""

    def __init__(self, blockers: list[dict]):
        super().__init__("; ".join(b["message"] for b in blockers))
        self.blockers = blockers


def _norm(text) -> str:
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def _terms(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z-]{2,}", _norm(text)) if w not in STOPWORDS}


def _numbers(text: str) -> set[str]:
    return set(NUMBER.findall(text))


def _waiver_clauses(reason_text: str) -> list[str]:
    """The clauses of a reason that say something is waived or not required."""
    clauses = []
    for sentence in re.split(r"(?<=[.!?])\s+", reason_text):
        for clause in CLAUSE_SPLIT.split(sentence):
            if any(p in clause.lower() for p in WAIVER_PHRASES):
                clauses.append(clause)
    return clauses


def waiver_conflicts(reasons: list[dict], conditions: list[dict]) -> tuple[list[dict], list[dict]]:
    """Conditions that require what a reason waives. Returns (blockers, warnings).

    A condition that shares a waived topic (two or more content words, or a measurement such as
    "2.4 m by 43 m") with the clause in which a reason waives it is a blocker when that reason is
    the condition's own justification, and a warning when it is another reason.
    """
    blockers, warnings = [], []
    for cond in conditions:
        c_terms, c_nums = _terms(cond.get("text", "")), _numbers(cond.get("text", ""))
        for reason in reasons:
            for clause in _waiver_clauses(reason.get("text", "")):
                shared_terms = c_terms & _terms(clause)
                shared_nums = c_nums & _numbers(clause)
                if len(shared_terms) < 2 and not shared_nums:
                    continue
                shared = sorted(shared_terms | shared_nums)
                own = cond.get("reason_id") == reason.get("id")
                finding = {
                    "rule": "condition_requires_waived_topic" if own else "review_possible_waiver_conflict",
                    "condition": cond.get("id"), "reason": reason.get("id"), "shared": shared,
                    "message": (f"condition {cond.get('id')} requires something that reason "
                                f"{reason.get('id')} says is waived or not required (shared: "
                                f"{', '.join(shared)})" if own else
                                f"condition {cond.get('id')} overlaps {shared} with the waiver in "
                                f"reason {reason.get('id')}; check before release"),
                }
                (blockers if own else warnings).append(finding)
                break
    return blockers, warnings


def check_consistency(draft: dict, policy_doc_ids: set[str]) -> dict:
    """Blockers (defects the writer must repair) and warnings for one fresh draft."""
    reasons, conditions = draft["reasons"], draft["conditions"]
    decision = draft["decision"]
    blockers, warnings = waiver_conflicts(reasons, conditions)

    if decision == "refuse" and conditions:
        blockers.append({"rule": "refusal_with_conditions", "conditions": [c.get("id") for c in conditions],
                         "message": "a refusal cannot impose conditions"})
    if decision == "approve" and conditions:
        blockers.append({"rule": "approve_with_conditions_mismatch",
                         "message": "decision is approve but conditions are attached; "
                                    "it should be approve_with_conditions"})
    if decision == "approve_with_conditions" and not conditions:
        blockers.append({"rule": "approve_with_conditions_mismatch",
                         "message": "decision is approve_with_conditions but no condition is given"})

    for reason in reasons:
        cited_docs = {span_id.split("@", 1)[0] for span_id in reason.get("citations", [])}
        if not cited_docs:
            blockers.append({"rule": "reason_without_citation", "reason": reason.get("id"),
                             "message": f"reason {reason.get('id')} cites no source"})
        elif not cited_docs & policy_doc_ids:
            blockers.append({"rule": "reason_without_policy", "reason": reason.get("id"),
                             "message": f"reason {reason.get('id')} cites no operative policy "
                                        f"(only {sorted(cited_docs)})"})

    for cit in draft.get("citations", []):
        if IMPERATIVE.match(str(cit.get("quote", ""))):
            warnings.append({"rule": "citation_quotes_an_instruction", "span": cit.get("span_id"),
                             "message": f"citation {cit.get('span_id')} quotes an instruction, "
                                        f"not evidence: {cit.get('quote')!r}"})
    return {"blockers": blockers, "warnings": warnings, "consistent": not blockers}


def triage_gaps(gaps: list[str], draft: dict, top: int = TOP_GAPS) -> dict:
    """Deduplicate gaps across stages and rank them by closeness to the decision.

    A gap ranks higher the more content words it shares with the reasons, conditions and
    conflicts; ties keep stage order, then draft order. The draft has no "could change the
    decision" flag, so this overlap is a proxy: calibrate it against officers' view.
    """
    anchor = " ".join([r.get("text", "") for r in draft["reasons"]] +
                      [c.get("text", "") for c in draft["conditions"]] + list(draft["conflicts"]))
    anchor_terms = _terms(anchor)
    seen: dict[str, dict] = {}
    duplicates = 0
    for position, gap in enumerate(gaps):
        match = STAGE_PREFIX.match(gap)
        stage = match.group(1).lower() if match else None
        message = STAGE_PREFIX.sub("", gap).strip()
        key = _norm(message)
        if key in seen:
            duplicates += 1
            if stage and stage not in seen[key]["stages"]:
                seen[key]["stages"].append(stage)
            continue
        seen[key] = {"message": message, "stages": [stage] if stage else [], "position": position,
                     "relevance": len(_terms(message) & anchor_terms)}
    ranked = sorted(seen.values(), key=lambda g: (-g["relevance"], g["position"]))
    return {"presented": ranked[:top], "collapsed_count": max(0, len(ranked) - top),
            "collapsed": ranked[top:], "duplicates_removed": duplicates}


def dedupe_notes(stage_notes: dict[str, list[str]]) -> list[str]:
    """Stage notes as "stage: note", each distinct note once, labelled by the stage that raised it first."""
    seen, out = set(), []
    for stage in STAGES:
        for note in stage_notes.get(stage, []):
            if _norm(note) not in seen:
                seen.add(_norm(note))
                out.append(f"{stage}: {note}")
    return out
