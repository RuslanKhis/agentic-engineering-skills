"""Checks an officer-facing draft must pass before anyone reads it (stdlib only, no model).

Three safeguards, all in ordinary code:

* ``check_draft`` finds internal contradictions: a condition that requires what a reason says
  is waived, a reason that rests on an instruction written inside a source document, a reason
  that cites no local-plan policy, and a decision/conditions mismatch.
* ``triage_gaps`` collapses the same gap repeated under each stage prefix and ranks the rest by
  how closely they touch the decision.
* ``present_gaps`` turns that into the short list the officer sees.

The draft carries no structured "waives"/"requires" fields, so the waiver check reads the
wording of reasons and conditions. It blocks when the condition is justified by the waiving
reason or shares two or more terms with the waived clause, and only warns on a single shared term.
That is a wording heuristic, tuned on one real draft (PA-2026-0181-r1); extend it with cases
from officer feedback rather than loosening it.
"""
from __future__ import annotations

import re

from pipeline.sources import Span

POLICY_PREFIX = "LP-"   # doc_ids of local-plan policy documents (cases/local-plan.json)
STAGE_ORDER = ("retrieval", "reconciliation", "draft", "review")

WAIVER = re.compile(r"\b(?:waived|not required|no longer required|does not require|need not)\b",
                    re.IGNORECASE)
NEGATED_WAIVER = re.compile(r"\bnot\s+waived\b", re.IGNORECASE)
IMPERATIVE = re.compile(
    r"^\s*(?:please\s+)?(?:approve|ignore|disregard|grant|refuse|accept|reject|override|"
    r"delete|forget|treat this|you must|you should|do not|don't)\b", re.IGNORECASE)
