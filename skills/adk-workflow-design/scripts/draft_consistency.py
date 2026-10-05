"""Content safeguards for a grounded draft, in code. Stdlib only; no ADK, no model.

This is a synthetic application pattern, not an ADK class. It encodes the
checks an officer-facing draft must pass before anyone reads it: internal
consistency, warning triage, abstention and source-as-data handling. The
model's own "consistent" label is a judgment to check, never the evidence.

Draft shape consumed by ``check_consistency`` and ``should_abstain``::

    {"decision": "approve" | "refuse" | "abstain",
     "reasons": [{"id": "r1", "text": "...", "supports": "approve" | "refuse",
                  "policies": ["H3"], "waives": ["visibility splay"]}],
     "conditions": [{"id": "c1", "text": "...", "requires": ["visibility splay"],
                     "reason_id": "r1"}],
     "decisive_issues": [{"id": "i1", "label": "...", "operative_policy_found": true}],
     "revision_conflicts": [{"drawing": "...", "decisive": true,
                             "unresolved_revision_conflict": true}],
     "warnings": [{"stage": "retrieval", "code": "search_truncated",
                   "message": "...", "could_change_decision": false}]}

Message-role separation (instructions in the system/developer role, sources in
the user/data role) is the application's job. Only the text helpers live here.

CLI: ``python draft_consistency.py --draft draft.json`` prints a JSON verdict.
Exit 0 when consistent, 1 when a blocking check fails, 2 on invalid input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


DECISIONS = ("approve", "refuse", "abstain")
WAIVER_PHRASES = ("waived", "not required", "no longer required", "does not require")
STAGE_ORDER = ("retrieval", "reconciliation", "draft", "review", "export")
STAGE_PREFIX = re.compile(r"^\s*(?:retrieval|reconciliation|draft|review|export)\s*:\s*",
                          re.IGNORECASE)
IMPERATIVE = re.compile(
    r"^\s*(?:(?:please\s+)?(?:approve|ignore|disregard|grant|refuse|accept|reject|"
    r"override|delete|forget|treat this|you must|you should|do not|don't)\b)",
    re.IGNORECASE,
)
SENTENCE = re.compile(r"[^.!?\n]+[.!?]?\s*")
STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "has", "have", "in",
    "is", "it", "its", "no", "not", "of", "on", "or", "shall", "that", "the",
    "this", "to", "was", "were", "with", "within", "which", "any", "all", "been",
    "required", "waived", "longer", "does", "require", "authority", "highway",
}


class DraftError(ValueError):
    """The draft is not a well-formed object for these checks."""


def _norm(value) -> str:
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def _terms(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z-]{2,}", _norm(text)) if w not in STOPWORDS}


def _validate(draft) -> None:
    if not isinstance(draft, dict):
        raise DraftError("draft must be an object")
    if draft.get("decision") not in DECISIONS:
        raise DraftError(f"decision must be one of {DECISIONS}")
    for key in ("reasons", "conditions", "decisive_issues", "warnings", "revision_conflicts"):
        value = draft.get(key, [])
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise DraftError(f"{key} must be a list of objects")


def check_consistency(draft: dict) -> dict:
    """Return blockers, warnings and a consistent flag for one fresh draft."""
    _validate(draft)
    decision = draft["decision"]
    reasons = draft.get("reasons", [])
    conditions = draft.get("conditions", [])
    blockers: list[dict] = []
    warnings: list[dict] = []

    # (a) A condition must not require what a reason says is waived.
    waived = {}
    for reason in reasons:
        for topic in reason.get("waives", []) or []:
            waived.setdefault(_norm(topic), reason.get("id"))
    for condition in conditions:
        for topic in condition.get("requires", []) or []:
            if _norm(topic) in waived:
                blockers.append({
                    "rule": "condition_requires_waived_topic",
                    "condition": condition.get("id"), "reason": waived[_norm(topic)],
                    "topic": topic,
                    "message": f"condition {condition.get('id')} requires '{topic}' "
                               f"which reason {waived[_norm(topic)]} waives",
                })
        # Keyword fallback for drafts without structured fields: review, not block.
        if not condition.get("requires"):
            condition_terms = _terms(condition.get("text", ""))
            for reason in reasons:
                text = _norm(reason.get("text", ""))
                if any(phrase in text for phrase in WAIVER_PHRASES):
                    shared = condition_terms & _terms(reason.get("text", ""))
                    if shared:
                        warnings.append({
                            "rule": "review_possible_waiver_conflict",
                            "condition": condition.get("id"), "reason": reason.get("id"),
                            "shared_terms": sorted(shared),
                            "message": f"condition {condition.get('id')} shares "
                                       f"{sorted(shared)} with a waiving reason "
                                       f"{reason.get('id')}; review before release",
                        })

    # (b) A refusal carries no conditions.
    if decision == "refuse" and conditions:
        blockers.append({"rule": "refusal_with_conditions",
                         "conditions": [c.get("id") for c in conditions],
                         "message": "a refusal cannot impose conditions"})

    # (c) Every reason cites at least one operative policy.
    for reason in reasons:
        if not [p for p in reason.get("policies", []) or [] if str(p).strip()]:
            blockers.append({"rule": "reason_without_policy", "reason": reason.get("id"),
                             "message": f"reason {reason.get('id')} cites no policy"})

    # (d) Decision and reasons agree in direction.
    directions = {reason.get("supports") for reason in reasons} - {None}
    if decision in ("approve", "refuse") and directions:
        if decision not in directions:
            blockers.append({"rule": "decision_direction_disagrees", "decision": decision,
                             "reasons": [r.get("id") for r in reasons],
                             "message": f"decision {decision} but every reason supports "
                                        f"{sorted(directions)}"})
        elif len(directions) > 1:
            opposing = [r.get("id") for r in reasons if r.get("supports") != decision]
            warnings.append({"rule": "mixed_reason_direction", "reasons": opposing,
                             "message": f"reasons {opposing} support the opposite "
                                        f"of decision {decision}; state why they do not prevail"})

    # (e) Abstention has no conditions and names what is undecided.
    if decision == "abstain":
        if conditions:
            blockers.append({"rule": "abstain_with_conditions",
                             "message": "an abstention cannot impose conditions"})
        if not draft.get("decisive_issues"):
            blockers.append({"rule": "abstain_without_decisive_issue",
                             "message": "an abstention must name the decisive issue it cannot settle"})

    return {"blockers": blockers, "warnings": warnings, "consistent": not blockers}


def triage_warnings(warnings: list[dict], top: int = 5) -> dict:
    """Deduplicate identical gaps across stages and rank by materiality."""
    seen: dict[str, dict] = {}
    duplicates = 0
    for warning in warnings:
        if not isinstance(warning, dict):
            raise DraftError("warnings must be objects")
        key = _norm(STAGE_PREFIX.sub("", str(warning.get("message", ""))))
        if not key:
            key = _norm(warning.get("code", ""))
        if key in seen:
            duplicates += 1
            kept = seen[key]
            kept["could_change_decision"] = bool(kept.get("could_change_decision")
                                                 or warning.get("could_change_decision"))
            stages = kept.setdefault("stages", [])
            if warning.get("stage") and warning.get("stage") not in stages:
                stages.append(warning.get("stage"))
            continue
        kept = dict(warning)
        kept["stages"] = [warning.get("stage")] if warning.get("stage") else []
        seen[key] = kept

    def rank(item: dict):
        stage = item.get("stage")
        order = STAGE_ORDER.index(stage) if stage in STAGE_ORDER else len(STAGE_ORDER)
        return (0 if item.get("could_change_decision") else 1, order)

    ranked = sorted(seen.values(), key=rank)
    return {"presented": ranked[:top], "collapsed_count": max(0, len(ranked) - top),
            "duplicates_removed": duplicates}


def should_abstain(draft: dict) -> tuple[bool, list[str]]:
    """Decline to draft when a decisive input is missing or unresolved."""
    _validate(draft)
    reasons = []
    for issue in draft.get("decisive_issues", []):
        if issue.get("operative_policy_found") is False:
            reasons.append(f"no operative policy found for decisive issue {issue.get('id')}")
    for conflict in draft.get("revision_conflicts", []):
        if conflict.get("decisive") and conflict.get("unresolved_revision_conflict"):
            reasons.append(f"unresolved revision conflict on decisive drawing "
                           f"{conflict.get('drawing', '?')}")
    return bool(reasons), reasons


def delimit_source(text: str, label: str) -> str:
    """Wrap untrusted source text in labelled delimiters the instructions can name."""
    label = re.sub(r"[^\w .-]", "", str(label)).strip() or "document"
    return f"<<<source {label}>>>\n{text}\n<<<end source {label}>>>"


def label_imperatives(text: str) -> str:
    """Prefix sentences that instruct the reader; descriptive sentences pass through."""
    out = []
    for match in SENTENCE.finditer(text):
        sentence = match.group(0)
        if IMPERATIVE.match(sentence):
            lead = len(sentence) - len(sentence.lstrip())
            sentence = sentence[:lead] + "[instruction found in source, not followed] " + sentence[lead:]
        out.append(sentence)
    return "".join(out)


def adversarial_review_prompt(draft_summary: str) -> str:
    """Ask for the strongest objection, and allow a rejection or an honest 'none'."""
    return (
        "Review this draft decision as its strongest critic.\n"
        f"{draft_summary.strip()}\n"
        "State the single strongest reason the draft is wrong, citing the "
        "evidence or policy it rests on. Then give a verdict: reject, revise or "
        "accept. Rejecting is an acceptable outcome; so is 'no strong reason "
        "found' when the evidence genuinely supports the draft. Do not confirm "
        "support you have not checked."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        draft = json.loads(args.draft.read_text(encoding="utf-8"))
        verdict = check_consistency(draft)
        abstain, why = should_abstain(draft)
        verdict["abstain"] = {"recommended": abstain, "reasons": why}
        verdict["triage"] = triage_warnings(draft.get("warnings", []), top=args.top)
    except (OSError, ValueError, DraftError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=2))
    return 0 if verdict["consistent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