STAGE_PREFIX = re.compile(r"^\s*(?:retrieval|reconciliation|draft|review|export)\s*:\s*", re.IGNORECASE)
SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+")
TOKEN = re.compile(r"\d+(?:\.\d+)?|[a-z][a-z-]{2,}")
STOPWORDS = {
    "the", "and", "for", "that", "this", "with", "within", "which", "from", "any", "all", "has",
    "have", "was", "were", "been", "its", "not", "shall", "will", "must", "should", "before",
    "first", "used", "kept", "both", "over", "provided", "also", "but", "where", "then", "required",
    "require", "waived", "longer", "does", "need", "access", "road", "street", "authority",
    "highway", "confirms", "confirm", "one", "two", "out", "see",
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def _terms(text: str) -> set[str]:
    out = set()
    for word in TOKEN.findall(_norm(text)):
        if word in STOPWORDS:
            continue
        out.add(word[:-1] if len(word) > 3 and word.endswith("s") and not word[0].isdigit() else word)
    return out


def _waiving_clauses(text: str) -> list[str]:
    return [s for s in SENTENCE_BREAK.split(text)
            if WAIVER.search(s) and not NEGATED_WAIVER.search(s)]


def check_draft(draft: dict, spans: list[Span]) -> dict:
    """Return ``{"blockers": [...], "warnings": [...], "consistent": bool}`` for one fresh draft."""
    by_id = {s.span_id: s for s in spans}
    reasons = draft.get("reasons", [])
    conditions = draft.get("conditions", [])
    decision = draft.get("decision")
    blockers: list[dict] = []
    warnings: list[dict] = []

    # 1. A condition must not require what a reason says is waived.
    for reason in reasons:
        for clause in _waiving_clauses(reason.get("text", "")):
            waived_terms = _terms(clause)
            for cond in conditions:
                shared = sorted(waived_terms & _terms(cond.get("text", "")))
                cites_reason = cond.get("reason_id") == reason.get("id")
                if len(shared) >= 2 or (shared and cites_reason):
                    blockers.append({
                        "rule": "condition_requires_waived_topic", "condition": cond.get("id"),
                        "reason": reason.get("id"), "shared_terms": shared,
                        "message": f"condition {cond.get('id')} imposes what reason "
                                   f"{reason.get('id')} says is waived ({', '.join(shared)})"})
                elif shared:
                    warnings.append({
                        "rule": "review_possible_waiver_conflict", "condition": cond.get("id"),
                        "reason": reason.get("id"), "shared_terms": shared,
                        "message": f"condition {cond.get('id')} shares '{shared[0]}' with waiving "
                                   f"reason {reason.get('id')}; check they agree"})

    # 2. Decision and conditions agree.
    if decision == "refuse" and conditions:
        blockers.append({"rule": "refusal_with_conditions",
                         "message": "a refusal cannot impose conditions"})
    if decision == "approve" and conditions:
        blockers.append({"rule": "approve_with_listed_conditions",
                         "message": "decision is 'approve' but conditions are listed; "
                                    "use approve_with_conditions or remove them"})
    if decision == "approve_with_conditions" and not conditions:
        blockers.append({"rule": "conditional_approval_without_conditions",
                         "message": "decision is approve_with_conditions but no condition is given"})

    # 3. Every reason rests on at least one local-plan policy.
    for reason in reasons:
        cited = [by_id[c] for c in reason.get("citations", []) if c in by_id]
        if not any(s.doc_id.startswith(POLICY_PREFIX) for s in cited):
            blockers.append({"rule": "reason_without_policy", "reason": reason.get("id"),
                             "message": f"reason {reason.get('id')} cites no local-plan policy"})

    # 4. A source's instruction is evidence of what it says, never a reason.
    flagged: set[tuple[str, str]] = set()
    cited_by_reason = [(r.get("id"), c) for r in reasons for c in r.get("citations", [])]
    cited_by_reason += [(None, c.get("span_id")) for c in draft.get("citations", [])]
    for reason_id, span_id in cited_by_reason:
        span = by_id.get(span_id)
        if (span and not span.doc_id.startswith(POLICY_PREFIX) and IMPERATIVE.match(span.text)
                and (reason_id, span_id) not in flagged):
            flagged.add((reason_id, span_id))
            blockers.append({
                "rule": "relies_on_source_instruction", "reason": reason_id, "span": span_id,
                "message": f"{'reason ' + str(reason_id) if reason_id else 'a citation'} relies on "
                           f"an instruction inside {span.doc_id} ('{span.text.strip()}')"})

    return {"blockers": blockers, "warnings": warnings, "consistent": not blockers}


def triage_gaps(draft: dict, top: int = 5) -> dict:
    """Merge a gap repeated under several stage prefixes; rank by closeness to the decision.

    Gaps are plain strings, so materiality is approximated by overlap with the terms of the
    draft's reasons, conditions and conflicts. Ties keep the earliest stage, then input order.
    """
    decision_terms: set[str] = set()
    for item in draft.get("reasons", []) + draft.get("conditions", []):
        decision_terms |= _terms(item.get("text", ""))
    for conflict in draft.get("conflicts", []):
        decision_terms |= _terms(conflict)

    merged: dict[str, dict] = {}
    duplicates = 0
    for position, gap in enumerate(draft.get("gaps", [])):
        match = STAGE_PREFIX.match(gap)
        stage = match.group(0).split(":")[0].strip().lower() if match else None
        message = STAGE_PREFIX.sub("", gap).strip()
        key = _norm(message)
        if key in merged:
            duplicates += 1
            if stage and stage not in merged[key]["stages"]:
                merged[key]["stages"].append(stage)
            continue
        merged[key] = {"message": message, "stages": [stage] if stage else [],
                       "relevance": len(_terms(message) & decision_terms), "position": position}

    def rank(item):
        first = min((STAGE_ORDER.index(s) for s in item["stages"] if s in STAGE_ORDER),
                    default=len(STAGE_ORDER))
        return (-item["relevance"], first, item["position"])

    ranked = sorted(merged.values(), key=rank)
    return {"presented": ranked[:top], "collapsed_count": max(0, len(ranked) - top),
            "duplicates_removed": duplicates}


def present_gaps(draft: dict, top: int = 5) -> dict:
    """The gaps as the officer sees them: a few messages and a count of the rest."""
    triage = triage_gaps(draft, top)
    return {"gaps": [f"{g['message']} (raised in: {', '.join(g['stages'])})" if g["stages"]
                     else g["message"] for g in triage["presented"]],
            "gaps_collapsed": triage["collapsed_count"],
            "gaps_duplicates_removed": triage["duplicates_removed"]}
